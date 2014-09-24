import math


class STDP(object):
    """STDP synapse plasticity.

    Represents a STDP Hebbian 'learning' rule.
    h = last_postsynaptic_spike - last_presynaptic_spike
    if working_time_window[0] > abs(h) or abs(h) >  working_time_window[1]:
        delta w = 0.
    elif h >= 0.:
        delta w = w_plus * exp(-h / tau_plus)
    else:
        delta w = - w_minus * exp(h / tau_minus)
    w += delta w
    if w > weight_max: w = weight_max
    if w < weight_min: w = weight_min

    Attributes:
        weight: Current weight of this synapse.
        weight_min, weight_max: Allowed minimum and maximum weight.
        tau_plus, tau_minus: Defines length of effect of spike on synapse.
        w_plus, w_minus: How much synapse changes with spike.
        working_time_window: Time window, where STDP has effect.
        last_presynaptic_spike, last_postsynaptic_spike: Read names of
          attributes again.
        spike_pairing = 0: What spike pairing rule should be used. Availaible
          values: 0, 2. Represent types (a) and (c) respectively from
            Abigail Morrison, Markus Diesmann, Wulfram Gerstner. 2008.
            Phenomenological models of synaptic plasticity based on spike
            timing. Biological Cybernetics 98:6, 459-478.
          Figure 7.
    """

    def __init__(self):
        """Inits an STDP synapse with default parameters."""
        self.weight_max = 1.
        self.weight_min = 0.
        self.weight = 0.5
        self.tau_plus = 20.
        self.tau_minus = 20.
        self.w_plus = 0.3
        self.w_minus = 0.3105
        self.working_time_window = [2., 60.]
        self.spike_pairing = 0
        self.reset()

    def reset(self):
        """Sets last_presynaptic_spike and last_postsynaptic_spike to -1000."""
        self.last_presynaptic_spike = -1000.
        self.last_postsynaptic_spike = -1000.

        self._spike_pairing_2_can_pre = True
        self._spike_pairing_2_can_post = True

    def spike_pairing():
        doc = "Type of spike pairing. See STDP help for more info."

        def fget(self):
            return self._spike_pairing

        def fset(self, value):
            if value == 0:
                self.presynaptic_spike = self._presynaptic_spike_0
                self.postsynaptic_spike = self._postsynaptic_spike_0
            elif value == 2:
                self.presynaptic_spike = self._presynaptic_spike_2
                self.postsynaptic_spike = self._postsynaptic_spike_2
            else:
                raise ValueError("Wrong spike pairing type.")
            self._spike_pairing = value
        return locals()
    spike_pairing = property(**spike_pairing())

    def _presynaptic_spike_0(self, time):
        """Processes presynaptic spike according to pairing scheme 0."""
        self.last_presynaptic_spike = time
        if self.w_minus > 0.:
            h = self.last_postsynaptic_spike - self.last_presynaptic_spike
            if (-self.working_time_window[1] <= h
                    <= -self.working_time_window[0]):
                self.weight = max(
                    self.weight_min,
                    self.weight - self.w_minus * math.exp(h / self.tau_minus))
        return self.weight

    def _postsynaptic_spike_0(self, time):
        """Processes postsynaptic spike according to pairing scheme 0."""
        self.last_postsynaptic_spike = time
        if self.w_plus > 0.:
            h = self.last_postsynaptic_spike - self.last_presynaptic_spike
            if self.working_time_window[0] <= h <= self.working_time_window[1]:
                self.weight = min(
                    self.weight_max,
                    self.weight + self.w_plus * math.exp(-h / self.tau_plus))
        return self.weight

    def _presynaptic_spike_2(self, time):
        """Processes presynaptic spike according to pairing scheme 2."""
        self.last_presynaptic_spike = time
        if self.w_minus > 0. and self._spike_pairing_2_can_pre:
            h = self.last_postsynaptic_spike - self.last_presynaptic_spike
            if (-self.working_time_window[1] <= h
                    <= -self.working_time_window[0]):
                self.weight = max(
                    self.weight_min,
                    self.weight - self.w_minus * math.exp(h / self.tau_minus))
            self._spike_pairing_2_can_pre = False
            self._spike_pairing_2_can_post = True
        return self.weight

    def _postsynaptic_spike_2(self, time):
        """Processes postsynaptic spike according to pairing scheme 2."""
        self.last_postsynaptic_spike = time
        if self.w_plus > 0. and self._spike_pairing_2_can_post:
            h = self.last_postsynaptic_spike - self.last_presynaptic_spike
            if self.working_time_window[0] <= h <= self.working_time_window[1]:
                self.weight = min(
                    self.weight_max,
                    self.weight + self.w_plus * math.exp(-h / self.tau_plus))
            self._spike_pairing_2_can_post = False
            self._spike_pairing_2_can_pre = True
        return self.weight

    def presynaptic_spike(self, time):
        """Processes presynaptic spike.

        Args:
            time: Time of the arriving of spike to the synapse.

        Returns:
            Weight of the synapse.
        """
        pass

    def postsynaptic_spike(self, time):
        """Processes postsynaptic spike.

        Args:
            time: Time of the excitation of postsynaptic neuron.

        Returns:
            Weight of the synapse.
        """
        pass
