%matplotlib notebook
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('fivethirtyeight')

A=2
B=1
C=0.3

def f(k, l):
    return k**(1/3) * l**(2/3)

k = np.arange(0, 100, 2.5)
l = np.arange(0, 100, 2.5)

K, L = np.meshgrid(k, l)
Y1 = A*f(K, L)
Y2 = B*f(K, L)
Y3 = C*f(K, L)

fig = plt.figure()
ax = Axes3D(fig)

ax.set_xlabel("K")
ax.set_ylabel("L")
ax.set_zlabel("Y")

ax.plot_wireframe(K, L, Y1, color='blue',linewidth=0.3) 
ax.plot_wireframe(K, L, Y2,linewidth=0.3)
ax.plot_wireframe(K, L, Y3, color='cyan',linewidth=0.3) 
plt.show()

# x軸の目盛設定
ax.set_xticks([ 0, 50, 100])

# y軸の目盛設定
ax.set_yticks([0, 50, 100])

# z軸の目盛設定
ax.set_zticks([0, 50, 100, 150, 200])

plt.rcParams['font.family'] ='sans-serif'
plt.rcParams["font.size"] = 12

plt.tick_params(labelbottom=False,
                labelleft=False,
                labelright=False,
                labeltop=False)

ax.set_xlabel("K", size = 16, weight = "light")
ax.set_ylabel("L", size = 16, weight = "light")
ax.set_zlabel("Y", size = 16, weight = "light")
fig.subplots_adjust(bottom=0.1)

plt.savefig("fy10", transparent=True, dpi=600) # default: False
