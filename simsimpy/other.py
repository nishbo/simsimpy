import sys
import math
import time

import numpy


miliseconds = 1.
seconds = 1000. * miliseconds
minutes = 60. * seconds
hours = 60. * minutes
days = 24. * hours


def time_stamp(gmtime=None, sep=':'):
    """Formats time string as I like."""
    if gmtime is None:
        gmtime = time.gmtime()
    timestring = '%Y.%m.%d_%H'+sep+'%M'+sep+'%S'
    return time.strftime(timestring, gmtime)


def dxrange(start, stop, step=1., rnd=None):
    """Floating-point xrange."""
    r = start
    stop += step*0.001
    if rnd is None:
        rnd = int(math.ceil(-math.log(step, 10.)))
    while r < stop:
        yield r
        r += step
        r = round(r, rnd)


def dlogrange(start, step, steps=-1, stop=None):
    """Floating-point exponential xrange."""
    r = start
    if step == 1:
        raise ValueError("Power of 1 increment, choose different step.")
    if steps < 0 and stop is not None:
        steps = abs(math.ceil(math.log(stop/start, step)))
    rnd = int(abs(math.log(sys.float_info.epsilon, 10.)))

    for _ in xrange(int(steps)):
        yield r
        r *= step
        r = round(r, rnd)


class Bounds(object):
    def __init__(self, bounds=None):
        self.min = numpy.array([bound[0] for bound in bounds])
        self.max = numpy.array([bound[1] for bound in bounds])

    def __call__(self, **kwargs):
        x = kwargs["x_new"]
        return (bool(numpy.all(x <= self.max)) and
                bool(numpy.all(x >= self.min)))
