import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame

#--------stable-------------------
import os,sys
path = os.getcwd()
parent_path = os.path.dirname(path)
parent_path = os.path.dirname(parent_path)	#notice
sys.path.append(parent_path)
import statics as sd
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
#--------stable-------------------
def num2Week(num):
	week=(START_WEEK+num)%7
	if week==0:
		return 7
	return week
'''
songs is a table:
row:DAYS=183
column:2(index,num2Week)+len(songs_list)+result(sum of play)
'''
def loadData(artist):
    artist_feature=[]
    with open(ARTIST_P_D_C,'r',encoding='utf-8') as fr:
        artist_id=fr.readline().strip('\n')
        while artist_id:
            play=list(map(int,fr.readline().strip('\n').split(',')))
            download=list(map(int,fr.readline().strip('\n').split(',')))
            collect=list(map(int,fr.readline().strip('\n').split(',')))
            if artist==artist_id:
                for i in range(DAYS):
                    artist_feature.append(play[i])
            artist_id=fr.readline().strip('\n')
    return artist_feature



'''diabetes=loadData('0c80008b0a28d356026f4b1097041689')
diabetes=np.array(diabetes)
print(diabetes)'''


def get_artist_set(filename):
    df = pd.read_csv(filename)
    df.columns=['song_id','artist_id','ppublish_time','song_init_plays','Language','Gender']
    artist_set = df['artist_id'].unique()
    return  artist_set

artist_set = get_artist_set(ARTIST)
#print(artist_set)

def get_all_feature(set):
    feature = {}
    for artist in set:
         feature[artist] = loadData(artist)
    return DataFrame(feature)
#print(get_all_feature(artist_set).shape)
#所有特征，183*50，第一列为歌手id,每一行为每天这个歌手歌曲下载量
get_all_feature(artist_set).to_csv('E:/mydata/tianchi_wanyiyun/all_feature.csv',index=False)



