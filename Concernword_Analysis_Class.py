#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/8/17 10:07
# @Author  : LuFeng
import csv
from Load_Data_Class import Text_Processing
import pymssql
import sys

"""这个类主要用于分类，通过字符串匹配将每条评论分到每个关注点下面，还有
通过分词来分类，时间成本较高，推荐选择‘str’"""

class Concernword_Analysis():
    #style参数'str'字符串匹配，'seg'分词,通过修改参数review_id_beg,review_id_end控制选取的评论范围
    def __init__(self,style,review_id_beg=1,review_id_end=2000,host = '192.168.0.15',user = 'sa',password = '*****',database = 'ReviewAnalysisSystem'):
        self.style = style
        self.tp = Text_Processing()
        self.review_id_end = str(review_id_end)
        self.review_id_beg = str(review_id_beg)
        # 数据库链接
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        #取出所需要的数据
        self.data = self.get_data()
        self.concernword_dict = self.get_my_concernword()

    #构造关键词词典
    def get_my_concernword(self):
        try:
            conn = pymssql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                   charset='UTF-8')
            cur = conn.cursor()
            result = {}
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

            print('取出关注点成功!!')
        except:
            print(u'取出关注点失败!!')
            print(sys.exc_info()[1])

        # 关闭连接
        finally:
            conn.close()
            return result

    #选取需处理的评论内容和评论ID
    def get_data(self):
        try:
            conn = pymssql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                   charset='UTF-8')
            cur = conn.cursor()
            cuted_review = []
            review_id = []
            # 选取数据，sql查询语句需要经常修改，通过reviewID范围控制选取的评论
            sql_1 = u"SELECT review,reviewID from Product_productReview WHERE reviewID>=%s and reviewID<=%s "%(self.review_id_beg,self.review_id_end)
            cur.execute(sql_1)
            rows = cur.fetchall()
            conn.commit()
            for i in rows:
                cuted_review.append(i[0])
                review_id.append(i[1])
            print('取出数据成功!!')
        except:
            print(u'取出数据失败!!')
            print(sys.exc_info()[1])

        # 关闭连接
        finally:
            conn.close()
            return cuted_review, review_id

    #分词得到和关注点相关的评论索引（时间复杂度高，不推荐）
    def get_index_seg(self, keyword):
        concernword_dict = self.concernword_dict
        review_set,review_id = self.data
        cuted_review = []
        source = []
        index_output = []
        descriptors = []
        for i in review_set:
            cuted_review.append(self.tp.cut_sentence_2(i))

        # 得到关注点索引，和包含关注点的分句
        for idx, review in zip(review_id,cuted_review):
            for sent in review:
                seg_sent = self.tp.segmentation(sent, 'list')
                for word in seg_sent:
                    # print(seg_sent)
                    if word in concernword_dict[keyword]:
                        index_output.append(idx)
                        source.append(sent)      #小分句
                        descriptors.append(word) #识别出的二级关注点

        # print(source)
        # 去除重复排序后输出
        # return sorted(list(set(index_output))),source
        # 不去除重复，不排序
        # print(index_output,source,descriptors)
        return index_output,source,descriptors


    #字符串匹配得到关注点相关的评论索引，及包含关注点的分句
    def get_index_str(self, keyword):
        concernword_dict = self.concernword_dict
        review_set, review_id = self.data
        cuted_review =[]
        source = []
        descriptors = []
        index_output = []
        for i in review_set:
            cuted_review.append(self.tp.cut_sentence_2(i))
        # 得到关注点索引，和包含关注点的分句
        for idx, review in zip(review_id, cuted_review):
            for sent in review:
                for concernword in concernword_dict[keyword]:
                    if sent.find(concernword) != -1:
                        index_output.append(idx)
                        source.append(sent)    # 小分句
                        descriptors.append(concernword)  # 识别出的二级关注点
        #print(source)
        #print(sorted(list(set(index_output))))

        #去除重复排序后输出
        # return sorted(list(set(index_output))),source
        #不去除重复，不排序
        return index_output, source,descriptors


    #输出每个一级关注点下的评论索引，分句，二级描述词
    def get_ind_dict(self):
        concernword_dict = self.concernword_dict
        ind_dict = {}
        source ={}
        descriptor_dict ={}
        for i in concernword_dict.keys():
            if self.style == 'seg':
                output,seg_output,descriptor = self.get_index_seg(i)

            elif self.style == 'str':
                output,seg_output,descriptor = self.get_index_str(i)

            if len(output) != 0:
                if i not in ind_dict:
                    ind_dict[i] = []
                    ind_dict[i].extend(output)
                else:
                    ind_dict[i].extend(output)
            if len(seg_output) != 0:
                if i not in source:
                    source[i] = []
                    source[i].extend(seg_output)
                else:
                    source[i].extend(seg_output)
            if len(descriptor) != 0:
                if i not in descriptor_dict:
                    descriptor_dict[i] = []
                    descriptor_dict[i].extend(descriptor)
                else:
                    descriptor_dict[i].extend(descriptor)
        # print(source)
        # print(ind_dict)
        return ind_dict,source,descriptor_dict


    # 关注点综合分析，及存储（初略看关注点分布）
    def get_concernword_analysis(self,file_output):
        valid_views = []
        input = self.get_ind_dict()
        ind_dict,source = input[0],input[1]
        for i in ind_dict.keys():
            valid_views.extend(ind_dict[i])

        valid_views_num = len(set(valid_views))
        #print('有效评论数%s'%valid_views_num)

        writer = csv.writer(open(file_output, 'w'), lineterminator='\n')
        writer.writerow(('有效评论数%s' % valid_views_num,))
        for i in ind_dict.keys():
            print(i,len(ind_dict[i]),len(ind_dict[i])/valid_views_num)
            writer.writerow((i, len(ind_dict[i]), len(ind_dict[i]) / valid_views_num))


if __name__=='__main__':
    test = Concernword_Analysis('str')
    test.get_concernword_analysis('D:/noneed.csv')
