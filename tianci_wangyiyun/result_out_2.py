import pandas as pd
from pandas import DataFrame
import numpy as np
def get_output():
    #df_1= pd.read_csv('E:/mydata/tianchi_wanyiyun/all_feature.csv')
    #feature_8_30 = df_1.iloc[-1]
    #print(feature_8_30)
    read_in_set = ['E:/mydata/tianchi_wanyiyun/result_{}.csv'.format(str(i)) for i in range(1,7)]
    output_set = ['E:/mydata/tianchi_wanyiyun/upload_{}.csv'.format(str(i)) for i in range(1,7)]
    for i in range(6):
        df_2 = pd.read_csv(read_in_set[i])
        index1=list(range(20150901,20150931))+list(range(20151001,20151031))
        df_2.index=[ str(i) for i in index1]
        df_2.drop('Unnamed: 0',axis=1,inplace=True)
        df_3 = df_2.apply(lambda x:np.rint(x))
        df_4=df_3.stack().unstack(0).stack()
        #print(df_4)
        df_4.apply(lambda x:str(x)).to_csv(output_set[i],encoding='utf-8')

get_output()