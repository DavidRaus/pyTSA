The Matlab function 'tsa' allow to compute the phase-average of a signal with varying cycles length.

As a avid user of this Matlab function, I was frustrated not to find an equivalent with Python.

## Algorithms
Time-domain method:
1. Divide the signal into segments corresponding to the different cycles
2. Interpolate the signals in each segment on the same number of sample
3. Compute the average of all the resampled segments

Frequency-domain method:
1. Divide the signal into segments corresponding to the different cycles
2. Compute the fft of each segment
3. Truncate the results on each segment so that all fft have the same length as the one of the shortest cycle
4. Average all the spectra
5. Compute the inverse fft to obtain the phase-averaged signal in the time domain.

## Reference
Bechhoefer, Eric, and Michael Kingsley. "A Review of Time-Synchronous Average Algorithms." Proceedings of the Annual Conference of the Prognostics and Health Management Society, San Diego, CA, September-October, 2009.

## David Raus
21/11/02
