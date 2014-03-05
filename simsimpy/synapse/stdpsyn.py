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
        exc: Multiplier of output. Change for excitatory/inhibitory synapses.
        last_presynaptic_spike, last_postsynaptic_spike: Read names of
          attributes again.
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
        self.exc = 1.
        self.reset()

    def reset(self):
        """Sets last_presynaptic_spike and last_postsynaptic_spike to -1000."""
        self.last_presynaptic_spike = -1000.
        self.last_postsynaptic_spike = -1000.

    def presynaptic_spike(self, time):
        """Processes presynaptic spike.

        Args:
            time: Time of the arriving of spike to the synapse.

        Returns:
            Weight of the synapse after processing multiplied by its
            excitatory/inhibitory value. E.g. -32.2 for inhibitory synapse with
            weight of 32.2.
        """
        self.last_presynaptic_spike = time
        if self.w_minus > 0.:
            h = self.last_postsynaptic_spike - self.last_presynaptic_spike
            if -self.working_time_window[1] <=h<= -self.working_time_window[0]:
                self.weight = max(
                    self.weight_min,
                    self.weight - self.w_minus * math.exp(h / self.tau_minus))
        return self.exc * self.weight

    def postsynaptic_spike(self, time):
        """Processes postsynaptic spike.

        Args:
            time: Time of the excitation of postsynaptic neuron.

        Returns:
            Weight of the synapse after processing multiplied by its
            excitatory/inhibitory value. E.g. -32.2 for inhibitory synapse with
            weight of 32.2.
        """
        self.last_postsynaptic_spike = time
        if self.w_plus > 0.:
            h = self.last_postsynaptic_spike - self.last_presynaptic_spike
            if self.working_time_window[0] <= h <= self.working_time_window[1]:
                self.weight = min(
                    self.weight_max,
                    self.weight + self.w_plus * math.exp(-h / self.tau_plus))
        return self.exc * self.weight
