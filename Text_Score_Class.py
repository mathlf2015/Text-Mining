#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/8/17 10:07
# @Author  : LuFeng
import csv
import numpy as np
from Load_Data_Class import Load_Sentiment_Dict
from Load_Data_Class import Text_Processing
import pymssql
import sys

"""这个类主要用于打分算法，分为对长句打分和对分句打分两种
注意导入词典时文件夹所在的路径可能需要修改，放在D盘下可直接运行"""
class Text_Score():

    # 通过修改参数review_id_beg,review_id_end控制选取的评论范围
    def __init__(self,review_id_beg = 1,review_id_end =659967,host = '192.168.0.15',user = 'sa',password = '*****',database = 'ReviewAnalysisSystem'):

        self.review_id_beg = str(review_id_beg)
        self.review_id_end = str(review_id_end)

        # 导入了howet和ntusd情感词典及自己添加的部分词典
        Data_Load = Load_Sentiment_Dict()
        self.tp = Text_Processing()
        self.postdict = Data_Load.loadDict(u"sentimentDict/正面情感词语.txt", 1)
        Data_Load.appendDict(self.postdict, u"sentimentDict/正面评价词语.txt", 1)
        Data_Load.appendDict(self.postdict, u"sentimentDict/正面评价词语1.txt", 1)
        Data_Load.appendDict(self.postdict, u"sentimentDict/正面评价词语2.txt", 1)
        Data_Load.appendDict(self.postdict, u"D:/project_reviews_analysis/正面.txt", 1)
        Data_Load.appendDict(self.postdict, "sentimentDict/ntusd_positive.txt", 1)

        self.negdict = Data_Load.loadDict(u"sentimentDict/负面情感词语.txt", -1)
        Data_Load.appendDict(self.negdict, u"sentimentDict/负面评价词语.txt", -1)
        Data_Load.appendDict(self.negdict, "sentimentDict/ntusd_negative.txt", -1)
        Data_Load.appendDict(self.negdict, u"D:/project_reviews_analysis/负面.txt", -1)

        # 导入程度副词词典
        self.very_mostdict = Data_Load.loadDict(u'D:/project_reviews_analysis/sentimentDict/程度级别6词语.txt', 1)
        self.mostdict = Data_Load.loadDict(u'D:/project_reviews_analysis/sentimentDict/程度级别5词语.txt', 1)
        self.verydict = Data_Load.loadDict(u'D:/project_reviews_analysis/sentimentDict/程度级别4词语.txt', 1)
        self.moredict = Data_Load.loadDict(u'D:/project_reviews_analysis/sentimentDict/程度级别3词语.txt', 1)
        self.ishdict = Data_Load.loadDict(u'D:/project_reviews_analysis/sentimentDict/程度级别2词语.txt', 1)
        self.insufficientdict = Data_Load.loadDict(u'D:/project_reviews_analysis/sentimentDict/程度级别1词语.txt', 1)
        self.inversedict = Data_Load.loadDict(u"sentimentDict/否定词语.txt", -1)
        self.sentiment_stopwords = Data_Load.get_txt_data('D:/project_reviews_analysis/Preprocessing module/sentiment_stopword.txt',
                                           'lines')
        #数据库链接
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    #为情感词赋予程度副词的权重
    def match(self,word, sentiment_value):
        # print(self.verydict)
        if word in self.very_mostdict:
            sentiment_value *= 3.0
        elif word in self.mostdict:
            sentiment_value *= 2.0
        elif word in self.verydict:
            sentiment_value *= 1.5
        elif word in self.moredict:
            sentiment_value *= 1.25
        elif word in self.ishdict:
            sentiment_value *= 0.5
        elif word in self.insufficientdict:
            sentiment_value *= 0.25
        elif word in self.inversedict:
            sentiment_value *= -1
        return sentiment_value

    #将分数转化为正
    def transform_to_positive_num(self,poscount, negcount):
        pos_count = 0
        neg_count = 0
        if poscount < 0 and negcount >= 0:
            neg_count += negcount - poscount
            pos_count = 0
        elif negcount < 0 and poscount >= 0:
            pos_count = poscount - negcount
            neg_count = 0
        elif poscount < 0 and negcount < 0:
            neg_count = -poscount
            pos_count = -negcount
        else:
            pos_count = poscount
            neg_count = negcount
        return [pos_count, neg_count]


    #为长句打分，每次有新评论时，通过修改sql语句中的reviewID范围控制选取的评论（核心）
    @property
    def sentence_sentiment_score(self):
        try:
            conn = pymssql.connect(host=self.host, user=self.user, password=self.password, database=self.database, charset='UTF-8')
            cur = conn.cursor()
            cuted_review = []
            review_id = []
            # 选取数据，sql查询语句需要经常修改，通过reviewID范围控制选取的评论(已完成reviewid 1~659967)
            sql_1 = u"SELECT review,reviewID from Product_productReview WHERE reviewEmotionTag is NULL and  %s <= reviewID and reviewID <= %s"%(self.review_id_beg,self.review_id_end)
            cur.execute(sql_1)
            rows = cur.fetchall()
            conn.commit()
            for i in rows:
                # print(self.tp.cut_sentence_2(i[0]))
                cuted_review.append(self.tp.cut_sentence_2(i[0]))
                review_id.append(i[1])

            print('取出数据成功!!')
        except:
            print(u'取出数据失败!!')
            print(sys.exc_info()[1])

        # 关闭连接
        finally:
            conn.close()

        single_review_count = []
        all_review_count = []
        for review in cuted_review:
            for sent in review:
                seg_sent = self.tp.segmentation(sent,'list')
                i = 0  # word position counter
                a = 0  # sentiment word position
                poscount = 0  # count a pos word
                negcount = 0
                for word in seg_sent:
                    if word in self.postdict:
                        poscount += 1
                        for w in seg_sent[a:i]:
                            poscount = self.match(w, poscount)
                        a = i + 1

                    elif word in self.negdict:
                        negcount += 1
                        for w in seg_sent[a:i]:
                            negcount = self.match(w, negcount)
                        a = i + 1

                    elif word == '！' or word == '!':
                        for w2 in seg_sent[::-1]:
                            if w2 in self.postdict:
                                poscount += 2
                                break
                            elif w2 in self.negdict:
                                negcount += 2
                                break
                    i += 1

                single_review_count.append(
                    self.transform_to_positive_num(poscount, negcount))  # [[s1_score], [s2_score], ...]
            # print(single_review_count)
            all_review_count.append(
                single_review_count)  # [[[s11_score], [s12_score], ...], [[s21_score], [s22_score], ...], ...]
            single_review_count = []

        return all_review_count ,review_id



    #为单个分句打分
    def seg_sentence_sentiment_score(self, source):

        output = {}
        for keyword in source:
            if keyword not in output:
                output[keyword]= []
            for review in source[keyword]:
                seg_sent = self.tp.segmentation(review,'list')
                i = 0  # word position counter
                a = 0  # sentiment word position
                poscount = 0  # count a pos word
                negcount = 0
                for word in seg_sent:
                    if word in self.postdict:
                        poscount += 1
                        for w in seg_sent[a:i]:
                            poscount = self.match(w, poscount)
                        a = i + 1

                    elif word in self.negdict:
                        negcount += 1
                        for w in seg_sent[a:i]:
                            negcount = self.match(w, negcount)
                        a = i + 1

                    elif word == '！' or word == '!':
                        for w2 in seg_sent[::-1]:
                            if w2 in self.postdict:
                                poscount += 2
                                break
                            elif w2 in self.negdict:
                                negcount += 2
                                break
                    i += 1

                # print(review,self.transform_to_positive_num(poscount, negcount))
                output[keyword].append(self.transform_to_positive_num(poscount, negcount))   # {concernword1:[s11_score,s12_score..], concernword2:[s21_score,s22_score..], ...}

            # print(all_review_count)
        return output


    #得到每条评论综合得分
    def all_review_sentiment_score(self,senti_score_list):
        score = []
        for review in senti_score_list:
            if len(review)==0:
                review = [[0.,0.]]
            score_array = np.array(review)
            #print(score_array)
            Pos = np.sum(score_array[:, 0])
            Neg = np.sum(score_array[:, 1])
            #下面部分暂时不需要
            AvgPos = np.mean(score_array[:, 0])
            AvgNeg = np.mean(score_array[:, 1])
            StdPos = np.std(score_array[:, 0])
            StdNeg = np.std(score_array[:, 1])
            #汇总
            score.append([Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg])
        return score

    #得到选取评论的情感，存储得分并输出为CSV文件（用不到）
    def store_sentiment_dictionary_score(self,score_file):
        senti_score_list,review_id =self.sentence_sentiment_score
        sentiment_score = self.all_review_sentiment_score(senti_score_list)

        f = csv.writer(open(score_file, 'w'), lineterminator='\n')
        for i in sentiment_score:
            f.writerow((str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]), str(i[5])))

    #得到选取评论的情感，储存数据库（核心）
    def store_sentiment_score_database(self):
        senti_score_list, review_id = self.sentence_sentiment_score
        sentiment_score = self.all_review_sentiment_score(senti_score_list)
        print('分数汇总完成')
        # print(review_id)
        try:
            conn = pymssql.connect(host=self.host, user=self.user, password=self.password, database=self.database, charset='UTF-8')
            cur = conn.cursor()
            result=[]
            for i in range(len(sentiment_score)):
                # print(review_id[i])
                if sentiment_score [i][0] > sentiment_score [i][1]:
                    result.append((1,review_id[i]))
                else:
                    result.append((0,review_id[i]))
            # print(result)
            # 更新情感极性标签到数据库
            sql_1 = u"update Product_productReview set reviewEmotionTag = '%s' where reviewID = '%s'"
            cur.executemany(sql_1, result)
            conn.commit()
            print('更新情感极性标签成功!!')
        except:
            print(u'更新情感极性标签失败!!')
            print(sys.exc_info()[1])

        # 关闭连接
        finally:
            conn.close()


    #得到每条评论分词结果并存储（用不到）
    def get_seg_output(self,rawdata_file,seg_file):
        reader = csv.reader(open(rawdata_file, 'r'))
        cuted_review = []
        for cell in reader:
            if len(cell[1]) != 0:
                cuted_review.append(self.tp.cut_sentence_2(cell[1]))

        writer =csv.writer(open(seg_file,'w'),lineterminator='\n')
        for review in cuted_review:
            temp = []
            for sent in review:
                seg_sent = self.tp.segmentation(sent, 'list')
                temp.extend([word for word in seg_sent if word not in self.sentiment_stopwords and word != ' '])
            #print(temp)
            writer.writerow((temp,))




if __name__=='__main__':
    test = Text_Score()
    test.store_sentiment_score_database()



