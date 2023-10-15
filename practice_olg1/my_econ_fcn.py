"""
Purpose:
Collect functions.
@author: Tomoaki Yamada
"""


def CRRA(cons, gamma):
    """
    CRRA utility function.
    :params: cons: consumption level.
    :params: gamma: relative risk aversion.
    :return: util: utility level.
    """

    import math

    if not gamma == 1:
        util = cons**(1-gamma)/(1-gamma)
    else:
        util = math.log(cons)

    return util


def mu_CRRA(cons, gamma):
    """
    Return marginal value of CRRA utility function.
    :params: cons: consumption level.
    :params: gamma: relative risk aversion.
    :return: mu: martinal utility.
    """

    mu = cons**-gamma

    return mu


def factor_price(KoverL, tfp, alpha, delta):
    """
    Given K/L, compute factor prices.
    :params: KoverL: K/L.
    :params: tfp: total factor productivity.
    :params: alpha: capital share.
    :params: delta: depreciation rate.
    :return: rent: interest rate.
    :return: wage: wage.
    :return: KoverY: K/Y.
    """

    # first order conditions
    rent = alpha*tfp*(KoverL**(alpha-1)) - delta
    wage = (1-alpha)*tfp*(KoverL**alpha)
    KoverY = KoverL**(1-alpha)

    return rent, wage, KoverY


def labor_efficienty(jr):
    """
    Age-efficiency profile.
    :params: jr: retirement age.
    :return: eta: age-efficiency profile.
    """

    import numpy as np

    eta = np.zeros(jr)

    eta[0] = 0.5506
    eta[1] = 0.5671
    eta[2] = 0.5867
    eta[3] = 0.6094
    eta[4] = 0.6346
    eta[5] = 0.6623
    eta[6] = 0.6921
    eta[7] = 0.7237
    eta[8] = 0.7569
    eta[9] = 0.7913
    eta[10] = 0.8268
    eta[11] = 0.8629
    eta[12] = 0.8996
    eta[13] = 0.9364
    eta[14] = 0.9730
    eta[15] = 1.0093
    eta[16] = 1.0450
    eta[17] = 1.0797
    eta[18] = 1.1132
    eta[19] = 1.1452
    eta[20] = 1.1754
    eta[21] = 1.2036
    eta[22] = 1.2294
    eta[23] = 1.2527
    eta[24] = 1.2730
    eta[25] = 1.2903
    eta[26] = 1.3041
    eta[27] = 1.3141
    eta[28] = 1.3202
    eta[29] = 1.3221
    eta[30] = 1.3194
    eta[31] = 1.3118
    eta[32] = 1.2992
    eta[33] = 1.2812
    eta[34] = 1.2576
    eta[35] = 1.2280
    eta[36] = 1.1922
    eta[37] = 1.1500
    eta[38] = 1.1010
    eta[39] = 1.0450
    eta[40] = 0.9816
    eta[41] = 0.9107
    eta[42] = 0.8319
    eta[43] = 0.7449
    eta[44] = 0.6496
    eta[45] = 0.5455

    return eta


def govt_budget(wage, eta, ave_L, rep_rate, jr, jf, mu):
    """
    Euilibrium tax rate from government budget constraint.
    :params: wage: wage.
    :params: eta: age-efficiency profile.
    :params: ave_L: average (aggregate) labor.
    :params: rep_rate: replacement rate.
    :params: jr: retirement age.
    :params: jf: maximum age.
    :params: mu: population distribution.
    :return: tax_ss: equilibrium tax rate.
    """

    # total social security benefit
    ss_benefit = 0.0
    for j in range(jr, jf, 1):
        ss_benefit = wage*rep_rate*ave_L*mu[j] + ss_benefit

    # total revenue*tax_rate
    ss_rev = 0.0
    for j in range(jr):
        ss_rev = wage*eta[j]*mu[j] + ss_rev

    # social security tax rate
    tax_ss = ss_benefit/ss_rev

    return tax_ss
