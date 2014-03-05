import math
import random

class Synapse(object):
    """Tsodyks-Markram short-term synaptic plasticity.

    As described in Maass, W., & Markram, H. (2002). Synapses as dynamic memory
    buffers. Neural Networks, 15, 155-161.

    Attributes:
        r, u, U, D, F: Model parameters.
        last_presynaptic_spike: Time of last presynaptic spike.
    """

    def __init__(self):
        """Initializes an excitatory TM synapse."""
        self.set_excitatory()
        self.shuffle_constants()
        self.reset()
        
    def U():
        doc = "U model variable. From 0 to 1."
        def fget(self):
            return self._U
        def fset(self, value):
            self._U = (value if value < 1. else 1.) if value > 0. else 0.
        return locals()
    U = property(**U())

    def u():
        doc = "u model variable. From 0 to 1. Always eq to U in the beginning."
        def fget(self):
            return self._u
        def fset(self, value):
            self._u = (value if value < 1. else 1.) if value > 0. else 0.
        return locals()
    u = property(**u())

    def _gauss_in_range(self, mu, sigma, mi, ma):
        ans = random.gauss(mu, sigma)
        while ans > ma or ans < mi:
            ans = random.gauss(mu, sigma)
        return ans

    def reset(self):
        """Resets synapse.

        Sets last_presynaptic_spike = -1000., r = 1., u = U.
        """
        self.last_presynaptic_spike = -1000.
        self.r = 1.
        self.u = self.U

    def set_excitatory(self):
        """Sets predefined excitatory parameters."""
        self.U = 0.5
        self.D = 1100.
        self.F = 50.

    def set_inhibitory(self):
        """Sets predefined inhibitory parameters."""
        self.U = 0.25
        self.D = 700.
        self.F = 20.

    def shuffle_constants(self):
        """Missy Elliott U, D, F."""
        self.U = self._gauss_in_range(self.U, self.U/10., 0., 1.)
        self.D = self._gauss_in_range(self.D, self.D/10., 0., 10.*self.D)
        self.F = self._gauss_in_range(self.F, self.F/10., 0., 10.*self.F)

    def presynaptic_spike(self, time):
        """Processes presynaptic spike.

        Args:
            time: Time of the arriving of spike to the synapse.

        Returns:
            Weight of this synapse. u*r.
        """
        h = time - self.last_presynaptic_spike
        [self.u, self.r] = [ self.U + self.u*(1. - self.U)*math.exp(-h/self.F), 
                    1. + (self.r - self.u*self.r - 1.)*math.exp(-h/self.D) ]
        self.last_presynaptic_spike = time
        return self.u*self.r

    def postsynaptic_spike(self, time):
        """Processes postsynaptic spike.

        Args:
            time: Time of the excitation of postsynaptic neuron.

        Returns:
            Weight of this synapse. u*r.
        """
        return self.u*self.r
