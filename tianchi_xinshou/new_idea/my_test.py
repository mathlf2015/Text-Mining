# -*- coding: utf-8 -*-
import pandas as pd
from datetime import *
df_user_action = pd.read_csv(r'E:\mydata\fresh_comp_offline\test.csv')
df_item = pd.read_csv(r'E:\mydata\fresh_comp_offline\tianchi_fresh_comp_train_item.csv')

print(u'初步数据处理')
#删除地理信息
del df_user_action['user_geohash']
del df_item['item_geohash']
print(df_item.head())
#print(df_user_action.head())

#日期转换
#print(datetime.strptime('2014-12-08 18','%Y-%m-%d %H'))
df_user_action['time']=df_user_action['time'].apply(lambda x:datetime.strptime(x,'%Y-%m-%d %H'))
max_day = df_user_action['time'].max()
#print(max_day)
df_user_action['time_index']=df_user_action['time'].apply(lambda x:(max_day - x).days + 1)
df_user_action['hour_index'] = df_user_action['time'].dt.hour
print(df_user_action.head())
df_user_action.to_csv(r'E:\mydata\fresh_comp_offline\user_action.csv',index=False)
df_item.to_csv(r'E:\mydata\fresh_comp_offline\item.csv',index=False)
print(u'初步数据处理完成')


print(u'数据探索')
df_item = pd.read_csv(r'E:\mydata\fresh_comp_offline\item.csv')
df_user_action = pd.read_csv(r'E:\mydata\fresh_comp_offline\user_action.csv')
print(df_user_action.head(5))
print(df_item.head(5))
print(u'统计特征')
print(df_user_action.dtypes)
print(u'用户行为表记录数%d'%len(df_user_action))
print(u'用户人数%d'%df_user_action.user_id.nunique())
print(u'商品数目%d'%df_user_action.item_id.nunique())
print(u'商品类别数%d'%df_user_action.item_category.nunique())
print (u'用户行为类型（1:点击、2:加收藏、3:加购物篮、4:购买）的数量：')
print(df_user_action.groupby('behavior_type')['time'].count().reset_index())
print(u'用户行为时间区间%s-%s'%(df_user_action.time.min(),df_user_action.time.max()))


