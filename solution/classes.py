import pylab
import pandas as pd
import datetime
import math
import numpy, scipy.optimize
import pylab as plt
import random

def fit_sin(tt, yy):
    """
    Fit sin to the inumpyut time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"
    """
    tt = numpy.array(tt)
    yy = numpy.array(yy)
    ff = numpy.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(numpy.fft.fft(yy))
    guess_freq = abs(ff[numpy.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = numpy.std(yy) * 2.**0.5
    guess_offset = numpy.mean(yy)
    guess = numpy.array([guess_amp, 2.*numpy.pi*guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):  return A * numpy.sin(w*t + p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*numpy.pi)
    fitfunc = lambda t: A * numpy.sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": numpy.max(pcov), "rawres": (guess,popt,pcov)}

def get_res(filename):
    data = pd.read_csv('austin_water.csv')
    x = list(set(data['Year Month']))
    x.sort()
    y = []
    for date in x:
        y.append(sum(data.loc[data['Year Month'] == date]['Total Gallons']))

    xShow = [datetime.datetime.strptime(str(i), "%Y%m") for i in x]
    x = numpy.array([date_valuation(k) for k in xShow])
    return fit_sin(x, y)

def date_valuation(date):
    if type(date) == numpy.ndarray
