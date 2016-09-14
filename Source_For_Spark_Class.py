#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/8/17 10:07
# @Author  : LuFeng
from Concernword_Analysis_Class import Concernword_Analysis
from Load_Data_Class import Text_Processing
import csv
from Text_Score_Class import Text_Score
import time
import pymssql
import sys

"""
增加数据库存取数据，删除从csv读入读出部分，
9.8 修正分句出现多个二级情感词时候索引错误的问题
"""

class Sentiment_seg():
    # style参数'str'字符串匹配，'seg'分词,通过修改参数review_id_beg,review_id_end控制选取的评论范围
    def __init__(self,style='str',reviewid_beg=1,reviewid_end=1000,host = '192.168.0.15',user = 'sa',password = '*****',database = 'ReviewAnalysisSystem'):

        self.style = style # 'str'字符串匹配，'seg'分词
        self.reviewid_beg = reviewid_beg
        self.reviewid_end = reviewid_end
        self.tp = Text_Processing()
        self.get_score = Text_Score()
        self.pos_neg_dict ={'pos':1,'neg':0}
        # 数据库链接
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.second_concernword_dict = self.get_second_concernword_dict()


    #得到二级关注点对应的一二级关注点ID(字典)
    def get_second_concernword_dict(self):
        try:
            conn = pymssql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                   charset='UTF-8')
            cur = conn.cursor()
            second_concernword_dict = {}
            # 选取数据
            sql_1 = u"SELECT * FROM Model_firstAndSecondLevelConcernsList"
            cur.execute(sql_1)
            rows = cur.fetchall()
            conn.commit()
            for i in rows:
                if i[3] not in second_concernword_dict:
                    second_concernword_dict[i[3]] = []
                    second_concernword_dict[i[3]].extend([i[0],i[1]])  # (一级关注点ID,二级关注点ID)
                else:
                    second_concernword_dict[i[3]].extend([i[0],i[1]])

            print('构建关注点词典成功!!')
        except:
            print(u'构建关注点词典失败!!')
            print(sys.exc_info()[1])

        # 关闭连接，输出词典，其键值对形式为{二级关注点：(一级关注点ID,二级关注点ID)}
        finally:
            conn.close()
            return second_concernword_dict


    #得到每个关注点下正负情感的索引（对单个分句而言）
    def get_sentiment_idx_for_seg_review(self):
        test_concernword = Concernword_Analysis(self.style,review_id_end=self.reviewid_end)
        ind_dict,source,descriptors = test_concernword.get_ind_dict()
        # print(ind_dict,source,descriptors)
        temp = self.get_score.seg_sentence_sentiment_score(source)
        # print(temp)
        result = {}
        source_sentiment ={}
        for keyword in ind_dict:
            result[keyword] = {}
            result[keyword]['neg'] = []
            result[keyword]['pos'] = []
            source_sentiment[keyword] = {}
            source_sentiment[keyword]['neg'] = set()
            source_sentiment[keyword]['pos'] = set()
            # print(len(temp[keyword]),len(ind_dict[keyword]),len(source[keyword]))
            for i in range(len(ind_dict[keyword])):
                # print(temp[keyword][i])
                if temp[keyword][i][0]-temp[keyword][i][1] > 0:
                    result[keyword]['pos'].append(ind_dict[keyword][i])
                    source_sentiment[keyword]['pos'].add(source[keyword][i])
                else:
                    result[keyword]['neg'].append(ind_dict[keyword][i])
                    source_sentiment[keyword]['neg'].add(source[keyword][i])
        # print(source_sentiment)
        return result,source_sentiment


    def get_sentiment_seg(self):
        test_concernword = Concernword_Analysis(self.style,review_id_beg=self.reviewid_beg,review_id_end=self.reviewid_end)
        concernword_dict = test_concernword.concernword_dict
        dic_for_partition,dic_for_source= self.get_sentiment_idx_for_seg_review()
        rawdata = test_concernword.data
        #将评论id和评论做成字典对应
        rawdata = dict(zip(rawdata[1],rawdata[0]))
        # print(rawdata)
        #print(dic_for_partition['物流'])
        output = {}
        for keyword in dic_for_partition:
            if keyword not in output:
                output[keyword] = {}
                output[keyword]['neg'] = []  #情感极性
                output[keyword]['pos'] = []
                output[keyword]['neg_seg'] = [] #分局内容
                output[keyword]['pos_seg'] = []
                output[keyword]['neg_descriptor'] = [] #二级关注点描述词
                output[keyword]['pos_descriptor'] = []
                output[keyword]['neg_review_id'] = []  #评论ID
                output[keyword]['pos_review_id'] = []
            temp_neg = []
            temp_neg_review_id = []
            for i in dic_for_partition[keyword]['neg']:
                # print(rawdata[i])
                #去重，rawdata的索引和输入文件格式有关
                if self.tp.cut_sentence_2(rawdata[i]) not in temp_neg:
                    temp_neg.append(self.tp.cut_sentence_2(rawdata[i]))
                    temp_neg_review_id.append(i)

            for review_id,review in zip(temp_neg_review_id,temp_neg):
                for sent in review:
                    for concernword in concernword_dict[keyword]:
                        if sent.find(concernword) != -1 and sent in dic_for_source[keyword]['neg']:
                            output[keyword]['neg'].append(review)
                            output[keyword]['neg_seg'].append(sent)
                            output[keyword]['neg_descriptor'].append(concernword)
                            output[keyword]['neg_review_id'].append(review_id)

            temp_pos = []
            temp_pos_review_id = []
            for i in dic_for_partition[keyword]['pos']:
                # print(rawdata[i])
                # 去重
                if self.tp.cut_sentence_2(rawdata[i]) not in temp_pos :
                    temp_pos.append(self.tp.cut_sentence_2(rawdata[i]))
                    temp_pos_review_id.append(i)

            for review_id,review in zip(temp_pos_review_id,temp_pos):
                for sent in review:
                    for concernword in concernword_dict[keyword]:
                        if sent.find(concernword) != -1 and sent in dic_for_source[keyword]['pos']:
                            output[keyword]['pos'].append(review)
                            output[keyword]['pos_seg'].append(sent)
                            output[keyword]['pos_descriptor'].append(concernword)
                            output[keyword]['pos_review_id'].append(review_id)
        # print(output)
        return output

    # 输出最终结果[评论ID，分局内容，分句情感标识，一级关注点id，二级关注点id,分句id]，并存储数据库
    def save_database(self,output):
        database_input = []

        #确定shortSentenceID的起始位置
        try:
            conn = pymssql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                   charset='UTF-8')
            cur = conn.cursor()
            sql_1 = u"SELECT COUNT(shortSentenceID) FROM ResultMiddle_shortSentenceEmotionAndConcernsResult"
            cur.execute(sql_1)
            rows = cur.fetchall()
            conn.commit()
            count = rows[0][0]
            print('取出短句id成功')
        except:
            print(u'取出短句id失败!!')
            print(sys.exc_info()[1])

        # 关闭连接
        finally:
            conn.close()

        for keyword in output:
            # [评论ID，分局内容，分句情感标识，一级关注点id，二级关注点id, 分句id]
            for idx in range(len(output[keyword]['pos'])):
                count += 1
                # print(output[keyword]['pos_review_id'][idx],output[keyword]['pos_seg'][idx],self.pos_neg_dict['pos'],self.second_concernword_dict[output[keyword]['pos_descriptor'][idx]][0],self.second_concernword_dict[output[keyword]['pos_descriptor'][idx]][1],count)
                database_input.append((output[keyword]['pos_review_id'][idx],output[keyword]['pos_seg'][idx],self.pos_neg_dict['pos'],self.second_concernword_dict[output[keyword]['pos_descriptor'][idx]][0],self.second_concernword_dict[output[keyword]['pos_descriptor'][idx]][1],count))
            for idx in range(len(output[keyword]['neg'])):
                count += 1
                # print(output[keyword]['neg_review_id'][idx], output[keyword]['neg_seg'][idx], self.pos_neg_dict['neg'],self.second_concernword_dict[output[keyword]['neg_descriptor'][idx]][0],self.second_concernword_dict[output[keyword]['neg_descriptor'][idx]][1],count)
                database_input.append((output[keyword]['neg_review_id'][idx], output[keyword]['neg_seg'][idx], self.pos_neg_dict['neg'],self.second_concernword_dict[output[keyword]['neg_descriptor'][idx]][0],self.second_concernword_dict[output[keyword]['neg_descriptor'][idx]][1],count))

        # print(database_input)
        try:
            conn = pymssql.connect(host=self.host, user=self.user, password=self.password, database=self.database, charset='UTF-8')
            cur = conn.cursor()
            # 插入数据
            sql_1 = u"insert into ResultMiddle_shortSentenceEmotionAndConcernsResult(reviewID,shortSentence,shortSentenceEmotionTag,firstLevelConcernsID,secondLevelConcernsID,shortSentenceID) values(%s,%s,%s,%s,%s,%s)"
            cur.executemany(sql_1, database_input)
            conn.commit()

            print('写进数据库成功!!')
        except:
            print(u'写进数据库失败!!')
            print(sys.exc_info()[1])

        # 关闭连接
        finally:
            conn.close()
            print(count)
            # return count


    # 对打完分分好类的关注点词频进行统计（用不到，可以在数据库中实现）
    def sentimented_seg_concernword_analysis(self,output,top_num=5,output_file=r'C:\Users\Data\Desktop\output.csv'):
        pos_set =[]
        neg_set =[]
        for keyword in output:
            pos_set.append([keyword,len(output[keyword]['pos'])])
            neg_set.append([keyword,len(output[keyword]['neg'])])
        pos_set = sorted(pos_set,key=lambda x: x[1],reverse=True)
        neg_set = sorted(neg_set,key=lambda x: x[1],reverse=True)
        pos_sum = sum([x[1] for x in pos_set])
        neg_sum = sum([x[1] for x in neg_set])
        writer = csv.writer(open(output_file,'w'),lineterminator='\n')
        print('pos')
        writer.writerow(('pos',))
        for i in pos_set[:top_num]:
            print('%s: %d,%.4f'%(i[0],i[1],i[1]/pos_sum))
            writer.writerow((i[0],i[1],i[1]/pos_sum))
        print('neg')
        writer.writerow(('neg',))
        for i in neg_set[:top_num]:
            print('%s: %d,%.4f'%(i[0],i[1],i[1]/neg_sum))
            writer.writerow((i[0],i[1],i[1]/neg_sum))



if __name__ == '__main__':
    #跑完60多万条记录大概2小时
    t1 = time.time()
    for_test = Sentiment_seg(style='str',reviewid_beg=1,reviewid_end=700000)
    output = for_test.get_sentiment_seg()
    # print(output)
    for_test.save_database(output)
    t2 = time.time()
    print('消耗时间%d'%(t2-t1))
