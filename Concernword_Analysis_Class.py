#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/8/17 10:07
# @Author  : LuFeng
import csv
from Load_Data_Class import Text_Processing
import pymssql
import sys

class Concernword_Analysis():
    #style参数'str'字符串匹配，'seg'分词
    def __init__(self,style,file_raw_data,file_output='D:/no_need_1.csv',file_part_sen_seg='D:/no_need_2.csv',concernword_file='D:/project_review/concernwords_2.csv'):
        self.file_part_sen_seg = file_part_sen_seg
        self.style = style
        self.concernword_file = concernword_file
        self.file_raw_data = file_raw_data
        self.file_output = file_output
        self.tp = Text_Processing()

    #构造关键词词典
    def get_my_concernword(self):
        reader = csv.reader(open(self.concernword_file))
        result = {}
        for line in reader:
            if line != ['category', 'categoryWord']:
                if line[0] not in result:
                    result[line[0]] = set()
                    result[line[0]].add(line[1])
                else:
                    result[line[0]].add(line[1])
        #print(result)
        return result

    #分词得到和关注点相关的评论索引
    def get_index_seg(self, keyword):
        concernword_dict = self.get_my_concernword()
        reader = csv.reader(open(self.file_raw_data, 'r'))
        cuted_review = []
        source = []
        index_output = []
        descriptors = []

        # for cell in reader:
        #     if len(cell[1]) != 0:  # 去除空评论
        #         cuted_review.append(self.tp.cut_sentence_2(cell[1]))

        # cell的索引和输入文件格式有关
        for cell in reader:
            if cell != ['Review', 'Crawler_Time', 'sku信息', 'Key_Word', '商品ID', '评论标签', '评论时间']:
                cuted_review.append(self.tp.cut_sentence_2(cell[0]))

        # 得到关注点索引，和包含关注点的分句
        for idx, review in enumerate(cuted_review):
            for sent in review:
                seg_sent = self.tp.segmentation(sent, 'list')
                for word in seg_sent:
                    if word in concernword_dict[keyword]:
                        index_output.append(idx)
                        source.append(sent)
                        descriptors.append(word) #输出增加描述词

        #print(source)
        #print(sorted(list(set(index_output))))
        # 去除重复排序后输出
        # return sorted(list(set(index_output))),source
        # 不去除重复，不排序
        return index_output,source,descriptors


    #字符串匹配得到关注点相关的评论索引，及包含关注点的分句
    def get_index_str(self, keyword):
        concernword_dict = self.get_my_concernword()
        reader = csv.reader(open(self.file_raw_data, 'r'))
        cuted_review = []
        source = []
        descriptors = []
        index_output = []

        # cell的索引和输入文件格式有关
        reader.__next__()
        for cell in reader:
            if len(cell[0]) != 0:  # 去除空评论
                cuted_review.append(self.tp.cut_sentence_2(cell[0]))

        # for cell in reader:
        #     if cell != ['Review', 'Crawler_Time', 'sku信息', 'Key_Word', '商品ID', '评论标签', '评论时间']:
        #         cuted_review.append(self.tp.cut_sentence_2(cell[0]))


        # 得到关注点索引，和包含关注点的分句
        for idx, review in enumerate(cuted_review):
            for sent in review:
                for concernword in concernword_dict[keyword]:
                    if sent.find(concernword) != -1:
                        index_output.append(idx)
                        source.append(sent)
                        descriptors.append(concernword)
        #print(source)
        #print(sorted(list(set(index_output))))

        #去除重复排序后输出
        # return sorted(list(set(index_output))),source
        #不去除重复，不排序
        return index_output, source,descriptors


    #输出关注点每个类别下的评论索引，分句，二级描述词
    def get_ind_dict(self):
        concernword_dict = self.get_my_concernword()
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


    # 关注点综合分析，及存储
    def get_concernword_analysis(self):
        valid_views = []
        ind_dict,source = self.get_ind_dict()[0],self.get_ind_dict()[1]
        for i in ind_dict.keys():
            valid_views.extend(ind_dict[i])

        valid_views_num = len(set(valid_views))
        #print('有效评论数%s'%valid_views_num)

        writer = csv.writer(open(self.file_output, 'w'), lineterminator='\n')
        writer.writerow(('有效评论数%s' % valid_views_num,))
        for i in ind_dict.keys():
            print(i,len(ind_dict[i]),len(ind_dict[i])/valid_views_num)
            writer.writerow((i, len(ind_dict[i]), len(ind_dict[i]) / valid_views_num))

        # writer = csv.writer(open(self.file_part_sen_seg, 'w'), lineterminator='\n')
        # writer.writerow(('有效评论数%s' % valid_views_num,))
        # for i in source.keys():
            # print(i, len(ind_dict[i]), len(ind_dict[i]) / valid_views_num)
            # print(i, source[i])
            # writer.writerow((i, source[i]))




        '''host = 'localhost'
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
            #print(result)
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
            conn.close()'''






# test = Concernword_Analysis('str','D:/project_review/concernwords_2.csv','D:/测试数据/test_1.csv','D:/测试数据/analysis_te_seg.csv','D:/测试数据/part_sen_seg.csv')
# test.get_concernword_analysis()
