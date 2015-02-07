import myerror


class LIAF(object):
    """Basic leaky integrate-and-fire neuron with no oscillation.

    Class represents a basic leaky integrate-and-fire neuron. Dypamics:
    If V<V_th:
        V' = - (V - V_rest) / tau_m + I * r_m
    else:
        spike occured
        V = V_reset
        neuron stays in refractory period for tau_ref
    Instance of the class can step with euler or runge-kutta4 method.

    Attributes:
        verbose: A boolean indicating if the neuron will print information
          about itself sometimes, e.g. when reset() or spike occur.
        dt: Length of time step, shen using step() method, ms.
        I_stim: Constant current that is presented to a neuron, pA.
        integration_method: String that defines used integration method. Now
          has two possible states: 'euler' and 'rk4'. If wrongly set, raises an
          myerror.Error exception, method does not change.
        r_m: Neuron membrane resistance, GOhm.
        tau_m: Membrane time constant, ms.
        c_m: Membrane capacity, nF.
        V_rest: Resting potential of a neuron, mV.
        V_reset: This value is assigned to the neuron during refractory period.
        V_th: Threshold potential for spike, mV. When potential crosses this
        value, neuron spikes.
        V: Current neuron membrane potential, mV.
        time: Current time for the neuron, ms.
        spikes: List of spike times of the neuron. Time of spike is defined by
        'self.time' attribute.
        tau_ref: Duration of refractory period of forced spike, ms.
    """

    def __init__(self):
        """Inits leaky integrate-and-fire neuron with default attributes."""
        self.verbose = False
        self.I_stim = 0.
        self.dt = 0.01

        self.set_default_constants()
        self.flush()
        self.reset()
        self.integration_method = 'rk4'

    def integration_method():
        doc = "Integration method of a neuron."

        def fget(self):
            return self._integration_method

        def fset(self, value):
            if value == 'rk4':
                self._integration_method = 'rk4'
                self._step = self._step_runge_kutta4
            elif value == 'euler':
                self._integration_method = 'euler'
                self._step = self._step_euler
            else:
                raise myerror.Error(
                    'Wrong string provided as an integration method.',
                    value)
        return locals()
    integration_method = property(**integration_method())

    def c_m():
        doc = "Membrane capacity and corrects resistance."

        def fget(self):
            return self._c_m

        def fset(self, value):
            self._c_m = value
            self._r_m = self.tau_m / value
        return locals()
    c_m = property(**c_m())

    def r_m():
        doc = "Membrane resistance and corrects capacity."

        def fget(self):
            return self._r_m

        def fset(self, value):
            self._r_m = value
            self._c_m = self.tau_m / value
        return locals()
    r_m = property(**r_m())

    def set_default_constants(self):
        """Sets default constants that are used in simulation of a neuron.

        Sets membrane, potential constants, refractory period. Called on
        __init__(self). Membrane capacity is not used: R_m * C_m = tau_m.
        """
        self.tau_m = 30.
        self.r_m = 1.
        self.tau_ref = 3.
        self.V_rest = 0.
        self.V_reset = 14.2
        self.V_th = 15.

    def flush(self):
        """Flushes saved data from a neuron.

        Flushes spike array. Prints a message if verbose.
        """
        self.spikes = []
        if self.verbose:
            print 'Neuron was flushed.'

    def reset(self):
        """Resets changable variables for the neuron.

        Sets time to 0., sets spike time to low value. Sets V to resting value.
        Prints a message if verbose.
        """
        self.V = self.V_rest
        self.time = 0.
        self.spike_time = - 2. * self.tau_ref - 1.
        if self.verbose:
            print 'Neuron was reset.'

    def name(self):
        """Returns some string to define class of neuron."""
        return 'liafneu'

    # V
    def _V_right_side(self, I, V=None):
        if V is None:
            V = self.V
        return (-(V - self.V_rest) + I * self.r_m) / self.tau_m

    # Solve steps
    def _step_euler(self, I):
        self.V += self.dt * self._V_right_side(I)

    def _step_runge_kutta4(self, I):
        k1_V = self._V_right_side(I)
        k2_V = self._V_right_side(I, V=self.V + self.dt * k1_V / 2.)
        k3_V = self._V_right_side(I, V=self.V + self.dt * k2_V / 2.)
        k4_V = self._V_right_side(I, V=self.V + self.dt * k3_V)
        self.V += self.dt / 6. * (k1_V + 2.*k2_V + 2.*k3_V + k4_V)

    def step(self, I=0.):
        """Propagates neuron dynamics forward for dt.

        Args:
            I: Optional variable, pA. Adds some incoming current to I_stim
            for the step.

        Returns:
            Boolean True if neuron spiked, False if did not.
        """
        self.time += self.dt
        if not self.spiking():
            self._step(I + self.I_stim)
            if self.V >= self.V_th:
                self.force_spike()
        return self.time == self.spike_time

    def spiking(self):
        """Returns True if neuron is in refractory period."""
        return not self.time >= self.spike_time + self.tau_ref

    def force_spike(self):
        """Forces neuron to spike and stay refractory for the period.

        Prints a message if verbose.
        """
        self.V = self.V_reset
        self.spikes.append(self.time)
        self.spike_time = self.time
        if self.verbose:
            print 'At', self.spike_time, 'liaf neuron spiked.'
