#!/usr/bin/env python

"""
Routines for Manipulating Band-Limited Signals
==============================================

- gen_band_limited    Generate band-limited signal

"""

__all__ = ['gen_band_limited']

from numpy import array, ceil, complex, exp, pi, zeros
from numpy.random import rand, randint, randn
from numpy.fft import irfft
from scipy.signal import firwin, lfilter

def gen_band_limited(dur, dt, fmax, np=None, nc=3):
    """Generate a uniformly sampled, band-limited signal.

    Parameters
    ----------
    dur : float
        Duration of signal (s).
    dt : float
        Sampling resolution; the sampling frequency is 1/dt Hz.
    fmax : float
        Maximum frequency (Hz).

    Returns
    -------
    u : ndarray of floats
        Generated signal.
        
    Optional Parameters
    -------------------
    np : float
        Noise power (dB). If np != None, Gaussian white noise
	is added to the generated signal before the latter is filtered.
    nc : int
        Number of discrete frequency components in generated signal.

    """

    # Since the signal generated by this function must be real, the
    # frequency components on one side of its fft representation are
    # complex conjugates of those on the other side; this allows for
    # the use of the inverse real fft (irfft), which only requires the
    # frequency components on one side of the full fft as input (and
    # hence allows this function to consume less memory when run).

    # The maximum frequency may not exceed the Nyquist frequency:
    fs = 1.0/dt
    if fmax > fs/2:
        raise ValueError("maximum frequency may not exceed the Nyquist frequency")

    # Determine number of entries in generated signal. This
    # corresponds to the length of arange(0, dur, dt):
    n = int(ceil(dur/dt))

    # Randomly set nc distinct frequency components:    
    f = zeros(int(n/2)+1, complex) # only one side of the spectrum is needed
    fmaxi = int(n*fmax/fs)
    if fmaxi < nc:
        raise ValueError("maximum frequency %f is too low to provide %i frequency components" % (fmax, nc))

    # The first element in the fft corresponds to the DC component;
    # hence, it is not set:
    ci = set()
    while len(ci) < nc:
        temp = randint(1, fmaxi+1)
        while temp in ci:
            temp = randint(1, fmaxi+1)
        ci.add(temp)
    ci = array(list(ci))
    p = -2*pi*rand(nc)
    f[ci] = (n/2)*exp(1j*p)

    # Create the signal by transforming the constructed frequency
    # representation into the time domain and adding white noise if so
    # specified:
    u = irfft(f,n)
    if np != None:
        u += randn(len(u))*10**(np/20)

    # Filter the result to get rid of high frequency components
    # introduced by the noise. Since a cutoff of 1 corresponds to the
    # Nyquist frequency 1/(2*dt), the cutoff corresponding to the
    # frequency fmax must be fmax/(1/2*dt):
    b = firwin(40, 2*fmax*dt)
    u = lfilter(b, 1, u)

    return u
