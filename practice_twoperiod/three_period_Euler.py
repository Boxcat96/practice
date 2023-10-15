"""
Purpose:
Solve three period model using nonlinear equation solver.
@author: Tomoaki Yamada
"""

import time
import numpy as np
import matplotlib.pyplot as plt
import my_econ_fcn as mef
from scipy.optimize import fsolve

start = time.time()

# %% calibration: preference
beta  = 0.985**20  # discount factor
gamma = 2.0        # relative risk aversion

# calibration: interest rate
rent = 1.025**20-1.0  # net rate of return

# calibration: labor income
y1 = 1.0  # labor income at t1
y2 = 1.2  # labor income at t2
y3 = 0.5  # labor income at t3

# calibration: asset
na = int(11)  # # of grid for asset
a1max = 1.0  # max of asset holding at t1
a1min = 0.0  # min of asset holding at t1

a2max = 1.0  # max of asset holding at t2
a2min = 0.0  # borrowing limit

a3max = 1.0  # max of asset holding at t3
a3min = 0.0  # borrowing limit

# %% solve three period model

print("")
print("-+-+-+- solve three period model using nonlinear equation solver -+-+-+-")

# discretize grid
a1grid = np.linspace(a1min, a1max, na)
a2grid = np.linspace(a2min, a2max, na)

# %% solve consumer's problem from period 2 to 3

a3_pol = np.zeros(na)
for i in range(na):
    arg = (y2, y3, a2grid[i], beta, gamma, rent, )
    a3_pol[i] = fsolve(mef.resid_three_period_23, [0.0], args=arg)

c2fcn = y2 + (1+rent)*a2grid - a3_pol

plt.figure()
plt.plot(a2grid, a3_pol, linestyle='solid', marker='o', color='blue', label='policy')
plt.plot(a2grid, a2grid, linestyle='dotted', color='black', label='45-degree')
plt.title("policy function between period 2 and period 3")
plt.xlabel("asset at period 2")
plt.ylabel("asset at period 3")
plt.xlim([a1min,a1max])
plt.grid(True)
plt.savefig('Fig2_three_period2.pdf')
plt.show()

# %% solve consumer's problem from period 1 to 2

a2_pol = np.zeros(na)
for i in range(na):
    arg = (y1, y2, a1grid[i], beta, gamma, rent, a2grid, c2fcn, )
    a2_pol[i] = fsolve(mef.resid_three_period_12, [0.0], args=arg)

c1fcn = y1 + (1+rent)*a1grid - a2_pol

elapsed_time = time.time() - start

print('-+- computation time -+-')
print(elapsed_time)

# %% plot figure

plt.figure()
plt.plot(a1grid, a2_pol, marker='o', color='blue', label='policy')
plt.plot(a1grid, a1grid, linestyle='dotted', color='black', label='45-degree')
plt.title("policy function between period 1 and period 2")
plt.xlabel("asset at period 1")
plt.ylabel("asset at period 2")
plt.xlim([a1min, a1max])
plt.grid(True)
plt.savefig('Fig2_three_period1.pdf')
plt.show()
