"""In this example we will create one neuron and some incoming synapses of two
types."""

import random
import pylab
import simsimpy as ssp


def main():
    # First, we set time-length of simulation, time-grid and buffer, where we
    # will save dynamics of potential and synaptic conductance.
    Tmax = 300.  # ms
    time_grid = pylab.arange(0., Tmax, 0.01)
    V = []
    g = []
    # Do not forget to set same time step for time grid and node (neuron and
    # synapses).

    print 'Creating node...'
    # Let's create a leaky integrate-and-fire neuron
    neuron = ssp.neuron.LIAF()
    neuron.I_stim = 10.  # Add some constant background current

    # List of simple synapses, that define dynamics of conductance of synapses.
    # First synapse is default: jumps on spike, second one is alpha-function.
    synapses = [ssp.node.SimpleSynapse(),
                ssp.node.SimpleSynapse([6., 6.])]

    # Combine neuron and synapses into a node.
    node = ssp.node.Node(neuron, synapses)

    print 'Creating synaptic plasticity and input...'
    # Now let's create some plasticity for our synapses and input.
    # Here we will store synapse plasticity, one sub-list for each type of
    # synaptic conductance model.
    synapse_plasticity = [[], []]
    # Here we will store times of spikes, same way as with plasticity.
    synapse_spikes = [[], []]
    for i in xrange(80):  # 90 synapses of first type.
        synapse_plasticity[0].append([
            ssp.synapse.STDP(),  # Long-term plasticity
            ssp.synapse.TM()])  # Short-term plasticity

        # Let's change some synaptic parameters.
        # synapse_plasticity[type_of_conductance][numer_of_synapse][
        #     type_of_synaptic_plasticity]
        synapse_plasticity[0][i][0].weight_max = 20.
        synapse_plasticity[0][i][0].weight = 10.
        synapse_plasticity[0][i][0].w_plus = 3.
        synapse_plasticity[0][i][0].w_minus = 3.105
        # And add a parameter for later use.
        synapse_plasticity[0][i][0].w_start = 10.

        # And here are spikes:
        synapse_spikes[0].append([])
        # We want between 10 and 50 Hz for each synapse:
        for j in xrange(random.randint(int(Tmax*0.001), int(Tmax*0.05))):
            # We round-up the values because we work on time-grid
            synapse_spikes[0][i].append(round(random.uniform(0., Tmax), 2))
    for i in xrange(20):  # 10 synapses of second type.
        # Here we will have only Tsodyks-Markram plasticity
        synapse_plasticity[1].append(ssp.synapse.TM())
        synapse_plasticity[1][i].set_inhibitory()  # Inhibitory
        synapse_plasticity[1][i].shuffle_constants()  # With shuffled constants

        synapse_spikes[1].append([])  # Same input:
        for j in xrange(random.randint(int(Tmax*0.001), int(Tmax*0.05))):
            synapse_spikes[1][i].append(round(random.uniform(0., Tmax), 2))

    print 'Starting the simulation.'
    # Everything is ready, so
    # Let's begin the simulation!
    for t in time_grid:
        weight = [0., 0.]  # Store synaptic spikes here
        for i, syns in enumerate(synapse_plasticity[0]):
            # Extremely slow implementation of finding spikes. Used for clarity
            # of code.
            if t in synapse_spikes[0][i]:
                # We multiply our STDP weight with TM weight. It's a common
                # style in computational NS. But you can put STDP in power of
                # TM if you want to.
                weight[0] += (syns[0].presynaptic_spike(t)
                              * syns[1].presynaptic_spike(t))
        for i, syn in enumerate(synapse_plasticity[1]):
            if t in synapse_spikes[1][i]:
                # Only one plasticity here.
                weight[1] += syn.presynaptic_spike(t)

        # Send accumulated weights of spikes to synapses of the node.
        if node.step(weight):
            # If node (neuron) spiked, send signal to STDP synapses. We can
            # also send signal to TM synapses, but they won't react much
            # anyway.
            for syns in synapse_plasticity[0]:
                syns[0].postsynaptic_spike(t)

        # We can change all parameters on the fly. Here we disable input from
        # 1/3*Tmax to 2/3*Tmax and increase it afterwards.
        if t == Tmax / 3:
            node.neuron.I_stim = 0.
        elif t == 2 * Tmax / 3:
            node.neuron.I_stim = 15.

        # Let's save neuron potential and synaptic conductances.
        V.append(node.neuron.V)
        g.append([node.synapses[0].g[0], node.synapses[1].g[0]])

        # Some info about the progress of the script.
        print 'Finished: %f\r' % (t / Tmax),
    print

    # Let's find out how much weights changed.
    # If weights are set some other way, you will have to use buffers.
    difference = 0.
    for syns in synapse_plasticity[0]:
        difference += abs(syns[0].weight - syns[0].w_start)
    difference /= len(synapse_plasticity[0])
    print 'Weights changed for %f on average.' % difference

    print 'Creating plots...'
    # Create plots
    pylab.figure(1)
    pylab.title('Leaky integrate and fire neuron with some input.')
    pylab.plot(time_grid, V, label='V, mV')
    pylab.plot(time_grid, [i[0] for i in g],
               label='Synapse type 1 conductance')
    pylab.plot(time_grid, [i[1] for i in g],
               label='Synapse type 2 conductance')
    pylab.legend()
    pylab.show()

if __name__ == '__main__':
    print 'Autostart with main() function.'
    main()
