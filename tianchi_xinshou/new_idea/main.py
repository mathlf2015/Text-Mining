# -*- coding: utf-8 -*-
#
# 金陵书生<netivs@qq.com>
# 欢迎加天池大数据非官方QQ讨论群： 155167917 ，众多大神在里面交流。
# 本程序是写来演示 2015天池大数据移动推荐大赛 的线下评测流程的，供初学者参考，有问题可加群或通过QQ联系我。
#  2016.05.18
#
import pandas as pd
from pandas import DataFrame,Series
import numpy as np
from datetime import *
import new_idea.feature_abstractor as fea
import os
from sklearn import metrics
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
#import gbdt

#---------------------------------- 主程序 ----------------------------------#
print (u'==================数据加载：原始数据加载、解析与抽样查看 =================')
if(not os.path.exists('data/tianchi_mobile_user_actions.csv')):
    df_user_actions = pd.read_csv('data/tianchi_mobile_recommend_train_user.csv')
    #df_user_actions = df_user_actions[1:1000] # 先测试程序的语法
    df_item_category = pd.read_csv('data/tianchi_mobile_recommend_train_item.csv')

    print (u'\n==================数据预处理1：格式转换、噪音过滤、缺失值填充等=================')
    print (u'--------------------- 地理位置信息暂时不用，删掉该信息 ----------------------')
    del df_user_actions['user_geohash']
    del df_item_category['item_geohash']

    print (u'----------------------------- 时间格式数据转换 --------------------------------')
    print (u'YYYYmmdd HH转换成天编号（逆序第几天，即距离要预测那天的第几天）和小时编号(1-24)两个字段')
    df_user_actions['time'] = df_user_actions['time'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H'))
    max_day = df_user_actions['time'].max()
    df_user_actions['day_index'] = df_user_actions['time'].apply(lambda x: (max_day - x).days + 1)
    df_user_actions['hour_index'] = df_user_actions['time'].dt.hour
    print (u'时间格式转换后的前5条数据：')
    print (df_user_actions.head(5))

    df_user_actions.to_csv('data/tianchi_mobile_user_actions.csv',index=False)
else:
    df_user_actions = pd.read_csv('data/tianchi_mobile_user_actions.csv')
    df_item_category = pd.read_csv('data/tianchi_mobile_recommend_train_item.csv')

print (u'-----------------------前5条用户行为数据-----------------------------')
print (df_user_actions.head(5))
print (u'\n--------------------- 前5条商品品类数据 ---------------------------')
print (df_item_category.head(5))

print (u'\n==================数据探索：显示数据的统计特征====================')
print (u'--------------------- 用户行为数据统计特性 ----------------------')
print (u'用户行为表的表结构：')
print (df_user_actions.dtypes)
print(u'用户行为表的记录数：%d'%(len(df_user_actions)))
print (u'用户行为表的用户数：%d'%(df_user_actions.user_id.nunique()))
print (u'用户行为表的商品数：%d'%(df_user_actions.item_id.nunique()))
print (u'用户行为表的品类数：%d'%(df_user_actions.item_category.nunique()))
print (u'用户行为类型（1:点击、2:加收藏、3:加购物篮、4:购买）的数量：')
print (df_user_actions.groupby('behavior_type')['time'].count().reset_index())
print (u'用户行为时间的范围：%s 至 %s'%(df_user_actions.time.min(),df_user_actions.time.max()))

print (u'\n--------------------- 商品品类的数据统计特性 ----------------------')
print (u'商品品类的记录数：%d'%(len(df_item_category)))
print (u'商品品类中的商品数：%d'%(df_item_category.item_id.nunique()))
print (u'商品品类中的品类数：%d'%(df_item_category.item_category.nunique()))


print (u'\n=========================== 数据集划分 ================================')
print (u'数据集按日期划分为4部分：')
print (u'提取2015-12-18当天的数据用作验证集，校验模型预测的效果（day_index == 1)&(behavior_type == 4)')
if(not os.path.exists('data/df_20151218_user_action.csv')):
    df_20151218_user_action = df_user_actions[(df_user_actions.day_index == 1)&(df_user_actions.behavior_type == 4)]
    df_20151218_user_action = df_20151218_user_action[['user_id','item_id']].drop_duplicates()
    df_20151218_user_action.to_csv('data/df_20151218_user_action.csv',index=False)
else:
    df_20151218_user_action = pd.read_csv('data/df_20151218_user_action.csv')

print (u'提取2015-12-17当天的数据用作给训练集打标签')
if(not os.path.exists('data/df_20151217_user_action.csv')):
    df_20151217_user_action = df_user_actions[(df_user_actions.day_index == 2)&(df_user_actions.behavior_type == 4)]
    df_20151217_user_action = df_20151217_user_action[['user_id','item_id']].drop_duplicates()
    df_20151217_user_action.to_csv('data/df_20151217_user_action.csv', index=False)
else:
    df_20151217_user_action = pd.read_csv('data/df_20151217_user_action.csv')

print (u'2015-12-16及之前的数据用作提取训练集的特征')
if(not os.path.exists('data/df_20151216_user_action.csv')):
    df_20151216_user_action = df_user_actions[df_user_actions.day_index > 2]
    df_20151216_user_action.to_csv('data/df_20151216_user_action.csv', index=False)
else:
    df_20151216_user_action = pd.read_csv('data/df_20151216_user_action.csv')

print (u'2015-12-17及之前的数据用作提取预测集（预测2015.12.18的销售）的特征')
if(not os.path.exists('data/df_20151217plus_user_action.csv')):
    df_20151217plus_user_action = df_user_actions[df_user_actions.day_index >= 2]
    df_20151217plus_user_action.to_csv('data/df_20151217plus_user_action.csv', index=False)
else:
    df_20151217plus_user_action = pd.read_csv('data/df_20151217plus_user_action.csv')

print (u'\n================== 特征提取：用户特征、商品特征、品类特征等 =================')
print (u'------------------------- 数据预处理2：噪音数据处理 -------------------------')
print (u'----------------------------- 噪音数据过滤 --------------------------------')
print (u'提取用户的不同行为的数量，用于识别爬虫')
df_20151216_noise_user = df_20151216_user_action.groupby(['user_id','behavior_type'])['item_id'].count().reset_index()
df_20151216_noise_user.columns = ['user_id','behavior_type','behavior_count']
df_20151216_noise_user = df_20151216_noise_user.pivot('user_id','behavior_type','behavior_count')
df_20151216_noise_user = df_20151216_noise_user.reset_index()
df_20151216_noise_user = df_20151216_noise_user.fillna(0) # 没有的数据填充0
print(df_20151216_noise_user.user_id)
print (u'总的用户数为：%d'%(len(df_20151216_noise_user)))

print (u'过滤爬虫数据:1. 有购买（购买数大于1），但点击数是购买数的500倍以上的用户的数据')
print (u'2.没有购买，但是点击数超过100的用户的数据')
df_20151216_noise_user = df_20151216_noise_user[
    ((df_20151216_noise_user[1]>df_20151216_noise_user[4]*500)&(df_20151216_noise_user[4]>0))
    |((df_20151216_noise_user[1]>500)&(df_20151216_noise_user[4]==0))]
print (u'爬虫用户数为：%d'%(len(df_20151216_noise_user)))

print (u'过滤掉爬虫用户...')
df_20151216_user_action = df_20151216_user_action[~df_20151216_user_action.user_id.isin(df_20151216_noise_user.user_id.unique())]

print (u'----------------------------- 提取<user_id,item_id>特征 ------------------------------')
print (u'最后1天有交互的数据作为基础<user_id,item_id>集合')
df_offline_basic_ui = df_20151216_user_action[df_20151216_user_action.day_index == 3][['user_id','item_id']].drop_duplicates()
df_online_basic_ui = df_20151217plus_user_action[df_20151217plus_user_action.day_index == 2][['user_id','item_id']].drop_duplicates()

df_offline_basic_ui = fea.get_ui_feature(df_20151216_user_action,df_offline_basic_ui)
df_online_basic_ui = fea.get_ui_feature(df_20151217plus_user_action,df_online_basic_ui)

df_20151217_user_action['buy_label'] = 1 # 20151217有购买的都标记为1
df_offline_basic_ui = df_offline_basic_ui.merge(df_20151217_user_action,how='left',on=['user_id','item_id'])
df_offline_basic_ui = df_offline_basic_ui.fillna(0)

print (u'提取完特征后的训练集的数据表格式为：')
print (df_offline_basic_ui.dtypes)
print (u'训练集的正负样本数分别为：')
print (df_offline_basic_ui.groupby('buy_label')['user_id'].count().reset_index())

print (u'正负样本严重不平衡，对正负样本进行抽样')
df_offline_basic_ui_pos = df_offline_basic_ui[df_offline_basic_ui.buy_label == 1]
df_offline_basic_ui_neg = df_offline_basic_ui[df_offline_basic_ui.buy_label == 0][0:2000]

df_offline_basic_ui_complex = pd.concat([df_offline_basic_ui_pos,df_offline_basic_ui_pos,df_offline_basic_ui_neg])

print (u'提取完特征后的预测集的数据表格式为：')
print (df_online_basic_ui.dtypes)

print (u'\n============================ 模型训练 =================================')
train_x = df_offline_basic_ui_complex[['hour_index_dist','hour_index_log_dist','last7day_buy_cnt']]
train_y = df_offline_basic_ui_complex['buy_label']
predict_x = df_online_basic_ui[['hour_index_dist','hour_index_log_dist','last7day_buy_cnt']]

model = GradientBoostingClassifier(n_estimators=200)
model.fit(train_x, train_y)

print (u'\n============================ 模型预测 =================================')
df_online_basic_ui['predict_result'] = model.predict(predict_x)

print (u'预测结果：')
print (df_online_basic_ui.groupby('predict_result').count().reset_index())

print (u'\n============================= 结果评估 ===============================')
df_20151218_user_action['buy_label'] = 1
df_online_basic_ui = df_online_basic_ui[df_online_basic_ui.predict_result == 1]
df_predict_result = df_online_basic_ui.merge(df_20151218_user_action,how='left',on=['user_id','item_id'])
df_predict_result = df_predict_result.fillna(0)
df_predict_result['score'] = df_predict_result['predict_result']  - df_predict_result['buy_label']
df_predict_result['score'] = df_predict_result['score'].apply(lambda x: 1 if x== 0 else 0)
print (u'预测结果统计（0预测错误，1为预测正确):')
print (df_predict_result.groupby('score')['user_id'].count().reset_index())
print (u'总的真实结果集的大小为：%d'%(len(df_20151218_user_action)))