"""
Purpose:
Plot even and uneven grids.
@author: Tomoaki Yamada
"""

import numpy as np
import generate_grid as gg
import matplotlib.pyplot as plt

# %% parameters
na = 11   # # of grid
amax = 1.0  # max of asset holding
amin = 0.0  # min of asset holding

# %% discretized grid

print("")
print("-+- make grid -+-")

print("amin  amax  na   ")
print([amin, amax, na])
print(" ")

# uniform grid
a_grid0 = np.linspace(amin, amax, na)

for i in range(na):
    print([a_grid0[i]])

# exponential grid
a_grid1 = gg.grid_exp1(amin, amax, na)

# double exponential grid
a_grid2 = gg.grid_exp2(amin, amax, na)

# triple exponential grid
a_grid3 = gg.grid_exp3(amin, amax, na)

# Maliar et al. (2010)'s approximation method
theta = 2.0
a_grid4 = gg.grid_mmv(amin, amax, theta, na)

theta = 4.0
a_grid5 = gg.grid_mmv(amin, amax, theta, na)

# %% plot figure

# x-axis
xaxis = np.linspace(1, 11, 11)

plt.figure()
plt.plot(xaxis, a_grid0, marker='o', color='blue', label='even')
plt.plot(xaxis, a_grid1, linestyle='dotted', marker='s', color='red', label='exp')
plt.xlabel("grid number")
plt.ylabel("value of grid")
plt.legend(loc='upper left')
plt.grid(True)
plt.savefig('Fig2_grid1.pdf')
plt.show()

plt.figure()
plt.plot(xaxis, a_grid4, marker='o', color='blue', label='$theta=2$')
plt.plot(xaxis, a_grid5, marker='s', color='red', label='$theta=4$')
plt.plot(xaxis, a_grid0, linestyle='dotted', color='black', label='45-degree')
plt.xlabel("grid number")
plt.ylabel("value of grid")
plt.legend(loc='upper left')
plt.grid(True)
plt.savefig('Fig2_grid2.pdf')
plt.show()
