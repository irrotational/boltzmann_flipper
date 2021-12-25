import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import argparse

############################################################################################################
# Argument parsing

parser = argparse.ArgumentParser()

parser.add_argument("-lattice_size",type=int,default=70,help="The size of the square 2D lattice.")
parser.add_argument("-initial_distribution",type=str,default="random",help="""Choose from 'random' or 'uniform'. If 'random', every lattice
	site will be randomly populated with a 0 or 1. If 'uniform', all lattice sites will initially be populated with a 1.""")
parser.add_argument("-timesteps",type=int,default=10000,help="The number of timesteps to run the simulation for.")

args = parser.parse_args()

lattice_size = args.lattice_size
initial_distribution = args.initial_distribution
timesteps = args.timesteps

############################################################################################################
# Create the lattice according to user's chosen starting distribution

if (initial_distribution == 'random'):
	lattice = np.array( [ round(np.random.random()) for i in range(lattice_size**2) ] )
elif (initial_distribution == 'uniform'):
	lattice = np.array( [ 1 for i in range(lattice_size**2) ] )

# Reshape the lattice such that it's square (it's currently just an array of length lattice_size**2)
lattice = lattice.reshape(lattice_size,lattice_size)

# Store a copy of the starting distribution
lattice_start = np.copy(lattice)

############################################################################################################
# Run the simulation

for i in range(timesteps):
	# Randomly pick x,y coordinates to move the energy quantum from and to
	x_init = int(np.random.random() * lattice_size)
	y_init = int(np.random.random() * lattice_size)
	# Now, keep rolling until we find a site that has at least one quantum
	while ( not lattice[x_init,y_init] ):
			x_init = int(np.random.random() * lattice_size)
			y_init = int(np.random.random() * lattice_size)
	x_final = int(np.random.random() * lattice_size)
	y_final = int(np.random.random() * lattice_size)

	# Now, hop the quantum between the sites
	lattice[x_init,y_init] -= 1
	lattice[x_final,y_final] += 1

# Find absolute minima and maxima of the 2D data - This is used to set the shared colorbar
minmin = np.min([np.min(lattice_start), np.min(lattice)])
maxmax = np.max([np.max(lattice_start), np.max(lattice)])

# In preparation for the plots, count the number of quanta on each site

hist_start = [0] * (maxmax+1)
hist_final = [0] * (maxmax+1)

for i in range(lattice_size):
	for j in range(lattice_size):
		hist_start[ lattice_start[i,j] ] += 1
		hist_final[ lattice[i,j] ] += 1

############################################################################################################
# Fitting to the Boltzmann distribution

def boltzmann_distribution(E,C,T):
	""" 'E' is an input variable and 'C' and T' are
		parameters, intended to be fitted below. """

	return C * np.exp(-E/T)

y_data = hist_final
x_data = [i for i in range(len(hist_final))]

# As for initial guesses, 'C' (i.e. the E=0 value) is going to be of order the total number of
# lattice sites (i.e. lattice_size^2), and 'T' (which is in units of kB) is going to be of order 1.

(C_opt,T_opt),(C_cov,T_cov) = curve_fit(boltzmann_distribution,x_data,y_data,p0=[lattice_size**2,1])

############################################################################################################
# Plot starting and finishing distributions

fig,((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)

ax1.set_title("Initial Lattice")
ax2.set_title("Final Lattice")

ax1.plot(hist_start,color='b')
ax1.scatter(x=x_data,y=hist_start,color='r')
ax1.set_xticks(x_data)
ax1.set_xlabel("Number of Sites")
ax1.set_ylabel("Energy Quanta")

ax2.plot(hist_final,color='b')
ax2.scatter(x=x_data,y=hist_final,color='r')
dense = np.linspace(0,10,1000)
exponential_curve = boltzmann_distribution(dense,C_opt,T_opt)
ax2.plot(dense,exponential_curve,linestyle='dashed',color='lime',label='Boltzmann Fit')
ax2.set_xticks(x_data)
ax2.set_xlabel("Number of Sites")
ax2.set_ylabel("Energy Quanta")
ax2.legend()

pos3 = ax3.imshow(lattice_start,vmin=minmin,vmax=maxmax,cmap='jet',label='Starting Lattice')
pos4 = ax4.imshow(lattice,vmin=minmin,vmax=maxmax,cmap='jet',label='Final Lattice')

fig.colorbar(pos3,ax=ax3)
fig.colorbar(pos4,ax=ax4)

plt.tight_layout()
plt.show()





