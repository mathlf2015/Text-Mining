from __future__ import print_function
import pandas as pd
import statics as sd
from pandas import DataFrame
import pandas as pd
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


#41，35,34,18

def get_result():
    df = pd.read_csv('E:/mydata/tianchi_wanyiyun/all_feature.csv')
    result ={}
    list_1=['445a257964b9689f115a69e8cc5dcb75','9e58afbf3fea116b0050bf56bfb4442e','9f69ffd8852196e02cfa19b5cd9bc432','c026b84e8f23a7741d9b670e3d8973f0','8fb3cef29f2c266af4c9ecef3b780e97']
    for i in list_1:
        feature = df[i]
        dta=DataFrame(feature)
        dta.index = pd.Index(pd.date_range('3/1/2015','30/8/2015'))
        dta.columns = ['play']
        mod = sm.tsa.statespace.SARIMAX(dta.play, trend='n', order=(2,0,0), seasonal_order=(1,1,1,30))
        results = mod.fit()
        #print(results.predict(1))
        result[i]=results.predict(183,243,dynamic= True)[-60:]
    return  DataFrame(result)
a=get_result()
a.to_csv('E:/mydata/tianchi_wanyiyun/result_6.csv')
print(a.head(),a.shape)




























