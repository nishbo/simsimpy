import os
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


def vesre(x):
    a = list(x)
    a[0], a[1:] = a[-1], a[:-1]
    return a


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
    """Creates callable Bounds object from a list of bounds.

    bounds: [[min, max], [min, max], ...]
    instance of Bounds(x, ...) or Bounds(x_new=x) or Bounds(x=x) checks if x
        is inside bounds.
    priority: kwargs x, kwargs x_new, args.
    """
    def __init__(self, bounds):
        self.min = numpy.array([bound[0] for bound in bounds])
        self.max = numpy.array([bound[1] for bound in bounds])

    def __call__(self, *args, **kwargs):
        if 'x' in kwargs.keys():
            x = kwargs['x']
        elif 'x_new' in kwargs.keys():
            x = kwargs['x_new']
        else:
            x = args[0]
        return (bool(numpy.all(x <= self.max)) and
                bool(numpy.all(x >= self.min)))


class Logger(object):
    """Doubles output into a file

    Usage:
        sys.stdout = Logger()
    Filename defaults to <pid>.log
    """
    def __init__(self, filename=None):
        self.terminal = sys.stdout
        if filename is None:
            filename = str(os.getpid()) + '.log'
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass
