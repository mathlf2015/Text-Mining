import pandas as pd
from pandas import DataFrame
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
df = pd.read_csv('E:/mydata/tianchi_wanyiyun/all_feature.csv')
#print(df.columns[0:20])
#print(df[df.columns[0:3]])
feature = df['8fb3cef29f2c266af4c9ecef3b780e97']
#feature = df[df.columns[0:3]]
dta=DataFrame(feature)
dta.index = pd.Index(pd.date_range('3/1/2015','30/8/2015'))
#print(dta)
dta.columns = ['play']
mod = sm.tsa.statespace.SARIMAX(df.play, trend='n', order=(2,1,0), seasonal_order=(1,1,1,30),)
results = mod.fit()
#print(results.predict(1))
print(results.predict(183,243,dynamic= True)[-60:])