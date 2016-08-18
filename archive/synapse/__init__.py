"""Synapse module of SimSimPy package.

Contains some synapse plasticity models' classes. All models have to have
following methods and varibles:
    reset(self)
    presynaptic_spike(self, time)
    postsynaptic_spike(self, time)
    
For description see help of models.
"""

from stdpsyn import *
from tsmsyn import *
