from __future__ import print_function
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot

print(sm.datasets.sunspots.NOTE)
dta = sm.datasets.sunspots.load_pandas().data
#print(type(dta))
dta.index = pd.Index(sm.tsa.datetools.dates_from_range('1700', '2008'))

del dta["YEAR"]
print(dta)
dta.plot(figsize=(12,8))

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(dta.values.squeeze(), lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(dta, lags=40, ax=ax2)
plt.show()


arma_mod20 = sm.tsa.ARMA(dta, (2,0)).fit()
print(arma_mod20.params)

arma_mod30 = sm.tsa.ARMA(dta, (3,0)).fit()
print(arma_mod30.params)

print(arma_mod20.aic, arma_mod20.bic, arma_mod20.hqic)
print(arma_mod30.aic, arma_mod30.bic, arma_mod30.hqic)

print(sm.stats.durbin_watson(arma_mod30.resid.values))

fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
ax = arma_mod30.resid.plot(ax=ax);
resid = arma_mod30.resid
stats.normaltest(resid)
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
fig = qqplot(resid, line='q', ax=ax, fit=True)
plt.show()


fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(resid, lags=40, ax=ax2)

plt.show()

r,q,p = sm.tsa.acf(resid.values.squeeze(), qstat=True)
data = np.c_[range(1,41), r[1:], q, p]
table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
print(table.set_index('lag'))



predict_sunspots = arma_mod30.predict('1990', '2012', dynamic=True)
print(predict_sunspots)


fig, ax = plt.subplots(figsize=(12, 8))
ax = dta.ix['1950':].plot(ax=ax)
fig = arma_mod30.plot_predict('1990', '2012', dynamic=True, ax=ax, plot_insample=False)


def mean_forecast_err(y, yhat):
    return y.sub(yhat).mean()


print(mean_forecast_err(dta.SUNACTIVITY, predict_sunspots))
plt.show()