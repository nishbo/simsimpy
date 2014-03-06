"""Neuron module of SimSimPy package.

Contains some neuron models' classes. All models have to have following
methods and varibles:
    self.verbose
    self.I_stim
    self.dt
    self.integration_method
    step(self)
    set_default_constants(self)
    flush(self)
    reset(self)
    name(self)
    step(self, I=)
    force_spike(self)
For description see help of models.
"""

from hhneu import *
from liafneu import *
