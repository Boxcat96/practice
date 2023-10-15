"""
Purpose:
Collect functions for generating grid points (evaluation points).
1. grid_exp1
2. grid_exp2
3. grid_exp3
4. grid_mmv
@author: Tomoaki Yamada
"""


def grid_exp1(xmin, xmax, num_grid):
    """
    Exponential grid: For details, see Carroll (2012).
    params: xmin: minimum gridpoint.
    params: xmax: maximum gridpoint.
    params: num_grid: the number of gridpoints
    return: grid: evaluation points.
    """

    import numpy as np

    dmax = np.log(xmax + 1.0)
    mesh = np.linspace(xmin, dmax, num_grid)
    grid = np.exp(mesh) - 1.0

    return grid


def grid_exp2(xmin, xmax, num_grid):
    """
    double exponential grid: For details, see Carroll (2012).
    params: xmin: minimum gridpoint.
    params: xmax: maximum gridpoint.
    params: num_grid: the number of gridpoints
    return: grid: evaluation points.
    """

    import numpy as np

    dmax = np.log(np.log(xmax + 1.0) + 1.0)
    mesh = np.linspace(xmin, dmax, num_grid)
    grid = np.exp(np.exp(mesh) - 1.0) - 1.0

    return grid


def grid_exp3(xmin, xmax, num_grid):
    """
    triple exponential grid: For details, see Carroll (2012).
    params: xmin: minimum gridpoint.
    params: xmax: maximum gridpoint.
    params: num_grid: the number of gridpoints
    return: grid: evaluation points.
    """

    import numpy as np

    dmax = np.log(np.log(np.log(xmax + 1.0) + 1.0) + 1.0)
    mesh = np.linspace(xmin, dmax, num_grid)
    grid = np.exp(np.exp(np.exp(mesh) - 1.0) - 1.0) - 1.0

    return grid


def grid_mmv(xmin, xmax, theta, num_grid):
    """
    Generate grids proposed in Maliar, Maliar and Valli (2010,JEDC).
    params: xmin: minimum gridpoint.
    params: xmax: maximum gridpoint.
    params: theta: coefficient for concentration of gridpoint.
    params: num_grid: the number of gridpoints
    return: grid: evaluation points.
    """

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
