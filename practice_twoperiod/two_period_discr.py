"""
Purpose:
Solve two period model using discretization.
@author: Tomoaki Yamada
"""

import time
import numpy as np
import matplotlib.pyplot as plt
import my_econ_fcn as mef

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
na1 = int(11)  # # of grid at t1
a1_max = 1.0   # max of asset holding at t1
a1_min = 0.0   # min of asset holding at t1

na2 = int(11)  # # of grid at t2
a2_max = 1.0   # max of asset holding at t2
a2_min = 0.0   # min of asset holding at t2

print("")
print("-+- start computing two period model using discretization method -+-")

# %% discretize grid
grid_a2 = np.linspace(a2_min, a2_max, na2)

# utility at period 2

util2 = beta*mef.CRRA(y2+(1.0+rent)*grid_a2, gamma)

# plot utility function
plt.figure()
plt.plot(grid_a2, util2, marker='o')
plt.title("utility function")
plt.xlabel("asset at period 2")
plt.ylabel("utility at period 2")
plt.grid(True)
plt.savefig('Fig2_utility2.pdf')
plt.show()

# %% utility at period 1
grid_a1 = np.linspace(a1_min, a1_max, na1)

util1 = np.empty((na2, na1))

for i in range(na1):
    for j in range(na2):
        cons = y1 + grid_a1[i] - grid_a2[j]
        if cons > 0:
            util1[j, i] = mef.CRRA(cons, gamma)
        else:
            util1[j, i] = -1000.0

plt.figure()
plt.plot(grid_a2, util1[:, 0], marker='o', label='$a_1$=0')
plt.plot(grid_a2, util1[:, 5], marker='s', label='$a_1$=0.5')
plt.plot(grid_a2, util1[:, 10], marker='^', label='$a_1$=1')
plt.title("utility at period 1")
plt.xlabel("saving (choice)")
plt.ylabel("utility")
plt.ylim(-3, 0)
plt.legend(loc='lower left')
plt.grid(True)
plt.savefig('Fig2_utility1.pdf')
plt.show()

# %% lifetime utility

obj = np.empty((na2, na1))

for i in range(na1):
    for j in range(na2):
        cons = y1 + grid_a1[i] - grid_a2[j]
        if cons > 0.0:
            obj[j, i] = mef.CRRA(cons, gamma) + beta*mef.CRRA(y2+(1.0+rent)*grid_a2[j], gamma)
        else:
            obj[j, i] = -1000.0

# %% get policy function

pol = np.empty(na1)

for i in range(na1):
    maxl = np.ndarray.argmax(obj[:, i])
    pol[i] = grid_a2[maxl]

elapsed_time = time.time() - start

print('-+- computation time -+-')
print(elapsed_time)

# %% plot figure

plt.figure()
plt.plot(grid_a2, obj[:, 0], marker='o', label='$a_1$=0')
plt.plot(grid_a2, obj[:, 5], marker='s', label='$a_1$=0.5')
plt.plot(grid_a2, obj[:, 10], marker='^', label='$a_1$=1')
plt.title("life time utility")
plt.xlabel("saving")
plt.ylabel("life time utility")
plt.ylim(-3, 0)
plt.legend(loc='lower left')
plt.grid(True)
plt.savefig('Fig2_utility_max.pdf')
plt.show()

plt.figure()
plt.plot(grid_a1, pol, marker='o', color='blue', label='policy')
plt.plot(grid_a1, grid_a1, linestyle='dotted', color='black', label='45-degree')
plt.title("policy function")
plt.xlabel("current asset")
plt.ylabel("next asset")
plt.grid(True)
plt.savefig('Fig2_pol_discr.pdf')
plt.show()
