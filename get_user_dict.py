#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/8/31 16:36
# @Author  : LuFeng
# @File    : get_user_dict.py
import pymssql
import sys
import os
host = '192.168.0.25'
user = 'sa'
password = '********'
database = 'ReviewAnalysisSystem'
try:
    conn = pymssql.connect(host=host, user=user, password=password, database=database,
                           charset='UTF-8')
    cur = conn.cursor()
    result ={}
    # 选取数据，sql查询语句需要经常修改，通过reviewID范围控制选取的评论，
    sql_1 = u"SELECT firstLevelConcernsName,secondLevelConcernsName FROM Model_firstAndSecondLevelConcernsList"
    cur.execute(sql_1)
    rows = cur.fetchall()
    conn.commit()
    for i in rows:
        if i[0] not in result:
            result[i[0]] = set()
            result[i[0]].add(i[1])
        else:
            result[i[0]].add(i[1])

    sql_1 = u"SELECT COUNT(shortSentenceID) FROM ResultMiddle_shortSentenceEmotionAndConcernsResult"
    cur.execute(sql_1)
    rows = cur.fetchall()
    conn.commit()
    print(rows[0][0])
    print('取出数据成功!!')
except:
    print(u'取出数据失败!!')
    print(sys.exc_info()[1])

# 关闭连接
finally:
    conn.close()
print(result)



import csv
source = []
for item in result:
    source.extend(item.split('/'))
    source.extend(result[item])
b= set(source)
f = open('usr_dict.txt','w',encoding='utf')
for i in b:
    f.write(str(i)+' 50'+'\n')
f.close()


def inject_jeba(file_path):
    file_set = os.listdir(os.chdir(file_path))
    result =[]
    for file in file_set:
        with open(file) as f:
            print(file)
            for line in f:
                result.append(line.strip())
    return  result


result = inject_jeba('sentimentDict/')
f = open('D:/project_reviews_analysis/usr_dict.txt','a',encoding='utf')
for i in result:
    f.write(i+' 4'+'\n')
f.close()


result = []
with open(u"D:/project_reviews_analysis/负面.txt") as f:
    for word in f:
        result.append(word.strip())

with open(u"D:/project_reviews_analysis/正面.txt") as f:
    for word in f:
        result.append(word.strip())
print(result)

f = open('D:/project_reviews_analysis/usr_dict.txt','a',encoding='utf')
for i in result:
    f.write(i+' 100'+'\n')
f.close()