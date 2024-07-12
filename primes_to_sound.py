import numpy as np
import pyaudio
from scipy.io.wavfile import write

# Ensure script is usable even if user environment does not contain pyqtgraph package.
try:
    import pyqtgraph as pg
except ImportError as e:
    pg = None
    exc1 = e


def is_prime(n: int) -> bool:
    """
    Returns True if n is prime, else returns False.
    :param n: int
    :return: bool
    """
    if n <= 1:
        return False

    if n == 2:
        return True

    if not n & 1:  # This is bitwise and. n & 1 is true for all odd numbers.
        return False

    # I avoid dependency on math package but math.sqrt() is actually a little faster.
    for k in range(3, int(n**0.5) + 1):
        if not n % k:  # "if not n%k" is much less explicit but also measurably faster than "if n%k == 0"
            return False

    return True

# If you want to change / optimize the is_prime() function you may want to uncomment bellow function to allow pytest
# to check that it continues to work ok.

# def test_is_prime():
#     prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
#
#     for val in range(max(prime_list) + 1):
#         ans = is_prime(val)
#         print(f'for value {val} ans is {ans}')
#         assert ans is True if val in prime_list else ans is False


def show_plot():  # optional

    if pg is None:
        raise ImportError(f'"show_plot()" function requires module "pyqtgraph", which failed on import with '
                          f'error:\n{exc1}')

    from pyqtgraph.Qt import QtGui

    pg.setConfigOptions(antialias=True)
    plt = pg.plot()
    plt.plot(primes_signal)
    plt.setLabel('left', 'Norm. pulse density')
    plt.setLabel('bottom', 'Samples')
    print('Close the plot to play audio.')
    QtGui.QApplication.instance().exec_()


if __name__ == "__main__":

    # Convert prime number positions to an audio waveform using pulse density, digital to analog conversion.

    # Define how many values will be checked if they belong to primes.
    SEARCH_LEN = int(500000)
    # Width of the addition window for the pulse density conversion.
    DAC_SIGMA_FRAME_LEN = 256
    # Below value in Hz should correspond to something your sound card can support. (44.1kHz is usually default)
    AUDIO_OUTPUT_SAMPLING_FREQUENCY = 44100

    # Preallocate numpy arrays for speed.
    primes_positions = np.zeros(SEARCH_LEN)
    primes_signal = np.zeros(SEARCH_LEN)

    print('Searching for primes...')
    for x in range(SEARCH_LEN):
        if is_prime(x):
            primes_positions[x] = 1

    print(f'Found {np.sum(primes_positions):.0f} primes up to {SEARCH_LEN}')

    # generate a waveform using pulse density conversion:
    print(f'\nGenerating pulse density waveform at:\n'
          f'    DAC_SIGMA_FRAME_LEN = {DAC_SIGMA_FRAME_LEN}')
    for x in range(SEARCH_LEN-DAC_SIGMA_FRAME_LEN):
        primes_signal[x] = np.sum(primes_positions[x:x + DAC_SIGMA_FRAME_LEN]) / DAC_SIGMA_FRAME_LEN

    # remove offset
    primes_signal -= np.average(primes_signal)
    # normalize
    primes_signal /= np.max(primes_signal)
    # format
    primes_signal = primes_signal.astype(np.float32)

    # uncomment to explore the signal visually before listening (you will need pyqtgraph in your env)
    # show_plot()

    # send signal to audio output using pyAudio

    # set up mono audio stream:
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=AUDIO_OUTPUT_SAMPLING_FREQUENCY,
                    output=True)

    print(f'\nStarting audio on default output device at:\n'
          f'    AUDIO_OUTPUT_SAMPLING_FREQUENCY = {AUDIO_OUTPUT_SAMPLING_FREQUENCY}')

    # write the output in one go. (lazy)
    stream.write(primes_signal.tobytes())

    # clean up
    stream.stop_stream()
    stream.close()
    p.terminate()

    # write to a wave file
    write('sound_of_primes.wav', AUDIO_OUTPUT_SAMPLING_FREQUENCY, primes_signal)
