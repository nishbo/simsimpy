SimSimPy is a collection of useful functions for simple simulation written in
Python.

It has a simple architecture, easy logic and clear classes. It should not be
used for hardcore calculations and experiments. Package is intended to use for
education in computational neuroscience, simple experiments and testing of
architecture performance.

Depends on:
Python35

Installation:
1. Download repository.
2. Open package directory (the one that contains setup.py) in terminal.
3. Type 'python setup.py install'.

Package simsimpy contains following modules:
1. random
Contains a few functions expanding random number generator capabilities.
2. other
A few useful functions.
3. intstep
Integration step module.
4. optimzie
Contains a series of optimization functions. Requires scipy.

Archive containes deprecated and not supported (although completely working)
functions:
1. neuron
Contains models of neurons. Now leaky integrate-and-fire and Hodgkin-Huxley
models are included.
2. node
Contains Node and SimpleSynapse classes. Defines a basic node of network.
3. synapse
Contains various models of synaptic plasticity. Short-term Tsodyks-Markram and
long-term STDP are included.
For more information use help. For example of usage see example.py script.
