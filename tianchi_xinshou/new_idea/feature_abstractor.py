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

import os

def get_ui_feature(df_20151216_user_action,df_basic_ui):
    print (u'提取特征1：前一天加购物篮的时间')
    df_20151216_addcart_action = df_20151216_user_action[
        (df_20151216_user_action.time_index == 3) & (df_20151216_user_action.behavior_type == 3)]
    df_20151216_addcart_action = df_20151216_addcart_action[['user_id', 'item_id', 'hour_index']]
    print (u'把加购物篮的时间转化成相对时间，即距离要预测的购物行为的小时数')
    df_20151216_addcart_action['hour_index_dist'] = 24 - df_20151216_addcart_action['hour_index']
    print (u'购物行为具有一定的艾宾浩斯遗忘曲线特性，加一个对时间取对数的特征')
    df_20151216_addcart_action['hour_index_log_dist'] = np.log2(df_20151216_addcart_action['hour_index_dist'])
    print (u'历史重复购买也许会对购物有影响，加一个最近7天的购买次数')
    df_offline_last7day_user_actions = df_20151216_user_action[
        (df_20151216_user_action.time_index < 10) & (df_20151216_user_action.behavior_type == 4)]
    df_offline_last7day_user_actions = df_offline_last7day_user_actions.groupby(['user_id', 'item_id'])[
        'time_index'].count().reset_index()
    df_offline_last7day_user_actions.columns = ['user_id', 'item_id', 'last7day_buy_cnt']
    print (u'合并特征')
    df_offline_basic_ui = df_basic_ui.merge(df_20151216_addcart_action, how='left', on=['user_id', 'item_id'])
    df_offline_basic_ui = df_offline_basic_ui.merge(df_offline_last7day_user_actions, how='left',
                                                    on=['user_id', 'item_id'])
    df_offline_basic_ui = df_offline_basic_ui.fillna(0)

    return df_offline_basic_ui