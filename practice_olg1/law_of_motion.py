"""
Purpose:
Compute law of motion.
@author: Tomoaki Yamada
"""


# compute policy function using endogenous gridpoint method
def lom(policy, jf, jr, na, rent, wage, eta, tax_ss, rep_rate, beq, ave_L, aprime):

    import numpy as np
    import matplotlib.pyplot as plt

    # output
    K_age = np.zeros(jf)
    C_age = np.zeros(jf)
    Y_age = np.zeros(jf)

    for age in range(jf):

        if age == 0:

            # initial asset = 0
            K_age[age] = 0.0

            # saving
            K_age[age+1] = np.interp(K_age[age], aprime, policy[:, age])

            # current disposable earnings
            Y_age[age] = (1.0-tax_ss)*wage*eta[age]

            # current consumption
            C_age[age] = (1+rent)*(K_age[age]+beq) + Y_age[age] - K_age[age+1]

        elif age >= 1 and age <= jr-1:

            # saving
            # K_age[age+1] = np.interp(K_age[age], aprime, policy[:, age])
            if K_age[age+1] > aprime[na-1]:
                K_age[age+1] = policy[na-1, age] + ((policy[na-1, age]-policy[na-2, age])/(aprime[na-1]-aprime[na-2]))*(K_age[age]-aprime[na-1])
            else:
                K_age[age+1] = np.interp(K_age[age], aprime, policy[:, age])

            # current disposable earnings
            Y_age[age] = (1.0-tax_ss)*wage*eta[age]

            # current consumption
            C_age[age] = (1+rent)*(K_age[age]+beq) + Y_age[age] - K_age[age+1]

        elif age >= jr and age < jf-1:

            # saving
            # K_age[age+1] = np.interp(K_age[age], aprime, policy[:, age])
            if K_age[age+1] > aprime[na-1]:
                K_age[age+1] = policy[na-1, age] + ((policy[na-1, age]-policy[na-2, age])/(aprime[na-1]-aprime[na-2]))*(K_age[age]-aprime[na-1])
            else:
                K_age[age+1] = np.interp(K_age[age], aprime, policy[:, age])

            # social security
            Y_age[age] = wage*rep_rate*ave_L

            # current consumption
            C_age[age] = (1+rent)*(K_age[age]+beq) + Y_age[age] - K_age[age+1]

        else:

            # social security
            Y_age[age] = wage*rep_rate*ave_L

            # current consumption
            C_age[age] = (1+rent)*(K_age[age]+beq) + Y_age[age]

    # for debug
    """
    age_grid = np.linspace(20, 100, 81)
    plt.figure()
    plt.plot(age_grid, K_age, marker='o', color='blue')
    plt.grid(True)
    plt.show()

    age_grid = np.linspace(20, 100, 81)
    plt.figure()
    plt.plot(age_grid, C_age, marker='o', color='blue')
    plt.grid(True)
    plt.show()
    """

    return K_age, C_age, Y_age
