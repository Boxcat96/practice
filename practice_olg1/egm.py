"""
Purpose:
Collect functions that are used in computing policy function.
@author: Tomoaki Yamada
"""


def end_grid_method(na, jr, jf, aprime, rent, wage, tax_ss,
                    rep_rate, beq, ave_L, beta, gamma, eta, surv, amax, amin):
    """
    Compute policy functions using endogenous gridpoint method.
    For more details, see Carroll (2006,EL).
    """

    import numpy as np
    import matplotlib.pyplot as plt

    # output
    policy = np.zeros([na, jf])

    # local variables
    con = np.zeros([na+1, jf])
    coh = np.zeros([na+1, jf])
    asset = np.zeros([na, jf])

    # consumption function over cash on hand by age
    for ia in range(jf-1, -1, -1):

        if ia == jf-1:

            con[0, ia] = 0.0
            coh[0, ia] = 0.0

            # receive social security
            ss = wage*rep_rate*ave_L

            # cash on hand and consumption
            for i in range(na):
                coh[i+1, ia] = (1.0+rent)*(aprime[i]+beq) + ss
                con[i+1, ia] = coh[i+1, ia]

            # retrieve current financial asset
            for i in range(na):
                asset[i, ia] = aprime[i]

            tmp = coh[:, ia]

            # for debug
            # plt.figure()
            # plt.plot(coh[:, ia], con[:, ia], marker='o', color='blue')
            # plt.grid(True)
            # plt.show()

        elif ia >= jr and ia <= jf-2:

            con[0, ia] = 0.0
            coh[0, ia] = 0.0

            for i in range(na):
                rhs = mv_retire(aprime[i], ia, rent, wage, beq, ave_L,
                                con, coh, na, beta, gamma, rep_rate, surv)

                con[i+1, ia] = rhs**(-1/gamma)
                coh[i+1, ia] = con[i+1, ia] + aprime[i]

            # retrieve current financial asset
            ss = wage*rep_rate*ave_L
            for i in range(na):
                asset[i, ia] = (coh[i+1, ia] - ss)/(1.0+rent) - beq

            # for debug
            # plt.figure()
            # plt.plot(coh[:, ia], con[:, ia], marker='o', color='blue')
            # plt.grid(True)
            # plt.show()

        elif ia <= jr-1:

            con[0, ia] = 0.0
            coh[0, ia] = 0.0

            for i in range(na):
                if ia == jr-1:
                    rhs = mv_retire(aprime[i], ia, rent, wage, beq, ave_L,
                                    con, coh, na, beta, gamma, rep_rate, surv)
                else:
                    rhs = mv_worker(aprime[i], ia, rent, wage, tax_ss, beq,
                                    con, coh, na, beta, gamma, eta, surv)

                con[i+1, ia] = rhs**(-1/gamma)
                coh[i+1, ia] = con[i+1, ia] + aprime[i]

            # retrieve current financial asset
            earning = (1.0-tax_ss)*wage*eta[ia]
            for i in range(na):
                asset[i, ia] = (coh[i+1, ia] - earning)/(1.0+rent) - beq

            # for debug
            # plt.figure()
            # plt.plot(coh[:, ia], con[:, ia], marker='o', color='blue')
            # plt.grid(True)
            # plt.show()

    # policy function over asset
    for ia in range(jf):
        if ia == jf-1:
            policy[:, ia] = 0.0
        else:
            # next period's asset
            for i in range(na):
                if asset[0, ia] > aprime[i]:
                    policy[i, ia] = amin
                elif aprime[i] > asset[na-1, ia]:
                    policy[i, ia] = aprime[na-1] + ((aprime[na-1]-aprime[na-2])/(asset[na-1, ia]-asset[na-2, ia]))*(aprime[i]-asset[na-1, ia])
                else:
                    policy[i, ia] = np.interp(aprime[i], asset[:, ia], aprime)
                # avoid exception
                if policy[i, ia] < amin:
                    policy[i, ia] = amin

    # for debug
    # plt.figure()
    # plt.plot(aprime, policy[:, 0], marker='o', color='blue')
    # plt.grid(True)
    # plt.show()

    return policy


def mv_worker(aprime, age, rent, wage, tax_ss, beq, conf, xgrid, na,
              beta, gamma, eta, surv):
    """
    Right hand side of the Euler quation: worker.
    """

    import numpy as np
    import my_econ_fcn as eco

    # next period's value for each state
    earning = (1.0-tax_ss)*wage*eta[age+1]

    # cash on hand
    coh = (1.0+rent)*(aprime+beq) + earning

    # given cash on hand, compute consumption
    con = consumption_fcn(coh, conf[:, age+1], xgrid[:, age+1], na)

    # marginal utility
    mu = eco.mu_CRRA(con, gamma)

    # GAMMA prime
    vf = surv[age]*beta*(1.0+rent)*mu

    return vf


def mv_retire(aprime, age, rent, wage, beq, ave_L, conf, xgrid, na,
              beta, gamma, rep_rate, surv):
    """
    Right hand side of the Euler quation: retiree.
    """

    import numpy as np
    import my_econ_fcn as eco

    # social security payment
    ss = wage*rep_rate*ave_L

    # cash on hand
    coh = (1.0+rent)*(aprime+beq) + ss

    # given cash on hand, compute consumption
    con = consumption_fcn(coh, conf[:, age+1], xgrid[:, age+1], na)

    # marginal utility
    mu = eco.mu_CRRA(con, gamma)

    # GAMMA prime
    vf = surv[age]*beta*(1.0+rent)*mu

    return vf


def consumption_fcn(coh, conf, xgrid, na):
    """
    Consumption function over cash on hand.
    """

    import numpy as np
    # from scipy.interpolate import interp1d

    # conf = interp1d(xgrid[1:na+1], conf[1:na+1], fill_value='extrapolate')

    if coh <= xgrid[1]:
        # if liquidity constraint binds
        cons = coh
    elif coh > xgrid[na]:
        # if cash on hand is over the maximum grid
        # interp does not "extrapolate" automatically
        # should use interp1d in scipy
        cons = conf[na] + ((conf[na]-conf[na-1])/(xgrid[na]-xgrid[na-1]))*(coh-xgrid[na])
    else:
        # use linear interpolation
        cons = np.interp(coh, xgrid[1:na+1], conf[1:na+1])

    # avoid exception
    if cons > coh:
        cons = coh

    return cons
