"""
Purpose:
Compute CRRA utility function and marginal utility function.
@author: Tomoaki Yamada
"""


# CRRA utility function
def CRRA(cons, gamma):

    import math

    if not gamma == 1:
        util = cons**(1.0-gamma)/(1.0-gamma)
    else:
        util = math.log(cons)

    return util


# marginal utility function
def mu_CRRA(cons, gamma):

    mu = cons**-gamma

    return mu
