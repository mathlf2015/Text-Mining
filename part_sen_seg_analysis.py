import pymssql
import sys

from Text_Score_Class import Text_Score
from Concernword_Analysis_Class import Concernword_Analysis
import time
import jieba
jieba.load_userdict('D:/project_reviews_analysis/usr_dict.txt')
rawdata_set = ['D:/测试数据/test_{}.csv'.format(str(i)) for i in range(1,4)]
score_set = ['D:/测试数据/result_{}.csv'.format(str(i)) for i in range(1,4)]
analysis_seg_set = ['D:/测试数据/analysis_{}_seg.csv'.format(str(i)) for i in range(1,4)]
analysis_str_set = ['D:/测试数据/analysis_{}_str.csv'.format(str(i)) for i in range(1,4)]
seg_set = ['D:/测试数据/seg_{}.csv'.format(str(i)) for i in range(1,4)]
part_sen_seg_set = ['D:/测试数据/part_sen_seg_{}.csv'.format(str(i)) for i in range(1,4)]


temp=[]
for idx in range(3):
    test_concernword = Concernword_Analysis('str', 'D:/project_review/concernwords_2.csv', rawdata_set[idx],
                                             analysis_seg_set[idx],part_sen_seg_set[idx])
    source = test_concernword.get_ind_dict()[1]
    temp.append(source)
source = {}
for item in temp:
    # print(item)
    for i in item:
        if i not in source:
            source[i] = item[i]
        else:
            source[i].extend(item[i])

# for key in source:
#     print(key,source[key])
# result = []
# for i in source.keys():
#     for seg_sen in source[i]:
#         result.append((i, seg_sen))
# for i in result:
#     print(i)



#导入数据库
host = 'localhost'
user = 'sa'
password = '1234'
database = 'my project'
try:
    conn = pymssql.connect(host=host, user=user, password=password, database=database, charset='UTF-8')
    cur = conn.cursor()
    result = []
    for i in source.keys():
        for seg_sen in source[i]:
            result.append((i, seg_sen))
    # print(result)
    # 新建数据库
    sql_1 = u"create table my_test(id nvarchar(max),review nvarchar(max))"
    cur.execute(sql_1)
    conn.commit()

    # 插入数据
    sql_2 = u"insert into my_test(id,review) values(%s,%s)"
    cur.executemany(sql_2, result)
    conn.commit()

    print('写进数据库成功!!')
except:
    print(u'写进数据库失败!!')
    print(sys.exc_info()[1])

# 关闭连接
finally:
    conn.close()