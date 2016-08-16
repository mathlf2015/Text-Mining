from Text_Score_Class import Text_Score
from Concernword_Analysis_Class import Concernword_Analysis
import time
import jieba
import textprocessing as tp
jieba.load_userdict('D:/project_reviews_analysis/usr_dict.txt')
rawdata_set = ['D:/测试数据/test_{}.csv'.format(str(i)) for i in range(1,4)]
score_set = ['D:/测试数据/result_{}.csv'.format(str(i)) for i in range(1,4)]
analysis_seg_set = ['D:/测试数据/analysis_{}_seg.csv'.format(str(i)) for i in range(1,4)]
analysis_str_set = ['D:/测试数据/analysis_{}_str.csv'.format(str(i)) for i in range(1,4)]
seg_set = ['D:/测试数据/seg_{}.csv'.format(str(i)) for i in range(1,4)]
part_sen_seg_set = ['D:/测试数据/part_sen_seg_{}.csv'.format(str(i)) for i in range(1,4)]

'''starttime = time.time()
for idx in range(3):
    test = Text_Score(rawdata_set[idx], score_set[idx],seg_set[idx])
    test.store_sentiment_dictionary_score()
    test.get_seg_output()
    test_concernword = Concernword_Analysis('seg', rawdata_set[idx],
                                             analysis_seg_set[idx],part_sen_seg_set[idx])
    test_concernword.get_concernword_analysis()
    test_concernword = Concernword_Analysis('str', rawdata_set[idx],
                                             analysis_str_set[idx],part_sen_seg_set[idx])
    test_concernword.get_concernword_analysis()
endtime = time.time()
print('共花费时间%s'%str(endtime-starttime))'''




#简单可视化分析
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt

#质量，包装，性价比，效果，物流，价格，真假，商家信誉/服务水平
keyword_set = ['质量','包装','性价比','效果','物流','价格','真假','商家信誉/服务水平']


def get_analysis(score_name,rawdata_name,style):
    test_concernword = Concernword_Analysis(style, 'D:/project_review/concernwords_2.csv',rawdata_name, 'D:/no_need_1.csv','D:/no_need_2.csv')
    ind_dict = test_concernword.get_ind_dict()
    df = pd.read_csv(score_name,header=None)
    result =[]
    for i in keyword_set:
        #print(i)
        result.append(df.ix[ind_dict[i],[2,3]].mean().values)
    return DataFrame(result)


def get_analysis_pic(item_1_rawdata,item_1_score,item_2_rawdata,item_2_score,style):
    analysis_1 = get_analysis(item_1_score,item_1_rawdata,style)
    analysis_2 = get_analysis(item_2_score,item_2_rawdata,style)
    analysis = DataFrame()
    analysis['item_1']= analysis_1[0] - analysis_1[1]
    analysis['item_2']= analysis_2[0] - analysis_2[1]
    analysis.index =['质量','包装','性价比','效果','物流','价格','真假','商家信誉/服务水平']
    #'quality', 'packaging', 'value', 'effect', 'logistics' and' price ', 'true', 'business credit/service level'
    analysis.index =['quality', 'packaging', 'value', 'effect', 'logistics' ,' price ', 'true or false', 'service level']
    print(analysis)
    analysis.plot(kind='bar',rot=20)
    #plt.show()
    plt.savefig('D:/测试数据/analysis_%s.png'%style,dpi=400,bbox_inches='tight')

#get_analysis_pic('D:/测试数据/test_1.csv','D:/测试数据/result_1.csv','D:/测试数据/test_2.csv','D:/测试数据/result_2.csv','str')



def test(score_name,rawdata_name,style):
    test_concernword = Concernword_Analysis(style,rawdata_name, 'D:/no_need_1.csv','D:/no_need_2.csv')
    ind_dict = test_concernword.get_ind_dict()[0]
    score = pd.read_csv(score_name,header=None)
    result ={}
    temp = score.ix[:, 0] - score.ix[:, 1]
    for keyword in keyword_set:
        if keyword not in result:
            result[keyword] = {}
            result[keyword]['neg'] = []
            result[keyword]['pos'] = []
            for idx in ind_dict[keyword]:
                if temp[idx] <0 :
                    result[keyword]['neg'].append(idx)
                else:
                    result[keyword]['pos'].append(idx)
    # print(DataFrame(result))
    return result



def get_sentiment_seg(score_name,rawdata_name,style):
    test_concernword = Concernword_Analysis(style, rawdata_name, 'D:/no_need_1.csv', 'D:/no_need_2.csv')
    concernword_dict = test_concernword.get_my_concernword()
    dic_for_partition = test(score_name,rawdata_name,style)
    rawdata = pd.read_csv('D:/测试数据/test_1.csv', header=None, encoding='gbk')
    output = {}
    for keyword in dic_for_partition:
        if keyword not in output:
            output[keyword]={}
            output[keyword]['neg'] = []
            output[keyword]['pos'] = []

        temp_neg =[]
        for i in dic_for_partition[keyword]['neg']:
            # print(tp.cut_sentence_2(rawdata.ix[i,1]))
            temp_neg.append(tp.cut_sentence_2(rawdata.ix[i,1]))
        for idx, review in enumerate(temp_neg):
            for sent in review:
                for concernword in concernword_dict[keyword]:
                    if sent.find(concernword) != -1:
                        output[keyword]['neg'].append(sent)

        temp_pos = []
        for i in dic_for_partition[keyword]['pos']:
            # print(tp.cut_sentence_2(rawdata.ix[i,1]))
            temp_pos.append(tp.cut_sentence_2(rawdata.ix[i, 1]))
        for idx, review in enumerate(temp_pos):
            for sent in review:
                for concernword in concernword_dict[keyword]:
                    if sent.find(concernword) != -1:
                        output[keyword]['pos'].append(sent)

    print(output)






# get_sentiment_seg('D:/测试数据/result_1.csv','D:/测试数据/test_1.csv','str')
# test('D:/测试数据/result_1.csv','D:/测试数据/test_1.csv','str')

test = Text_Score(r'C:\Users\Data\Desktop\高露洁_ForJack.csv', 'D:/no_need_1.csv', 'D:/no_need_2.csv')
test_concernword = Concernword_Analysis('str',r'C:\Users\Data\Desktop\高露洁_ForJack.csv')
source = test_concernword.get_ind_dict()[1]
output = test.seg_sentence_sentiment_score(source)
print(output)
