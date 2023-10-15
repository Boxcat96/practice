#%%
import pandas as pd
import statsmodels.api as sm
import pandas_datareader.data as pdr
import datetime
import seaborn as sns
import pandas as pd
#%%
########################################
#1978-1996replication(USA)-EPIを含まないバージョン
########################################
df = pd.read_csv("C:/test/2107riron/0811/df_former.csv")
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
#1978-1996replication(USA)-EPIも含めたバージョン
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
#%%
########################################
#1997-2015replication(USA)-EPIを含まないバージョン
########################################
df = pd.read_csv("C:/test/2107riron/0811/df_latter.csv")
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
#%%
########################################
#1997-2015replication(USA)-EPIも含めたバージョン
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
########################################
#1997-2015(US)-EPI, GPIを含めたバージョン
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
