# =============================================================================
# This code presents an example of use of the TSA algorithms. 
# for the computation of the time-synchronous average of the position of a fan blade as it slows down after switchoff.
# This example is inspired by the Matlab example presented in the 'tsa' function help page 
# 
# Two methods are tested:
# - Time-domain method (function pyTSA_TimeDomain)
# - Frequency-domain method (function pyTSA_fft)
#
# by David Raus
# 21/11/02
# =============================================================================


# Load librairies
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp


def main():

    global t,signal,nPulse,N
    
    # Initialize instantaneous signal
    fs = 1000
    time_lim = 3
    t = np.arange(0,time_lim,1/fs)

    rpm0 = 2400   
    a = 0.1
    f0 = rpm0/60    # original rotation frequency (Hz)
    T = 0.75        # decay time (s)
    phi = 2*np.pi*f0*T*(1-np.exp(-t/T))
    
    signal = a*np.cos(phi) + np.random.randn(np.size(phi))/200
        
    # Detect beginning of cycles
    nPulse,_ = sp.signal.find_peaks(-a*np.cos(phi))
    
    # Plot signal to check that cycles beginning are well detected
    plt.figure()
    plt.plot(t,signal)
    plt.plot(t[nPulse],signal[nPulse],'r+')
    plt.xlabel('$t$')
    plt.ylabel('Amplitude')
    

    # Compute the phase-averaged signal with the Time-domain method
    from pyTSA_functions import pyTSA_TimeDomain
    y_TSA_TimeDomain,t_interp = pyTSA_TimeDomain(signal,t,nPulse,fs)

    # Compute the phase-averaged signal with the fft method
    from pyTSA_functions import pyTSA_fft
    y_TSA_fft,t_TSA_fft = pyTSA_fft(signal,nPulse,fs)
    

    # Plot the phase-averaged signal and compare with the instantaneous signal
    plt.figure()

    for pp in np.arange(len(nPulse)-1):
        t_instant_norm = (t[nPulse[pp]:nPulse[pp+1]]-t[nPulse[pp]])/max((t[nPulse[pp]:nPulse[pp+1]]-t[nPulse[pp]]));
        p_instant, = plt.plot(t_instant_norm,signal[nPulse[pp]:nPulse[pp+1]],color=(0.8, 0.8, 0.8))
    p_method1, = plt.plot((t_interp-t_interp[1])/max(t_interp-t_interp[1]),np.rot90(y_TSA_TimeDomain),color=(0.1, 0.2, 0.5))
    p_method2, = plt.plot(t_TSA_fft/max(t_TSA_fft),y_TSA_fft,'r')
    plt.legend([p_instant, p_method1, p_method2],["Original signal","TSA: Time-domain method","TSA: FFT method"])
    plt.xlabel("Phase (rotations)")
    plt.ylabel("Amplitude")
    plt.title('Time-synchronous average')
    
# %%
if __name__ == '__main__':
    main()
    
    



