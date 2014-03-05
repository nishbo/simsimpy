class Node(object):
    """Node that has a neuron and a number of simple synapses.

    Node is a basis of network. In this simulator a node will be a neuron with
    incoming simple synapses that define incoming current. Node provides a
    simple interface for a neuron and its incoming synapses. Does not add
    anything complex.

    Attributes:
        neuron: Neuron model for this node. Has to have attributes: dt, step(I),
          time, reset().
        synapses: List of incoming synapses (synapse types). Have to have dt,
          step(weight), time, reset().
    """

    def __init__(self, neuron, synapses):
        """Inits node with neuron and synapses."""
        self.neuron = neuron
        self.synapses = synapses
        self.set_dt(self.neuron.dt)

    def step(self, synapse_weights):
        """Propagates dynamics of neuron and synapses.

        Args:
            synapse_weights: List of weights for list of synapses.

        Raises:
            IndexError: An error occurs if list provided is shorter then list of
              synapses.
        """
        I = 0.
        for i, synapse in enumerate(self.synapses):
            I += synapse.step(synapse_weights[i])
        return self.neuron.step(I)

    def set_dt(self, dt):
        self.neuron.dt = dt
        for synapse in self.synapses:
            synapse.dt = dt

    def set_time(self, time):
        self.neuron.time = time
        for synapse in self.synapses:
            synapse.time = time

    def reset(self):
        self.neuron.reset()
        for synapse in self.synapses:
            synapse.reset()