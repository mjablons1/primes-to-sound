# primes-to-sound
Have you ever wondered what the primes would sound like? This script conversts primes positions into an audio signal using a primitive form of pulse density D-A conversion.

## Dependencies
You need numpy and pyaudio packages. Optionally you can view the output waveform using pyqtgraph.

## How does it work?

The script marks prime positions with a value of 1 on the x-axis. A conversion window of a given length is used to compute the density of primes within that window. The density is calculated each time the conversion window is moved along the x axis. The subsequent density values are treated as a waveform. 

After normalizing the waveform is played back on your audio output device.

## What does it sound like?

After listening on the headphones, the signal sounds to me very similar to the background noise in a passenger jet airliner with low components resembling perturbed air stream and higher sounds resembling high speed rotating engines. Changing the window length does not seem to change that impression much except for increasing / decreasing fidelity (short windows cause lower bit depth output, longer generate smoother waveforms). It's also interesting to play with the sampling rate as this changes the pitch of the sound.

## What does it look like?
You can uncomment the show_plot() call to interactively preview the output waveform (you will need pyqtgraph package). Here an example output:

The primes' density is high for initial values and decreases quite quickly into a form of steady state density for larger values, making for an interesting audio signal.

## What is it good for?

No idea, you tell me! However, before you endeavour, be advised that It's potentially entirely without purpose or application. (Can't be more fun.)

## What else could you do with it?

Few ideas. For start, you can play with the window length and sampling rate just to hear the difference.

Perhaps it would be interesting to smooth out the waveforms using some scipy filters. 

As a more advanced coding exercise you could place the signal generation in a producer thread and the audio output logging into a consumer tread just to see how long it takes before you run out of the shared buffer due to computational complexity of looking for primes among ever larger values vs the constant audio output rate. Optimizing the primes search speed would then translate into the benefit of listening longer before you run out of buffer. A simple test_is_prime() function is readily included. Just uncomment it to see if the optimized code still finds a handful of small primes correctly.(you will need pytest).

Please fork until you are bored. Thank you.