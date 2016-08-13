from __future__ import print_function
import pandas as pd
import statics as sd
from pandas import DataFrame
CURRENT_PATH=sd.CURRENT_PATH
ARTIST_FOLDER=sd.ARTIST_FOLDER
ARTIST=sd.ARTIST
SONGS=sd.SONGS
SONG_P_D_C=sd.SONG_P_D_C
ARTIST_P_D_C=sd.ARTIST_P_D_C
SONG_FAN=sd.SONG_FAN
ARTIST_FAN=sd.ARTIST_FAN
DAYS=sd.DAYS
START_UNIX  =sd.START_UNIX
DAY_SECOND  =sd.DAY_SECOND
START_WEEK=sd.START_WEEK


def get_artist_set(filename):
    df = pd.read_csv(filename)
    df.columns=['song_id','artist_id','ppublish_time','song_init_plays','Language','Gender']
    artist_set = df['artist_id'].unique()
    return  artist_set


artist_set = get_artist_set(ARTIST)
df = pd.read_csv('E:/mydata/tianchi_wanyiyun/all_feature.csv')
#print(df.info())
feature = df.values.T
#print(feature.shape)
dta=DataFrame(feature[0])
#print(dta)


def test_stationarity(timeseries):
    from statsmodels.tsa.stattools import adfuller

    #Determing rolling statistics
    rolmean = timeseries.rolling(center=False,window=7).mean()
    rolstd = timeseries.rolling(center=False,window=7).std()

    #Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()

    #Perform Dickey-Fuller test:
    print ('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)


#######################################################################################################

import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot
#print(pd.date_range('3/1/2015','30/8/2015'))

dta.index = pd.Index(pd.date_range('3/1/2015','30/8/2015'))
dta.columns = ['play']
#dta['play'] = dta.play.apply(lambda x: np.log(x))
#print(dta)
dta.plot(figsize=(12,8))
plt.show()

'''fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(dta, lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(dta, lags=40, ax=ax2)
plt.show()'''

#test_stationarity(dta.play)
#dta['first_difference'] = dta.play - dta.play.shift(1)
#dta['second_diff'] =dta.play - dta.play.shift(2)
#dta['log']= dta.play.apply(lambda x: np.log(x))
#test_stationarity(dta.log)
#print(dta.first_difference[:5])
#print(dta.play - dta.play.shift(2))
#test_stationarity(dta.first_difference.dropna(inplace=False))

#dta['log_first_difference'] = dta.log - dta.log.shift(1)
#test_stationarity(dta.log_first_difference.dropna(inplace=False))


'''fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(dta.log.iloc[1:], lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(dta.log.iloc[1:], lags=40, ax=ax2)
plt.show()'''


'''fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(dta.log_first_difference.dropna(inplace=False), lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(dta.log_first_difference.dropna(inplace=False), lags=40, ax=ax2)
plt.show()'''



from statsmodels.tsa.arima_model import ARIMA
mod = sm.tsa.statespace.SARIMAX(endog=dta.play, trend='t', order=(2,1,0),seasonal_order=(1,1,1,30))

results = mod.fit()
print(results.summary())
dta['pre']=results.predict(1,183)
print(dta)
plt.plot(dta.play[1:])
print( results.predict(183,243,dynamic= True))
plt.plot( results.predict(183,243,dynamic= True))
plt.show()
