class Node(object):
    """Node that has a neuron and a number of simple synapses.

    Node is a basis of network. In this simulator a node will be a neuron with
    incoming simple synapses that define incoming current. Node provides a
    simple interface for a neuron and its incoming synapses. Does not add
    anything complex. Enables simultaneous access and set for:
        dt
        time
        reset()
        g
        V
        spikes
    as properties.

    Attributes:
        neuron: Neuron model for this node. Has to have attributes: dt,
          step(I), time, reset().
        synapses: List of incoming synapses (synapse types). Have to have dt,
          step(weight), time, reset().
    """

    def __init__(self, neuron, synapses):
        """Inits node with neuron and synapses."""
        self._I_syn = []
        self.neuron = neuron
        self.synapses = []
        self._synapse_step = []
        for synapse in synapses:
            self.add_synapse(synapse)
        self.dt = self.neuron.dt

    def add_synapse(self, synapse):
        """Adds an incoming synapse."""
        self.synapses.append(synapse)
        if synapse.base[0] == 'current':
            self._synapse_step.append(self._current_synapse_step)
        elif synapse.base[0] == 'conductance':
            self._synapse_step.append(self._conductance_synapse_step)
        self._I_syn.append(0.)

    def _current_synapse_step(self, synapse, weight):
        return synapse.step(weight) * synapse.base[1]

    def _conductance_synapse_step(self, synapse, weight):
        return synapse.step(weight) * (synapse.base[1] - self.V)

    def step(self, synapse_weights):
        """Propagates dynamics of neuron and synapses.

        Args:
            synapse_weights: List of weights for list of synapses.

        Raises:
            IndexError: An error occurs if list provided is shorter then list
              of synapses.
        """
        for i, synapse in enumerate(self.synapses):
            self._I_syn[i] = self._synapse_step[i](synapse, synapse_weights[i])
        return self.neuron.step(sum(self._I_syn))

    def reset(self):
        self.neuron.reset()
        for synapse in self.synapses:
            synapse.reset()

    def g():
        doc = "Array of all synaptic conductances."

        def fget(self):
            return [syn.g[0] for syn in self.synapses]

        def fset(self, value):
            for i, syn in enumerate(self.synapses):
                syn.g[0] = value[i]
        return locals()
    g = property(**g())

    def V():
        doc = "Potential of the neuron."

        def fget(self):
            return self.neuron.V

        def fset(self, value):
            self.neuron.V = value
        return locals()
    V = property(**V())

    def I_stim():
        doc = "Stimulation current of the neuron."

        def fget(self):
            return self.neuron.I_stim

        def fset(self, value):
            self.neuron.I_stim = value
        return locals()
    I_stim = property(**I_stim())

    def spikes():
        doc = "Spikes of neuron."

        def fget(self):
            return self.neuron.spikes

        def fset(self, value):
            self.neuron.spikes = value
        return locals()
    spikes = property(**spikes())

    def time():
        doc = "Time of the node."

        def fget(self):
            return self.neuron.time

        def fset(self, value):
            self.neuron.time = value
            for syn in self.synapses:
                syn.time = value
        return locals()
    time = property(**time())

    def dt():
        doc = "Time step of the node."

        def fget(self):
            return self.neuron.dt

        def fset(self, value):
            self.neuron.dt = value
            for syn in self.synapses:
                syn.dt = value
        return locals()
    dt = property(**dt())

    def I_syn():
        doc = "Current synaptic current."

        def fget(self):
            return [i for i in self._I_syn]
        return locals()
    I_syn = property(**I_syn())
