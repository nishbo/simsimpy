import math
import myerror


class HH(object):
    """Basic three-channel Hodgkin-Huxley neuron.

    Class represents a basic Hodgkin-Huxley neuron as described in the original
    paper: A. Hodgkin and A. Huxley, 'A quantitative description of membrane
    current and its application to conduction and excitation in nerve',
    J. Physiol, 117:500-544, 1952.
    Instance of the class can step with euler or runge-kutta4 method.

    Attributes:
        verbose: A boolean indicating if the neuron will print information
          about itself sometimes, e.g. when reset() or spike occur.
        dt: Length of time step, shen using step() method, ms.
        I_stim: Constant current that is presented to a neuron, muA/cm^2.
        integration_method: String that defines used integration method. Now
          has two possible states: 'euler' and 'rk4'. If wrongly set, raises an
          myerror.Error exception, method does not change.
        g_Na, g_K, g_L: Maximum conductance of Na, K and leakage channels,
          mS/cm^2.
        E_Na, E_K, E_L: Nernst potentials of Na, K and leakage channels, mV.
          Relative to neuron resting potential from paper. Auto-ajust for
          custom set V_rest.
        C_m: Specific membrane capacity of a neuron, muF/cm^2.
        V_rest: Resting potential of a neuron, mV.
        V_th: Threshold potential for spike, mV. When potential crosses this
        value, neuron spikes.
        V_th_end: Threshold potential for the end of spike, mV. Potential has
          to cross this value after spike to be able to spike again.
          NB: V_th_end <= V_th !!!
        V: Current neuron membrane potential, mV.
        m, h, n: Gating variables. For description see paper.
        time: Current time for the neuron, ms.
        spikes: List of spike times of the neuron. Time of spike is defined by
        'time' attribute.
        tau_ref_force: Duration of refractory period of forced spike, ms.
    """

    def __init__(self):
        """Inits Hodgkin-Huxley neuron with default attributes."""
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

    def set_default_constants(self):
        """Sets default constants that are used in simulation of a neuron.

        Sets channel parameters, membrane capacity, potential constants. Called
        on __init__(self).
        """
        self.g_Na = 120.
        self.E_Na = 115.
        self.g_K = 36.
        self.E_K = -12.
        self.g_L = 0.3
        self.E_L = 10.6
        self.C_m = 1.
        self.V_rest = -70.
        self.V_th = 0.
        self.V_th_end = -55.
        self.tau_ref_force = 2.5

    def flush(self):
        """Flushes saved data from a neuron.

        Sets time to 0., flushes spike array. Prints a message if verbose.
        """
        self.time = 0.
        self.spikes = []
        if self.verbose:
            print 'Neuron was flushed.'

    def set_gating_variables(self):
        self.m = self.m_inf()
        self.h = self.h_inf()
        self.n = self.n_inf()

    def reset(self):
        """Resets changable variables for the neuron.

        Sets V to resting value, gating variables too. Prints a message if
        verbose.
        """
        self.V = self.V_rest
        self.set_gating_variables()
        self._already_spiking = False

        if self.verbose:
            print 'Neuron was reset.'

    def name(self):
        """Returns some string to define class of neuron."""
        return 'hhneu'

    # Gating variables:
    # m
    def _am(self, V=None):
        if V is None:
            V = self.V
        if V - self.V_rest == 25.:
            return 1.
        else:
            return (0.1 * (25. - (V - self.V_rest))
                    / (math.exp((25. - (V - self.V_rest)) / 10.) - 1.))

    def _bm(self, V=None):
        if V is None:
            V = self.V
        return 4. * math.exp(-(V - self.V_rest) / 18.)

    def m_inf(self, V=None):
        """Returns resting value for m gating variable with given potential."""
        return self._am(V) / (self._am(V) + self._bm(V))

    def _m_right_side(self, V=None):
        return self._am(V) * (1 - self.m) - self._bm(V) * self.m

    # h
    def _ah(self, V=None):
        if V is None:
            V = self.V
        return 0.07 * math.exp(-(V - self.V_rest) / 20.)

    def _bh(self, V=None):
        if V is None:
            V = self.V
        return 1. / (math.exp((30. - (V - self.V_rest)) / 10.) + 1.)

    def h_inf(self, V=None):
        """Returns resting value for h gating variable with given potential."""
        return self._ah(V) / (self._ah(V) + self._bh(V))

    def _h_right_side(self, V=None):
        return self._ah(V) * (1 - self.h) - self._bh(V) * self.h

    # n
    def _an(self, V=None):
        if V is None:
            V = self.V
        if V - self.V_rest == 10.:
            return 0.1
        else:
            return (0.01 * (10. - (V - self.V_rest))
                    / (math.exp((10. - (V - self.V_rest)) / 10.) - 1.))

    def _bn(self, V=None):
        if V is None:
            V = self.V
        return 0.125 * math.exp(-(V - self.V_rest) / 80.)

    def n_inf(self, V=None):
        """Returns resting value for n gating variable with given potential."""
        return self._an(V) / (self._an(V) + self._bn(V))

    def _n_right_side(self, V=None):
        return self._an(V) * (1 - self.n) - self._bn(V) * self.n

    # V
    def _V_right_side(self, I, V=None):
        if V is None:
            V = self.V
        return (I - self.g_Na*self.m**3*self.h*(V - self.V_rest - self.E_Na)
                  - self.g_K *self.n**4*       (V - self.V_rest - self.E_K)
                  - self.g_L *                 (V - self.V_rest - self.E_L)
                ) / self.C_m

    # Spiking
    def _spiking_test(self):
        if not self._already_spiking and self.V >= self.V_th:
            self._already_spiking = True
        elif self._already_spiking and self.V < self.V_th_end:
            self._already_spiking = False
            self.spikes.append(self.time)
            if self.verbose:
                print 'At', self.time, 'hh neuron spiked.'

    # Solve steps
    def _step_euler(self, I):
        n = self.n + self.dt * self._n_right_side()
        h = self.h + self.dt * self._h_right_side()
        m = self.m + self.dt * self._m_right_side()
        V = self.V + self.dt * self._V_right_side(I)
        [self.n, self.h, self.m, self.V] = [n, h, m, V]

    def _step_runge_kutta4(self, I):
        k1_n = self._n_right_side()
        k1_h = self._h_right_side()
        k1_m = self._m_right_side()
        k1_V = self._V_right_side(I)

        k2_n = self._n_right_side(V=self.V + self.dt * k1_V / 2.)
        k2_m = self._m_right_side(V=self.V + self.dt * k1_V / 2.)
        k2_h = self._h_right_side(V=self.V + self.dt * k1_V / 2.)
        k2_V = self._V_right_side(I, V=self.V + self.dt * k1_V / 2.)

        k3_n = self._n_right_side(V=self.V + self.dt * k2_V / 2.)
        k3_h = self._h_right_side(V=self.V + self.dt * k2_V / 2.)
        k3_m = self._m_right_side(V=self.V + self.dt * k2_V / 2.)
        k3_V = self._V_right_side(I, V=self.V + self.dt * k2_V / 2.)

        k4_n = self._n_right_side(V=self.V + self.dt * k3_V)
        k4_h = self._h_right_side(V=self.V + self.dt * k3_V)
        k4_m = self._m_right_side(V=self.V + self.dt * k3_V)
        k4_V = self._V_right_side(I, V=self.V + self.dt * k3_V)

        n = self.n + self.dt / 6. * (k1_n + 2.*k2_n + 2.*k3_n + k4_n)
        h = self.h + self.dt / 6. * (k1_h + 2.*k2_h + 2.*k3_h + k4_h)
        m = self.m + self.dt / 6. * (k1_m + 2.*k2_m + 2.*k3_m + k4_m)
        V = self.V + self.dt / 6. * (k1_V + 2.*k2_V + 2.*k3_V + k4_V)

        [self.n, self.h, self.m, self.V] = [n, h, m, V]

    def _step_forced_spike(self, I):
        if self.time >= self.spikes[-1] + self.tau_ref_force:
            self.integration_method = self.integration_method

    def step(self, I=0.):
        """Propagates neuron dynamics forward for dt.

        Args:
            I: Optional variable, muA/cm^2. Adds some incoming current to
              I_stim for the step.

        Returns:
            Boolean True if neuron spiked, False if did not.
        """
        self.time += self.dt
        self._step(I + self.I_stim)
        self._spiking_test()

        return bool(len(self.spikes)) and self.time == self.spikes[-1]

    def force_spike(self):
        """Forces neuron to spike. Use with caution.

        Saves spike and forces neuron to ignore everything for tau_ref_force
        period. Neuron is also reset(). Prints a message if verbose.
        """
        self.spikes.append(self.time)
        self._step = self._step_forced_spike
        self.reset()
        if self.verbose:
            print 'At', self.time, 'hh neuron spiked.'
