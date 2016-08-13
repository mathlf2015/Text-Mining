import pandas as pd
from datetime import *
import os
import new_idea.feature_abstractor as fea
from sklearn import metrics
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
#os.chdir()设置工作路径
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
print(u'用户行为时间区间%s至%s'%(df_user_action.time.min(),df_user_action.time.max()))

print(u'划分数据集')
print (u'提取2015-12-18当天的数据用作验证集，校验模型预测的效果（day_index == 1)&(behavior_type == 4)')
if not os.path.exists(r'E:\mydata\fresh_comp_offline\user_12_18.csv'):
    df_12_18_user_action = df_user_action[(df_user_action.time_index==1)&(df_user_action.behavior_type==4)]
    df_12_18_user_action = df_12_18_user_action[['user_id','item_id']].drop_duplicates()
    df_12_18_user_action.to_csv(r'E:\mydata\fresh_comp_offline\user_12_18.csv',index=False)
else:
    df_12_18_user_action = pd.read_csv(r'E:\mydata\fresh_comp_offline\user_12_18.csv')

print(u'提取2015-12-17数据用于训练集打标签')
if not os.path.exists(r'E:\mydata\fresh_comp_offline\user_12_17.csv'):
    df_12_17_user_action = df_user_action[(df_user_action.time_index==2)&(df_user_action.behavior_type==4)]
    df_12_17_user_action = df_12_17_user_action[['user_id','item_id']].drop_duplicates()
    df_12_17_user_action.to_csv(r'E:\mydata\fresh_comp_offline\user_12_17.csv',index=False)
else:
    df_12_17_user_action = pd.read_csv(r'E:\mydata\fresh_comp_offline\user_12_17.csv')

print (u'2015-12-16及之前的数据用作提取训练集的特征')
if not os.path.exists(r'E:\mydata\fresh_comp_offline\user_12_16_action.csv'):
    df_12_16_user_action = df_user_action[df_user_action.time_index>2]
    df_12_16_user_action.to_csv(r'E:\mydata\fresh_comp_offline\user_12_16_action.csv',index=False)
else:
    df_12_16_user_action = pd.read_csv(r'E:\mydata\fresh_comp_offline\user_12_16_action.csv')

print (u'2015-12-17及之前的数据用作提取预测12-18的购买的特征')
if not os.path.exists(r'E:\mydata\fresh_comp_offline\user_12_17_action.csv'):
    df_12_17_plus_user_action = df_user_action[df_user_action.time_index>=2]
    df_12_17_plus_user_action.to_csv(r'E:\mydata\fresh_comp_offline\user_12_17_plus_action.csv',index=False)
else:
    df_12_17_plus_user_action = pd.read_csv(r'E:\mydata\fresh_comp_offline\user_12_17_plus_action.csv')

print(u'噪声过滤')
df_12_16_nosier_user = df_12_16_user_action.groupby(['user_id','behavior_type'])['item_id'].count().reset_index()
df_12_16_nosier_user.columns = ['user_id','behavior_type','behavior_count']
df_12_16_nosier_user = df_12_16_nosier_user.pivot('user_id','behavior_type','behavior_count').reset_index()
df_12_16_nosier_user.fillna(0,inplace=True)
print(u'总用户数%d'%len(df_12_16_nosier_user))
#print(df_12_16_nosier_user.head(5))
print (u'过滤爬虫数据:1. 有购买（购买数大于1），但点击数是购买数的500倍以上的用户的数据')
print (u'2.没有购买，但是点击数超过100的用户的数据')
df_12_16_nosier_user = df_12_16_nosier_user[((df_12_16_nosier_user[4]>1) & (df_12_16_nosier_user[1]>df_12_16_nosier_user[4]*500))
 |((df_12_16_nosier_user[4]==0) & (df_12_16_nosier_user[1]>100))]
print(u'爬虫用户数%d'%(len(df_12_16_nosier_user)))
df_12_16_user_action = df_12_16_user_action[~df_12_16_user_action.user_id.isin(df_12_16_nosier_user.user_id.unique())]
print(u'过滤完成')

print (u'----------------------------- 提取<user_id,item_id>特征 ------------------------------')
print (u'最后1天有交互的数据作为基础<user_id,item_id>集合')
df_offline_basic_ui = df_12_16_user_action[df_12_16_user_action['time_index']==3][['user_id','item_id']].drop_duplicates()
df_online_basci_ui = df_12_17_plus_user_action[df_12_17_plus_user_action['time_index']==2][['user_id','item_id']].drop_duplicates()
#print(df_12_16_user_action.head())
df_offline_basic_ui = fea.get_ui_feature(df_12_16_user_action,df_offline_basic_ui)
df_online_basci_ui = fea.get_ui_feature(df_12_17_plus_user_action,df_online_basci_ui)

df_12_17_user_action['buy_lable'] = 1
df_offline_basic_ui = df_offline_basic_ui.merge(df_12_17_user_action,how='left',on=['user_id','item_id'])
df_offline_basic_ui = df_offline_basic_ui.fillna(0)

print(u'提取完特征训练集数据表格式')
print(df_offline_basic_ui.dtypes)
print(u'正负样本数目')
print(df_offline_basic_ui.groupby(['buy_lable'])['user_id'].count().reset_index())

print(u'正负样本数目不平衡，采取抽样')
df_offline_basic_ui_pos = df_offline_basic_ui[df_offline_basic_ui.buy_lable == 1]
df_offline_basic_ui_neg = df_offline_basic_ui[df_offline_basic_ui.buy_lable == 0][0:200]
df_offline_basic_ui_complex = pd.concat([df_offline_basic_ui_pos,df_offline_basic_ui_pos,df_offline_basic_ui_neg])


print(u'提取完特征预测集的数据表格式')
print(df_online_basci_ui.dtypes)

print (u'\n============================ 模型训练 =================================')
train_x = df_offline_basic_ui_complex[['hour_index_dist','hour_index_log_dist','last7day_buy_cnt']]
train_y = df_offline_basic_ui_complex['buy_label']
predict_x = df_online_basci_ui[['hour_index_dist','hour_index_log_dist','last7day_buy_cnt']]

model = GradientBoostingClassifier(n_estimators=200)
model.fit(train_x, train_y)

print (u'\n============================ 模型预测 =================================')
df_online_basci_ui['predict_result'] = model.predict(predict_x)

print (u'预测结果：')
print (df_online_basci_ui.groupby('predict_result').count().reset_index())

print (u'\n============================= 结果评估 ===============================')
df_12_18_user_action['buy_label'] = 1
df_online_basic_ui = df_online_basci_ui[df_online_basci_ui.predict_result == 1]
df_predict_result = df_online_basic_ui.merge(df_12_18_user_action,how='left',on=['user_id','item_id'])
df_predict_result = df_predict_result.fillna(0)
df_predict_result['score'] = df_predict_result['predict_result']  - df_predict_result['buy_label']
df_predict_result['score'] = df_predict_result['score'].apply(lambda x: 1 if x== 0 else 0)
print (u'预测结果统计（0预测错误，1为预测正确):')
print (df_predict_result.groupby('score')['user_id'].count().reset_index())
print (u'总的真实结果集的大小为：%d'%(len(df_12_18_user_action)))








