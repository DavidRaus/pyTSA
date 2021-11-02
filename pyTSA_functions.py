# =============================================================================
# Functions to compute the time-synchronous average of a signal with varying cycle length
#
# Two methods are tested:
# - Time-domain method (function pyTSA_TimeDomain)
# - Frequency-domain method (function pyTSA_fft)
#
# by David Raus
# 21/11/02
# =============================================================================


import numpy as np
import scipy


# Time-domain TSA
def pyTSA_TimeDomain(y,t,nPulse,fs):
    
    # Length of the signal for the interpolation
    N = max(np.diff(nPulse/fs))*fs
    
    y_TSA_TimeDomain = np.zeros((1,round(N)))
    PP = 0

    for pp in np.arange(len(nPulse)-1):
        
        # Interpolates the signal onto grids of equally spaced samples corresponding to the different cycles.
        t_interp = np.linspace(t[nPulse[pp]],t[nPulse[pp+1]],round(N))
        y_rs = scipy.interpolate.pchip_interpolate(t[nPulse[pp]:nPulse[pp+1]],y[nPulse[pp]:nPulse[pp+1]],t_interp, der=0, axis=0)
        
        # Concatenates the resampled signal segments
        y_TSA_TimeDomain = y_TSA_TimeDomain + y_rs
        PP = PP + 1
        
    # Computes the average of all the segments.    
    y_TSA_TimeDomain = y_TSA_TimeDomain/PP

    return y_TSA_TimeDomain,t_interp



# Frequency-domain TSA
def pyTSA_fft(y,nPulse,fs):    
    
    nF = np.min(np.diff(nPulse))-1
    Y_TSA_fft_tmp = np.zeros((len(nPulse),nF),dtype=complex)
    
    PP = 0
    
    for pp in np.arange(len(nPulse)-1):
        
        # Breaks the signal into segments corresponding to the different cycles.
        signal_crop = y[nPulse[pp]:nPulse[pp+1]]
        
        # Computes the discrete Fourier transform of each segment.
        spec = np.fft.fft(signal_crop)/len(signal_crop)
    
        # Truncates the longer transforms so all transforms have the same length.
        Y_TSA_fft_tmp[pp,:] = spec[0:nF]*nF*2
        
        PP = PP +1
    
    # Averages the spectra
    Y_TSA_fft = np.mean(Y_TSA_fft_tmp,0)

    # Computes the inverse discrete Fourier transform of the average to convert it to the time domain
    fd = np.append(np.append(Y_TSA_fft,0),np.conj(np.flipud(Y_TSA_fft[1:])))

    y_TSA_fft = np.real(np.fft.ifft(fd));
    t_TSA_fft = np.arange(0,len(y_TSA_fft)/fs,1/fs)
    
    return y_TSA_fft,t_TSA_fft