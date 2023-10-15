"""
Purpose:
Solve a life cycle model.
@author: Tomoaki Yamada
"""

import time
import numpy as np
import generate_grid as gg
import my_econ_fcn as eco
import demographics
import egm
import law_of_motion
import matplotlib.pyplot as plt

start = time.time()

print("")
print("-+-+-+- Solving a life cycle model -+-+-+-")
print("")

# %% calibration: preference
beta = 0.98  # discount factor
gamma = 2  # relative risk aversion

# calibration: production
tfp = 1.0  # TFP level
alpha = 0.377  # capital share
delta = 0.08  # depreciation rate

# calibration: life cycle
jr = 46  # household works for 46 periods: 20-65
jf = 81  # household lives for 81 periods: 20-100

# calibration: social security system
rep_rate = 0.5  # replacement rate

# calibration: population growth rate
popn = 0.0036  # match replacement rate

# other parameters
na = 101  # #grid for financial asset
amax = 20.0  # max of asset holding
amin = 0.0  # min of asset holding

# variables
surv = np.zeros(jf)  # survival probability
mu = np.zeros(jf)  # population distribution
eta = np.zeros(jr)  # age-efficiency profile

K_age = np.zeros(jf)
K_mean_age = np.zeros(jf)
C_mean_age = np.zeros(jf)
Y_mean_age = np.zeros(jf)

# policy function
policy = np.zeros([na, jf])

# tolerance of error
iter = 1
maxit = 100
metric = 1.0
toler = 1.0e-005
adj = 0.2

# %% demographics
[surv, mu, frac_ret] = demographics.demog(jr, jf, popn)

# age-efficiency profile
eta = eco.labor_efficienty(jr)

"""
age_grid = np.linspace(20, 65, 46)
plt.figure()
plt.plot(age_grid, eta, color='blue')
plt.title("Age-Efficiency Profile")
plt.xlabel("Age")
plt.ylabel("Labor Efficiency")
plt.xlim(20, 65)
plt.grid(True)
plt.savefig('Fig_efficiency.pdf')
plt.show()
"""

# exponential grid
# aprime = np.linspace(amin, amax, na)
# aprime = gg.grid_exp1(amin, amax, na)
aprime = gg.grid_exp2(amin, amax, na)
# aprime = gg.grid_exp3(amin, amax, na)

# aggregate labor
L_agg = 0.0
for i in range(jr):
    L_agg = mu[i]*eta[i] + L_agg

# average labor
ave_L = sum(eta)/float(jr)

# initial guess of aggregate capital and labor
K_agg = 3.0
beq = 0.01

# initial guess: factor prices
KoverL = K_agg/L_agg
[rent, wage, KoverY] = eco.factor_price(KoverL, tfp, alpha, delta)

# equilibrium tax rate
tax_ss = eco.govt_budget(wage, eta, ave_L, rep_rate, jr, jf, mu)
print("equilibrium payroll tax rate (%):", tax_ss*100)
print("")

while iter <= maxit and metric > toler:

    print("-------- iteration counter --------")
    print(iter)
    print("capital-output ratio: %f" % KoverY)
    print("interest rate: %f" % float(rent*100))
    print("wage: %f" % wage)

    # given factor prices, compute policy functions
    policy = egm.end_grid_method(na, jr, jf, aprime, rent, wage, tax_ss,
                                 rep_rate, beq, ave_L, beta, gamma, eta, surv,
                                 amax, amin)

    # age profiles
    [K_mean_age, C_mean_age, Y_mean_age] = law_of_motion.lom(policy, jf, jr, na, rent, wage, eta, tax_ss, rep_rate, beq, ave_L, aprime)

    # aggregate capital
    for i in range(jf):
        K_age[i] = mu[i]*K_mean_age[i]

    K_supply = sum(K_age)

    print("capital demand & supply:")
    print(K_agg, K_supply)

    # update accidental bequest
    beq = 0.0
    for i in range(jf-1):
        beq = (1.0-surv[i])*(1.0+rent)*K_age[i+1] + beq

    # iteration error
    metric = abs((K_supply-K_agg)/K_supply)

    print("iteration error: capital (%):")
    print(metric*100)
    print("")

    # update and new factor prices
    K_agg = adj*K_supply + (1.0-adj)*K_agg
    KoverL = K_agg/L_agg

    [rent, wage, KoverY] = eco.factor_price(KoverL, tfp, alpha, delta)
    iter = iter + 1

elapsed_time = time.time() - start

print("-+- computation time -+-")
print(elapsed_time)

# plot figure
age_grid = np.linspace(20, 100, 81)

plt.figure()
plt.plot(age_grid, K_mean_age, color='blue')
plt.title("Asset Profile")
plt.xlabel("Age")
plt.ylabel("Asset")
plt.xlim(20, 100)
plt.ylim(0, 12)
plt.grid(True)
plt.savefig('Fig_asset_profile.pdf')
plt.show()

plt.figure()
plt.plot(age_grid, C_mean_age, color='blue')
plt.title("Consumption Profile")
plt.xlabel("Age")
plt.ylabel("Consumption")
plt.xlim(20, 100)
plt.ylim(0.6, 1.5)
plt.grid(True)
plt.savefig('Fig_consumption_profile.pdf')
plt.show()

age_grid = np.linspace(20, 100, 81)
plt.figure()
plt.plot(age_grid, Y_mean_age, color='blue')
plt.title("Earnings (+ Social Security) Profile")
plt.xlabel("Age")
plt.ylabel("Income")
plt.ylim(0.5, 1.4)
plt.grid(True)
plt.savefig('Fig_income_profile.pdf')
plt.show()
