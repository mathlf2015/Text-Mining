#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/8/17 10:07
# @Author  : LuFeng
from Concernword_Analysis_Class import Concernword_Analysis
import pandas as pd
from Load_Data_Class import Text_Processing
import csv
from Text_Score_Class import Text_Score
import time

class Sentiment_seg():

    def __init__(self,score_name,rawdata_name,style,output_for_spark='C:/Users/Data/Desktop/input_for_quency.csv'):
        self.score_name = score_name
        self.rawdata_name = rawdata_name
        self.style = style
        self.tp = Text_Processing()
        self.get_score = Text_Score(self.rawdata_name,self.score_name)
        self.output_for_spark = output_for_spark

    #得到每个关注点下正负情感的索引（对整个分句而言）
    def get_sentiment_idx_for_review(self):
        test_concernword = Concernword_Analysis(self.style, self.rawdata_name)
        ind_dict = test_concernword.get_ind_dict()[0]
        score = pd.read_csv(self.score_name, header=None)
        result = {}
        temp = score.ix[:, 0] - score.ix[:, 1]

        for keyword in ind_dict:
            if keyword not in result:
                result[keyword] = {}
                result[keyword]['neg'] = []
                result[keyword]['pos'] = []

                for idx in ind_dict[keyword]:
                    if temp[idx] < 0:
                        result[keyword]['neg'].append(idx)
                    else:
                        result[keyword]['pos'].append(idx)
        # print(DataFrame(result))
        return result

    #得到每个关注点下正负情感的索引（对单个分句而言）
    def get_sentiment_idx_for_seg_review(self):
        test_concernword = Concernword_Analysis(self.style, self.rawdata_name)
        ind_dict,source,descriptors = test_concernword.get_ind_dict()
        # print(ind_dict,source,descriptors)
        temp = self.get_score.seg_sentence_sentiment_score(source)
        # print(temp)
        result = {}
        for keyword in ind_dict:
            result[keyword] = {}
            result[keyword]['neg'] = []
            result[keyword]['pos'] = []
            # print(len(temp[keyword]),len(ind_dict[keyword]),len(source[keyword]))
            for i in range(len(ind_dict[keyword])):
                # print(i)
                if temp[keyword][i][0]-temp[keyword][i][1]< 0:
                    result[keyword]['neg'].append(ind_dict[keyword][i])
                elif temp[keyword][i][0]-temp[keyword][i][1]>0:
                    result[keyword]['pos'].append(ind_dict[keyword][i])
        # print(result)
        return result

    #输出最终结果[关注点，正负情感，形容词，分句，整条评论]
    def get_sentiment_seg(self):
        test_concernword = Concernword_Analysis(self.style, self.rawdata_name, 'D:/no_need_1.csv', 'D:/no_need_2.csv')
        concernword_dict = test_concernword.get_my_concernword()
        dic_for_partition = self.get_sentiment_idx_for_seg_review()
        rawdata = pd.read_csv(self.rawdata_name, encoding='gbk')
        #print(rawdata)
        #print(dic_for_partition['物流'])
        output = {}
        for keyword in dic_for_partition:
            if keyword not in output:
                output[keyword] = {}
                output[keyword]['neg'] = []
                output[keyword]['pos'] = []
                output[keyword]['neg_seg'] = []
                output[keyword]['pos_seg'] = []
                output[keyword]['neg_descriptor'] = []
                output[keyword]['pos_descriptor'] = []

            temp_neg = []
            for i in dic_for_partition[keyword]['neg']:
                # print(tp.cut_sentence_2(rawdata.ix[i,1]))
                #去重
                if self.tp.cut_sentence_2(rawdata.ix[i, 0]) not in temp_neg:
                    temp_neg.append(self.tp.cut_sentence_2(rawdata.ix[i, 0])) # rawdata的索引和输入文件格式有关


            for idx, review in enumerate(temp_neg):
                for sent in review:
                    for concernword in concernword_dict[keyword]:
                        if sent.find(concernword) != -1:
                            output[keyword]['neg'].append(sent)
                            output[keyword]['neg_seg'].append(review)
                            output[keyword]['neg_descriptor'].append(concernword)

            temp_pos = []
            for i in dic_for_partition[keyword]['pos']:
                # print(tp.cut_sentence_2(rawdata.ix[i,1]))
                #去重
                if self.tp.cut_sentence_2(rawdata.ix[i, 0]) not in temp_pos:
                    temp_pos.append(self.tp.cut_sentence_2(rawdata.ix[i, 0]))

            for idx, review in enumerate(temp_pos):
                for sent in review:
                    for concernword in concernword_dict[keyword]:
                        if sent.find(concernword) != -1:
                            output[keyword]['pos'].append(sent)
                            output[keyword]['pos_seg'].append(review)
                            output[keyword]['pos_descriptor'].append(concernword)
        return output

    def save_csv(self,output):
        #写入csv输出
        writer = csv.writer(open(self.output_for_spark,'w'),lineterminator='\n')
        for keyword in output:
            for idx in range(len(output[keyword]['pos'])):
                writer.writerow((keyword,'pos',output[keyword]['pos_descriptor'][idx],output[keyword]['pos'][idx],output[keyword]['pos_seg'][idx]))
            for idx in range(len(output[keyword]['neg'])):
                writer.writerow((keyword, 'neg',output[keyword]['neg_descriptor'][idx], output[keyword]['neg'][idx], output[keyword]['neg_seg'][idx]))
        # print(pd.DataFrame(output))
        # pd.DataFrame(output).to_csv('D:/need_1.csv')

    # 对打完分分好类的关注点词频进行统计
    def sentimented_seg_concernword_analysis(self,output,top_num=5):
        pos_set =[]
        neg_set =[]
        for keyword in output:
            pos_set.append([keyword,len(output[keyword]['pos'])])
            neg_set.append([keyword,len(output[keyword]['neg'])])
        pos_set = sorted(pos_set,key=lambda x: x[1],reverse=True)
        neg_set = sorted(neg_set,key=lambda x: x[1],reverse=True)
        pos_sum = sum([x[1] for x in pos_set])
        neg_sum = sum([x[1] for x in neg_set])
        for i in pos_set[:top_num]:
            print('%s: %d,%.4f'%(i[0],i[1],i[1]/pos_sum))
        print('neg')
        for i in neg_set[:top_num]:
            print('%s: %d,%.4f'%(i[0],i[1],i[1]/neg_sum))




# input_transform = Text_Processing()
# input_transform.file_to_input(r'C:\Users\Data\Desktop\高露洁_ForJack.csv','C:/Users/Data/Desktop/source.csv')
t1 = time.time()
for_test = Sentiment_seg('C:/Users/Data/Desktop/score_for_quency.csv',r'C:\Users\Data\Desktop\高露洁_ForJack.csv','seg','C:/Users/Data/Desktop/input_for_quency_final.csv')
output = for_test.get_sentiment_seg()
# print(output)
for_test.save_csv(output)
for_test.sentimented_seg_concernword_analysis(output)
t2 = time.time()
print('消耗时间%d'%(t2-t1))