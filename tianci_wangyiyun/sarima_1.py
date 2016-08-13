import numpy as np
import pandas as pd
from scipy.stats import norm
import statsmodels.api as sm
import matplotlib.pyplot as plt
from datetime import datetime
import requests
from io import BytesIO
friedman2 = requests.get('http://www.stata-press.com/data/r12/friedman2.dta').content
# Dataset
raw = pd.read_stata(BytesIO(friedman2))
raw.index = raw.time
data = raw.ix[:'1981']

# Variables
endog = data.ix['1959':, 'consump']
exog = sm.add_constant(data.ix['1959':, 'm2'])
nobs = endog.shape[0]

# Fit the model
print(endog.ix[:'1978-01-01'])
print(exog.ix[:'1978-01-01'])
mod = sm.tsa.statespace.SARIMAX(endog.ix[:'1978-01-01'], exog=exog.ix[:'1978-01-01'], order=(1,0,1))
fit_res = mod.fit()
plt.plot(endog.ix[:'1978-01-01'])
plt.plot( fit_res.predict(40,60,dynamic= True))
plt.show()
print(fit_res.summary())