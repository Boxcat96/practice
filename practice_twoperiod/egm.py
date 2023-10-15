"""
Purpose:
Solve two period model using then endogenous gridpoint method
@author: Tomoaki Yamada
"""

import time
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

start = time.time()

# %% calibration: preference
beta = 0.985**30  # discount factor
gamma = 2.0       # relative risk aversion

# calibration: interest rate
rent = 1.025**30-1.0  # net rate of return

# calibration: labor income
y1 = 1.0  # labor income at t1
y2 = 0.5  # labor income at t2

# parameter settings
na = int(11)  # # of grid at t1
a1_max = 1.0  # max of asset holding at t1
a1_min = 0.0  # min of asset holding at t1

a2_max = 1.0  # max of asset holding at t2
a2_min = 0.0  # min of asset holding at t2

# %% endogenous gridpoint method

print("")
print("-+-+-+- solve two period model using endogenous gridpoint method -+-+-+-")

# discretize grid
a2grid = np.linspace(a2_min, a2_max, na)

# consumption at period 2
c2 = y2 + (1.0+rent)*a2grid

# marginal value: function Gamma
GAM = beta*(1.0+rent)*c2**-gamma

# consumption at period 1: inverse of RHS of Euler eq
c1 = GAM**(-1.0/gamma)

# cash on hand x1 and a1
x1 = c1 + a2grid
a1 = x1 - y1

# %% saving function: a2=g(a1)

a1grid = np.linspace(a1_min, a1_max, na)
a2_policy = np.zeros(na)

# approximation
for i in range(na):
    if a1grid[i] < a1[0]:
        a2_policy[i] = a2_min
    else:
        # use bilinear interpolation or spline
        a2_policy[i] = np.interp(a1grid[i], a1, a2grid)

# consumption ar period 1: c1=f1(a1)
c1_policy = y1 + a1grid - a2_policy

elapsed_time = time.time() - start

print('-+- computation time -+-')
print(elapsed_time)

# %% plot figure

plt.figure()
plt.plot(a1grid, a2_policy, marker='o', color='blue', label='policy')
plt.plot(a1grid, a1grid, linestyle='dotted', color='black', label='45-degree')
plt.title("policy function using EGM")
plt.xlabel("current asset")
plt.ylabel("next asset")
plt.grid(True)
plt.savefig('Fig2_egm.pdf')
plt.show()
