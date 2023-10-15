"""
Purpose:

Generate grid points (evaluation points).
The grids are spaced uniformly or exponentially.

1. grid_exp
2. grid_double_exp
3. grid_triple_exp
4. grid_mmv

@author: Tomoaki Yamada
"""


# %% exponential grid: Carroll (2012)
def grid_exp1(xmin, xmax, num_grid):

    import numpy as np

    dmax = np.log(xmax + 1.0)
    mesh = np.linspace(xmin, dmax, num_grid)
    grid = np.exp(mesh) - 1.0

    return grid


# %% double exponential grid: Carroll (2012)
def grid_exp2(xmin, xmax, num_grid):

    import numpy as np

    dmax = np.log(np.log(xmax + 1.0) + 1.0)
    mesh = np.linspace(xmin, dmax, num_grid)
    grid = np.exp(np.exp(mesh) - 1.0) - 1.0

    return grid


# %% trible exponential grid: Carroll (2012)
def grid_exp3(xmin, xmax, num_grid):

    import numpy as np

    dmax = np.log(np.log(np.log(xmax + 1.0) + 1.0) + 1.0)
    mesh = np.linspace(xmin, dmax, num_grid)
    grid = np.exp(np.exp(np.exp(mesh) - 1.0) - 1.0) - 1.0

    return grid


# %% grid by Maliar, Maliar and Valli (2010,JEDC)
def grid_mmv(xmin, xmax, theta, num_grid):

    import numpy as np

    # Equation (7) in Maliar et al. (2010,JEDC)
    tmp = np.empty(num_grid)
    for i in range(num_grid):
        tmp[i] = (float(i)/float(num_grid-1))**theta * xmax

    # adjust to [xmin,xmax]
    grid = np.empty(num_grid)
    grid[0] = xmin
    for i in range(1, num_grid, 1):
        grid[i] = grid[i-1] + (tmp[i]-tmp[i-1]) / xmax*(xmax-xmin)

    return grid
