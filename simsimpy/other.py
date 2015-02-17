import math
import time


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
