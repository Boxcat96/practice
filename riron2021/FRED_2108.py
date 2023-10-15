#%%
%matplotlib inline
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import pandas_datareader.data as pdr
import datetime
start = datetime.datetime(1983,1,1)
end = datetime.datetime(2019,12,31)
y = pdr.DataReader('GDPC1', 'fred', start, end)
ypot = pdr.DataReader('GDPPOT', 'fred', start, end)
c_obs = pdr.DataReader('A794RX0Q048SBEA', 'fred', start, end)
i_obs = pdr.DataReader('GPDIC1', 'fred', start, end)
w_obs = pdr.DataReader('LES1252881600Q', 'fred', start, end)
n_obs = pdr.DataReader('CIVPART', 'fred', start, end)
pi_obs = pdr.DataReader('DPCERD3Q086SBEA', 'fred', start, end)
epi_obs = pdr.DataReader('MICH', 'fred', start, end)
gpi_obs = pdr.DataReader('CPIFABSL', 'fred', start, end)
r_obs = pdr.DataReader('BOGZ1FL072052006Q', 'fred', start, end)
# %%
#月次データの四半期への変換
epi_obs = epi_obs.resample(rule="Q").mean()
n_obs = n_obs.resample(rule="Q").mean()
gpi_obs = gpi_obs.resample(rule="Q").mean()
#%%
df1 = y.join([ypot, c_obs, i_obs, w_obs, pi_obs, r_obs])
df1["y_obs"] = (df1["GDPC1"]-df1["GDPPOT"])/df1["GDPPOT"]*100
Ccycle, Ctrend = sm.tsa.filters.hpfilter(df1.A794RX0Q048SBEA, 1600)
Wcycle, Wtrend = sm.tsa.filters.hpfilter(df1.LES1252881600Q, 1600)
Icycle, Itrend = sm.tsa.filters.hpfilter(df1.GPDIC1, 1600)

df1["c_obs"] = Ccycle/Ctrend*100
df1["w_obs"] = Wcycle/Wtrend*100
df1["i_obs"] = Icycle/Itrend*100
df1["pi_obs"] = df1["DPCERD3Q086SBEA"]/df1["DPCERD3Q086SBEA"].shift(4)*100-100
df1["r_obs"] =df1["BOGZ1FL072052006Q"] 
df1 = df1[4:]
df1.drop(columns=df1.columns[[0,1, 2,3,4,5,6]])
#%%
PIcycle, PItrend = sm.tsa.filters.hpfilter(df1.pi_obs, 1600)
df1["tau_obs"] =PItrend 
plt.plot(df1["pi_obs"],label="inflation",color ="deepskyblue")
plt.plot(df1["tau_obs"],color ="midnightblue",ls="--",label="trend")
plt.legend()
plt.show()
#%%
df2 = epi_obs.join([gpi_obs, n_obs])
Ncycle, Ntrend = sm.tsa.filters.hpfilter(df2.CIVPART, 1600)
df2["n_obs"] = Ncycle/Ntrend*100
df2["gpi_obs"] =df2["CPIFABSL"]/df2["CPIFABSL"].shift(4)*100-100
df2["epi_obs"]=df2["MICH"]  
df2 = df2[4:]
df2.drop(columns=df2.columns[[0,1,2]])
# %%
############################################
#任意のパスを設定してください。
#df1、df2とUSdataのフォルダは分けてください。
#Time legendが異なるため、ファイルが一度２つに分かれてしまう（要修正）
############################################
df1.to_excel("C:/test/2107riron/0820/datamake/df_1.xlsx")
df2.to_excel("C:/test/2107riron/0820/datamake/df_2.xlsx")
import glob
folder='C:/test/2107riron/0820/datamake/*.xlsx'
lists = []
file_list=glob.glob(folder)
for i in file_list:
    lists.append(pd.read_excel(i))
df = pd.concat(lists, axis=1)
USdata = df.drop(df.columns[[0,1,2,3,4,5,6,7,16,17,18]], axis=1)
USdata.to_excel("C:/test/2107riron/0820/USdata.xlsx", index=False)
#%%
#############################################
#以下は描画
#############################################
plt.plot(df1["pi_obs"],label="inflation",color ="deepskyblue")
plt.plot(df1["tau_obs"],color ="midnightblue",ls="--",label="trend")
plt.plot(df2["epi_obs"],label="expectation",color ="darkorange")
plt.axhline(y=0,color ="black", lw=0.5)
plt.legend(loc = 'lower left')
plt.show()
#%%
plt.plot(df1["pi_obs"],label="inflation",color ="deepskyblue")
plt.plot(df1["tau_obs"],color ="midnightblue",ls="--",label="trend")
plt.plot(df2["gpi_obs"],label="grocery price",color ="darkorange")
plt.axhline(y=0,color ="black", lw=0.5)
plt.legend(loc = 'lower left')
plt.show()
# %%
plt.plot(df1["w_obs"],label="wage",color ="deepskyblue")
plt.plot(df2["n_obs"],label="labor",color ="darkorange")
plt.axhline(y=0,color ="black", lw=0.5)
plt.legend(loc = 'lower left')
plt.show()
# %%
plt.plot(df1["y_obs"],label="GDP gap",color ="deepskyblue")
plt.plot(df1["r_obs"],label="Interest Rate",color ="darkorange")
plt.axhline(y=0,color ="black", lw=0.5)
plt.legend(loc = 'upper right')
plt.show()
#%%
############################################
#4変数VAR（Y, GPI, PI, EPI）
############################################
from statsmodels.tsa.api import VAR
data = df.loc[:,  ['y_obs','gpi_obs','pi_obs','epi_obs']]
data.head()
# %%
model = VAR(data)
lag_length = model.select_order(maxlags = 12)
lag_length.summary()
# %%
results=model.fit(3)
GrangerTest=results.test_causality('gpi_obs', 'epi_obs', kind='f',signif=0.1)
GrangerTest.summary()
# %%
irf=results.irf(periods=40)
irf.plot(orth=True,signif=0.1)
# %%
df1['MODEL'] = 0.5*df1["y_obs"] + 1.5 * df1["pi_obs"]
plt.plot(df1["MODEL"],label="MODEL",color ="deepskyblue")
plt.plot(df1["r_obs"],label="FF RATE",color ="darkorange")
plt.axhline(y=0,color ="black", lw=0.5)
plt.legend(loc = 'lower left')
plt.show()
# %%
