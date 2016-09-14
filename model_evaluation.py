#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/9/2 16:09
# @Author  : LuFeng
# @File    : model_evaluation.py

import pymssql
import sys
import csv
import pandas as pd
'''host = '192.168.0.25'
user = 'sa'
password = 'i2mago.com'
database = 'ReviewAnalysisSystem'
try:
    conn = pymssql.connect(host=host, user=user, password=password, database=database,
                           charset='UTF-8')
    cur = conn.cursor()
    result ={}
    # 选取数据，sql查询语句需要经常修改，通过reviewID范围控制选取的评论，
    sql_1 = u"SELECT top 250 review,reviewEmotionTag  FROM Product_productReview WHERE reviewEmotionTag=0 and reviewID>5000 AND reviewID <12000"
    cur.execute(sql_1)
    rows1 = cur.fetchall()
    conn.commit()
    sql_2 = u"SELECT top 250 review,reviewEmotionTag  FROM Product_productReview WHERE reviewEmotionTag=1 and reviewID>15000 AND reviewID <22000"
    cur.execute(sql_2)
    rows2 = cur.fetchall()
    conn.commit()
    writer = csv.writer(open('C:/Users/Data/Desktop/evaluate_1.csv','a'),lineterminator='\n')
    for i in rows1:
        writer.writerow((i[0],i[1]))
    for i in rows2:
        writer.writerow((i[0],i[1]))


    print('取出数据成功!!')
except:
    print(u'取出数据失败!!')
    print(sys.exc_info()[1])

# 关闭连接
finally:
    conn.close()'''


df = pd.read_csv('C:/Users/Data/Desktop/evaluate_1.csv',encoding='gbk')
evaluation = df.ix[:,[1,2]]
evaluation.columns = ['pred','truth']
print(evaluation[['pred','truth']])
# evaluation['pred'] = evaluation['pred'].apply(lambda x:1 if x==0 else 0)
# evaluation['truth'] = evaluation['truth'].apply(lambda x:1 if x==0 else 0)
print(evaluation)
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix
y_test = evaluation['truth']
y_pred = evaluation['pred']
print('accuracy_score: %s'%accuracy_score(y_test,y_pred))
print('precision_score: %s'%precision_score(y_test,y_pred))
print('recall_score: %s'%recall_score(y_test,y_pred))
print('f1_score: %s'%f1_score(y_test,y_pred))
print('confusion_matrix:',confusion_matrix(y_test,y_pred))