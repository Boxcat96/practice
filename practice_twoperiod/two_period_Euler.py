"""
Purpose:
Solve two period model using nonlinear equation solver.
@author: Tomoaki Yamada
"""

import time
import numpy as np
import matplotlib.pyplot as plt
import my_econ_fcn as mef
from scipy.optimize import fsolve

start = time.time()

# calibration: preference
beta = 0.985**30  # discount factor
gamma = 2.0       # relative risk aversion

# calibration: interest rate
rent = 1.025**30-1.0  # net rate of return

# calibration: labor income
y1 = 1.0  # labor income at t1
y2 = 0.5  # labor income at t2

# parameters
na = int(11)  # # of grid at t1
a1_max = 1.0  # max of asset holding at t1
a1_min = 0.0  # min of asset holding at t1

a2_max = 1.0  # max of asset holding at t2
a2_min = 0.0  # min of asset holding at t2

print("")
print("-+-+-+- solve two period model using nonlinear equation solver -+-+-+-")

# discretize grid
grid_a1 = np.linspace(a1_min, a1_max, na)

# %% use nonlinear equation solver

pol_a2 = np.zeros(na)

for i in range(na):
    arg = (y1, y2, grid_a1[i], beta, gamma, rent, )
    pol_a2[i] = fsolve(mef.resid_two_period, [0.0], args=arg)

elapsed_time = time.time() - start

print('-+- computation time -+-')
print(elapsed_time)

# %% plot figure

plt.figure()
plt.plot(grid_a1, pol_a2, marker='o', color='blue', label='policy')
plt.plot(grid_a1, grid_a1, linestyle='dotted', color='black', label='45-degree')
plt.title("approximated policy function")
plt.xlabel("current asset")
plt.ylabel("next asset")
plt.grid(True)
plt.savefig('Fig2_optimization.pdf')
plt.show()

# closed-form solution

coef1 = (beta*(1+rent))**(-1/gamma)
coef2 = coef1*(1+rent)
a_cfs = (y1 + grid_a1 - coef1*y2) / (1+coef2)

plt.figure()
plt.plot(grid_a1, a_cfs, marker='o', color='blue', label='policy')
plt.plot(grid_a1, grid_a1, linestyle='dotted', color='black', label='45-degree')
plt.title("analytical policy function")
plt.xlabel("current asset")
plt.ylabel("next asset")
plt.grid(True)
plt.savefig('Fig2_closed_form.pdf')
plt.show()
