from __future__ import print_function
import pandas as pd
import statics as sd
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
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

#1-20,20-30,35-40,45-50,30-33,41-45，
def get_artist_set(filename):
    df = pd.read_csv(filename)
    df.columns=['song_id','artist_id','ppublish_time','song_init_plays','Language','Gender']
    artist_set = df['artist_id'].unique()
    return  artist_set




def get_result():
    df = pd.read_csv('E:/mydata/tianchi_wanyiyun/all_feature.csv')
    df[df==0]=1
    result ={}
    for i in df.columns[0:50]:
        feature =np.log( df[i])
        #feature = df[i]
        #print(feature)
        dta=DataFrame(feature)
        dta.index = pd.Index(pd.date_range('3/1/2015','30/8/2015'))
        dta.columns = ['play']
        mod = sm.tsa.statespace.SARIMAX(dta.play, trend='n', order=(2,1,0), seasonal_order=(1,1,1,30))
        results = mod.fit()
        #print(results.predict(1))
        result[i]=results.predict(183,243,dynamic= True)[-60:]
        #print(dta)
        #plt.plot(dta.play[1:])
        #print( results.predict(150,245))
        #plt.plot( results.predict(1,245))
        #plt.show()
        #print(result)
    #DataFrame(result)
    return  DataFrame(result)
a=get_result()
a.to_csv('E:/mydata/tianchi_wanyiyun/result_5_30.csv')
print(a.head(),a.shape)




























