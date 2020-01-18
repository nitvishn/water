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
    if type(date) == numpy.ndarray:
        valuations = []
        for d in date:
            valuations.append((d - datetime.datetime.strptime("200101", "%Y%m")).days)
        return numpy.array(valuations)
    return (date - datetime.datetime.strptime("200101", "%Y%m")).days

class Community(object):
    def __init__(self, name, x, y, type, locality, vendor_id, tanker_supply_factor = 0.1):
        self.name = name
        self.x = x
        self.y = y
        self.type = type
        self.locality = locality
        self.vendor_id = vendor_id
        self.tanker_supply_factor = tanker_supply_factor

    def assign_function(self, res):
        """
        returns None
        """
        usage_per_person = 150
        if self.type == 'Apartment':
            persons = random.randrange(100, 200)
        elif self.type == 'House':
            persons = random.randrange(2, 6)
        elif self.type == 'Restaurant':
            persons = random.randrange(20, 30)

        mean = usage_per_person * persons
        amp = 0.2 * mean
        self.fit_function = lambda x: amp * numpy.sin(x*res['omega'] + res['phase']) + mean

    def predict(self, date):
        return self.tanker_supply_factor * self.fit_function(date_valuation(date))

    def __str__(self):
        return '<Community \'' + self.name + '\' (' + str(self.type)+ '): ' + str(self.x) + ',' + str(self.y) + '>'

class Tanker(object):
    def __init__(self, max_capacity, cur_capacity = None):
        self.max_capacity = max_capacity
        self.cur_capacity = self.max_capacity or cur_capacity
