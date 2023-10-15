"""
Purpose:
Demonstrate interpolation method.
@author: Tomoaki Yamada
"""

import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

# %% true function

x = np.linspace(0, 5, 101)
y = -2*(x-3)**2 + 20.0

plt.figure()
plt.plot(x, y, color='blue')
plt.title("true function")
plt.xlabel("x")
plt.ylabel("y")
plt.xlim(0, 5)
plt.grid(True)
plt.savefig('Fig2_true_fcn.pdf')
plt.show()

# %% example

xapp = np.zeros(6)
yapp = np.zeros(6)

xapp[0] = x[0]
xapp[1] = x[20]
xapp[2] = x[40]
xapp[3] = x[60]
xapp[4] = x[80]
xapp[5] = x[100]

yapp[0] = y[0]
yapp[1] = y[20]
yapp[2] = y[40]
yapp[3] = y[60]
yapp[4] = y[80]
yapp[5] = y[100]

plt.figure()
plt.plot(xapp, yapp, marker='o', color='blue')
plt.title("limited points to be interpolated")
plt.xlabel("x")
plt.ylabel("y")
plt.xlim(0, 5)
plt.grid(True)
plt.savefig('Fig2_data.pdf')
plt.show()

# %% interpolation using scipy

xmin = 0.0
xmax = 5.0
nx = 101

xgrid = np.linspace(xmin, xmax, nx)
y_ln = np.zeros(nx)
y_cs = np.zeros(nx)

for i in range(nx):
    # linear interpolation
    f1 = interpolate.interp1d(xapp, yapp)
    y_ln[i] = f1(xgrid[i])
    # cubic spline interpolation
    f2 = interpolate.interp1d(xapp, yapp, kind="cubic")
    y_cs[i] = f2(xgrid[i])

ytrue = -2*(xgrid-3)**2 + 20

plt.figure()
plt.plot(xgrid, y_ln, color='blue')
plt.title("linear interpolation")
plt.xlabel("x")
plt.ylabel("y")
plt.xlim(0, 5)
plt.grid(True)
plt.savefig('Fig2_interp_linear.pdf')
plt.show()

plt.figure()
plt.plot(xgrid, y_cs, color='blue')
plt.title("cubic spline interpolation")
plt.xlabel("x")
plt.ylabel("y")
plt.xlim(0, 5)
plt.grid(True)
plt.savefig('Fig2_interp_cubic.pdf')
plt.show()

plt.figure()
plt.plot(xgrid, y_ln, linestyle='solid', color='blue', label='linear')
plt.plot(xgrid, y_cs, linestyle='dashed', color='red', label='cubic spline')
plt.plot(xgrid, ytrue, linestyle='dotted', color='green', label='true')
plt.title("comparison of interpolation")
plt.xlabel("x")
plt.ylabel("y")
plt.xlim(0, 5)
plt.grid(True)
plt.legend(loc='lower right')
plt.savefig('Fig2_interp_comp.pdf')
plt.show()
