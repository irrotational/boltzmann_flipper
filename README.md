# boltzmann_flipper
This script will create a square lattice of specified size, with each lattice site initially containing either zero or a single quantum of energy.

The simulation then propagates for a specified number of timesteps (default=10000), and at each timestep, a quantum of energy is randomly transferred from one site to another. After a sufficient number of timesteps has passed, and provided the lattice is large enough (usually even a 25x25 lattice is sufficient), the distribution of lattice quanta will follow a Boltzmann distribution, as required for the equilibrium state of a (U,N,T) ensemble.

To run, simply type:

python3 boltzmann_flipper.py

Which, by default, will randomly populate a 50x50 square lattice and run the simulation for 10000 timesteps, before plotting summary statistics. To control the lattice size, for example, type:

python3 boltzmann_flipper.py -lattice_size 100

Which will do the same, but now for a 100x100 square lattice. To change the starting distribution to a uniform distribution of 1s (instead of randomly 1s and 0s), type:

python3 boltzmann_flipper.py -initial_distribution uniform

Again, the lattice should equilibriate to a Boltzmann distribution provided a sufficient number of timesteps has passed.
