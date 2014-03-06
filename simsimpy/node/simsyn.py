import myerror


class SimpleSynapse(object):
    """Simple synapse that can work as both current-based and conductance-based
    synapse.

    Defines only the curve of spikes. No plasticity included. Equations:
    tau = [tau[0], tau[1]]
        tau[0] * tau[1] * g'' + (tau[0] + tau[1]) * g' + g =
          sum_i(weight_i(t) * sum_j(delta(spike_i^j)))
    (sum of all incoming spikes (j) from synapse (i))

    Attributes:
        verbose: A boolean indicating if the neuron will print information
          about itself sometimes, e.g. when reset() or spike occur.
        dt: Length of time step, shen using step() method, ms.
        tau: List of two time constants for the synapse type, ms.
        g: g=[g, dg/dt]. List of current conductance and additional state
          variable (derivative).
        base: Indicates which type is the synapse, current or conductance.
          Second value represents multiplicator (for inhibitory or excitatory
          synapses) and Nernst potential for current- and conductance-based
          synapse respectively.
    """

    def __init__(self, tau=[3., 0.], base=['current', 1.]):
        """Inits conductance-based synapse with default attributes."""
        self.verbose = False
        self._tau = [0., 0.]
        self.tau = tau
        self.reset()
        self.dt = 0.01
        self.base = base

    def reset(self):
        """Resets changable variables for the synapse.

        Sets g to zero value. Prints a message if verbose.
        """
        self.g = [0., 0.]
        if self.verbose:
            print 'Simple synapse was reset.'

    def tau():
        doc = "Time-constants for current curve."

        def fget(self):
            return [self._tau[0], self._tau[1]]

        def fset(self, value):
            if value[0] > 0. and value[1] > 0.:
                self._tau[0] = value[0]
                self._tau[1] = value[1]
                self.step = self._step_two_times
            elif value[0] > 0.:
                self._tau[0] = value[0]
                self._tau[1] = 0.
                self.step = self._step_one_time
            elif value[1] > 0.:
                self._tau[0] = value[1]
                self._tau[1] = 0.
                self.step = self._step_one_time
            else:
                raise myerror.Error(
                    'Trying to set wrong time in simple synapse.',
                    value)
        return locals()
    tau = property(**tau())

    def base():
        doc = "conductance or current base."

        def fget(self):
            return self._base

        def fset(self, value):
            if value[0] == 'current' or value[0] == 'conductance':
                self._base = value
            else:
                raise myerror.Error('Wrong base of synapse.'
                                    ' Use \'conductance\' or \'current\'.',
                                    value)
        return locals()
    base = property(**base())

    def _step_one_time(self, weight):
        self.g[0] += weight
        self.g = [self.g[0] - self.dt * self.g[0] / self.tau[0], self.g[1]]
        return self.g[0]

    def _step_two_times(self, weight):
        self.g[1] += weight
        self.g = [self.g[0] + self.g[1] * self.dt,
                  self.g[1] - ((self.tau[0] + self.tau[1])*self.g[1]
                  + self.g[0]) / (self.tau[0] * self.tau[1]) * self.dt]
        return self.g[0]

    def step(self, weight):
        """Propagates synapse dynamics forward for dt.

        Args:
            weight: Spike with this value occured. Weight is added to
              conductance in defined way.

        Returns:
            Current conductance of this synapses.
        """
        pass