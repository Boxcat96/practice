"""
Purpose:
Compute demographic structure in Japan.
@author: Tomoaki Yamada
"""


def demog(jr, jf, popn):
    """
    Demographic structure in Japan.
    params: jr: retirement age.
    params: jf: maximum age.
    params: popn: population growth rate.
    return: surv: survival probability from 20 to 100.
    return: mu: population distribution btwn 20 and 100.
    return: frac_ret: fraction of retired.
    """

    import numpy as np
    import matplotlib.pyplot as plt

    surv_0_100 = np.zeros(101)
    surv = np.zeros(jf)
    mu = np.zeros(jf)

    surv_0_100[0] = 0.99723
    surv_0_100[1] = 0.99960
    surv_0_100[2] = 0.99972
    surv_0_100[3] = 0.99980
    surv_0_100[4] = 0.99985
    surv_0_100[5] = 0.99986
    surv_0_100[6] = 0.99987
    surv_0_100[7] = 0.99988
    surv_0_100[8] = 0.99989
    surv_0_100[9] = 0.99991
    surv_0_100[10] = 0.99992
    surv_0_100[11] = 0.99991
    surv_0_100[12] = 0.99990
    surv_0_100[13] = 0.99988
    surv_0_100[14] = 0.99983
    surv_0_100[15] = 0.99977
    surv_0_100[16] = 0.99970
    surv_0_100[17] = 0.99963
    surv_0_100[18] = 0.99956
    surv_0_100[19] = 0.99950
    surv_0_100[20] = 0.99946
    surv_0_100[21] = 0.99943
    surv_0_100[22] = 0.99942
    surv_0_100[23] = 0.99941
    surv_0_100[24] = 0.99940
    surv_0_100[25] = 0.99939
    surv_0_100[26] = 0.99938
    surv_0_100[27] = 0.99936
    surv_0_100[28] = 0.99934
    surv_0_100[29] = 0.99932
    surv_0_100[30] = 0.99929
    surv_0_100[31] = 0.99925
    surv_0_100[32] = 0.99921
    surv_0_100[33] = 0.99917
    surv_0_100[34] = 0.99912
    surv_0_100[35] = 0.99906
    surv_0_100[36] = 0.99900
    surv_0_100[37] = 0.99893
    surv_0_100[38] = 0.99886
    surv_0_100[39] = 0.99876
    surv_0_100[40] = 0.99866
    surv_0_100[41] = 0.99854
    surv_0_100[42] = 0.99842
    surv_0_100[43] = 0.99829
    surv_0_100[44] = 0.99813
    surv_0_100[45] = 0.99795
    surv_0_100[46] = 0.99775
    surv_0_100[47] = 0.99754
    surv_0_100[48] = 0.99733
    surv_0_100[49] = 0.99709
    surv_0_100[50] = 0.99681
    surv_0_100[51] = 0.99647
    surv_0_100[52] = 0.99606
    surv_0_100[53] = 0.99563
    surv_0_100[54] = 0.99518
    surv_0_100[55] = 0.99470
    surv_0_100[56] = 0.99419
    surv_0_100[57] = 0.99364
    surv_0_100[58] = 0.99305
    surv_0_100[59] = 0.99243
    surv_0_100[60] = 0.99182
    surv_0_100[61] = 0.99119
    surv_0_100[62] = 0.99052
    surv_0_100[63] = 0.98980
    surv_0_100[64] = 0.98898
    surv_0_100[65] = 0.98805
    surv_0_100[66] = 0.98696
    surv_0_100[67] = 0.98566
    surv_0_100[68] = 0.98409
    surv_0_100[69] = 0.98227
    surv_0_100[70] = 0.98025
    surv_0_100[71] = 0.97808
    surv_0_100[72] = 0.97577
    surv_0_100[73] = 0.97328
    surv_0_100[74] = 0.97056
    surv_0_100[75] = 0.96758
    surv_0_100[76] = 0.96426
    surv_0_100[77] = 0.96053
    surv_0_100[78] = 0.95629
    surv_0_100[79] = 0.95151
    surv_0_100[80] = 0.94620
    surv_0_100[81] = 0.94033
    surv_0_100[82] = 0.93380
    surv_0_100[83] = 0.92638
    surv_0_100[84] = 0.91798
    surv_0_100[85] = 0.90863
    surv_0_100[86] = 0.89847
    surv_0_100[87] = 0.88774
    surv_0_100[88] = 0.87643
    surv_0_100[89] = 0.86431
    surv_0_100[90] = 0.85135
    surv_0_100[91] = 0.83779
    surv_0_100[92] = 0.82347
    surv_0_100[93] = 0.80821
    surv_0_100[94] = 0.79189
    surv_0_100[95] = 0.77457
    surv_0_100[96] = 0.75698
    surv_0_100[97] = 0.74082
    surv_0_100[98] = 0.72455
    surv_0_100[99] = 0.70625
    surv_0_100[100] = 0.00000

    for i in range(jf):
        surv[i] = surv_0_100[i+20]

    # stationary population distribution
    nu = np.ones(101)

    for i in range(100):
        nu[i+1] = surv_0_100[i]/(1.0+popn)*nu[i]

    for i in range(jf):
        # note: sum(x[1:n]) = x[1] + ... + x[n-1]
        mu[i] = nu[i+20]/sum(nu[20:101])

    # fraction of retired households: 0.2496 as a target
    frac_ret = sum(mu[jr:jf+1])

    print("dependency ratio (%):", frac_ret*100)
    print("")

    """
    age_grid = np.linspace(20, 100, 81)
    plt.figure()
    plt.plot(age_grid, mu*100, color='blue')
    plt.title("Population Distribution")
    plt.xlabel("Age")
    plt.ylabel("Population (%)")
    plt.xlim(20, 100)
    plt.ylim(0, 2)
    plt.grid(True)
    plt.savefig('Fig_population.pdf')
    plt.show()
    """

    return surv, mu, frac_ret
