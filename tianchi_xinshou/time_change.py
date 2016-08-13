#数据探索
import pandas as pd
import numpy as np
import pickle
f = pd.read_csv('E:/mydata/fresh_comp_offline/data_summary_concat.csv',chunksize=1000000)
print(f.get_chunk().info(),f.get_chunk().head())

w = pd.read_csv('E:/mydata/fresh_comp_offline/tianchi_fresh_comp_train_user.csv',chunksize=1000)
print(w.get_chunk().info(),w.get_chunk().head())

import numpy
data = numpy.loadtxt('E:/mydata/fresh_comp_offline/data_summary_concat.csv', dtype='object', delimiter=',')


def date_change(time):
    striped = time.split()[0]
    month,day = striped.split('-')[1],striped.split('-')[2]
    if month == '11':
        return int(day) -17
    else:
        return int(day)+13
#b = '2014-12-08 18'
#print(date_change(b))
def get_chunk_list(x):
    chunks = []
    for each in f:
        each.drop('user_geohash',axis=1,inplace=True)
        each.drop_duplicates()
        each['time'] = each['time'].map(date_change)
        #insert = each.groupby(['user_id','item_id','time'])['behavior_type'].apply(pd.value_counts)
        chunks.append(each)
        #chunks.append(insert)
    return chunks
#chunks = get_chunk_list(f)
'''with open('E:/mydata/fresh_comp_offline/data_chunks.pkl', "wb") as myprofile:
    pickle.dump(chunks[0:5], myprofile)
with open('E:/mydata/fresh_comp_offline/data_chunks.pkl', "rb") as get_myprofile:
    print (pickle.load(get_myprofile))'''

#print(chunks[0].head())
#df_1= pd.concat(chunks[0:2], ignore_index=True)
#test_chunk =chunks[22]
#chunk_test = test_chunk.groupby(['user_id','item_category','item_id','time'])['behavior_type'].apply(pd.value_counts)
#chunk_test.to_csv('E:/mydata/fresh_comp_offline/data_summary_part_23.csv')
#print(chunk_test.head())
#df_1.to_csv('E:/mydata/fresh_comp_offline/data_change_part_2.csv')
#df_2=pd.concat(chunks[10:20],ignore_index=True)
#print(df_1.head())'''
print('done')


