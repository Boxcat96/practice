#%%
import pandas as pd
import statsmodels.api as sm
import pandas_datareader.data as pdr
import datetime
import seaborn as sns
import pandas as pd
#%%
########################################
#2004-2019(JP)-EPIを含まないバージョン
########################################
df = pd.read_csv("C:/test/2107riron/0811/JPdata.csv")
df.head()
# %%
from statsmodels.tsa.api import VAR
data = df.loc[:,  ['y','pi']]
data.head()
# %%
model = VAR(data)
lag_length = model.select_order(maxlags = 12)
lag_length.summary()
# %%
results=model.fit(3)
GrangerTest=results.test_causality('y', 'pi', kind='f',signif=0.1)
GrangerTest.summary()
# %%
irf=results.irf(periods=28)
irf.plot(orth=True,signif=0.1)
# %%
########################################
#2004-2019(JP)-EPIを含めたバージョン
########################################
from statsmodels.tsa.api import VAR
data = df.loc[:,  ['y','pi','epi']]
data.head()
# %%
model = VAR(data)
lag_length = model.select_order(maxlags = 12)
lag_length.summary()
# %%
results=model.fit(3)
GrangerTest=results.test_causality('y', 'pi', kind='f',signif=0.1)
GrangerTest.summary()
# %%
irf=results.irf(periods=28)
irf.plot(orth=True,signif=0.1)

# %%
########################################
#2004-2019(JP)-EPI, GPIを含めたバージョン
########################################
from statsmodels.tsa.api import VAR
data = df.loc[:,  ['y','gpi','pi','epi']]
data.head()
# %%
model = VAR(data)
lag_length = model.select_order(maxlags = 6)
lag_length.summary()
# %%
results=model.fit(2)
GrangerTest=results.test_causality('y', 'pi', kind='f',signif=0.1)
GrangerTest.summary()
# %%
irf=results.irf(periods=28)
irf.plot(orth=True,signif=0.1)
# %%
