from Concernword_Analysis_Class import Concernword_Analysis
import pandas as pd
from Load_Data_Class import Text_Processing
import csv
from Text_Score_Class import Text_Score
class Sentiment_seg():

    def __init__(self,score_name,rawdata_name,style):
        self.score_name = score_name
        self.rawdata_name = rawdata_name
        self.style = style
        self.tp = Text_Processing()
        self.get_score = Text_Score(self.rawdata_name,self.score_name)

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

    def get_sentiment_idx_for_seg_review(self):
        test_concernword = Concernword_Analysis(self.style, self.rawdata_name)
        ind_dict,source = test_concernword.get_ind_dict()
        temp = self.get_score.seg_sentence_sentiment_score(source)
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


    def get_sentiment_seg(self):
        test_concernword = Concernword_Analysis(self.style, self.rawdata_name, 'D:/no_need_1.csv', 'D:/no_need_2.csv')
        concernword_dict = test_concernword.get_my_concernword()
        dic_for_partition = self.get_sentiment_idx_for_seg_review()
        rawdata = pd.read_csv(self.rawdata_name, encoding='gbk')
        #print(rawdata)
        output = {}
        for keyword in dic_for_partition:
            if keyword not in output:
                output[keyword] = {}
                output[keyword]['neg'] = []
                output[keyword]['pos'] = []
                output[keyword]['neg_seg'] = []
                output[keyword]['pos_seg'] = []

            temp_neg = []
            for i in dic_for_partition[keyword]['neg']:
                # print(tp.cut_sentence_2(rawdata.ix[i,1]))
                temp_neg.append(self.tp.cut_sentence_2(rawdata.ix[i, 0]))


            for idx, review in enumerate(temp_neg):
                for sent in review:
                    for concernword in concernword_dict[keyword]:
                        if sent.find(concernword) != -1:
                            output[keyword]['neg'].append(sent)
                            output[keyword]['neg_seg'].append(review)

            temp_pos = []
            for i in dic_for_partition[keyword]['pos']:
                # print(tp.cut_sentence_2(rawdata.ix[i,1]))
                temp_pos.append(self.tp.cut_sentence_2(rawdata.ix[i, 0]))

            for idx, review in enumerate(temp_pos):
                for sent in review:
                    for concernword in concernword_dict[keyword]:
                        if sent.find(concernword) != -1:
                            output[keyword]['pos'].append(sent)
                            output[keyword]['pos_seg'].append(review)

        writer = csv.writer(open('C:/Users/Data/Desktop/input_for_quency_1.csv','w'),lineterminator='\n')
        for keyword in output:
            for idx in range(len(output[keyword]['pos'])):
                writer.writerow((keyword,'pos',output[keyword]['pos'][idx],output[keyword]['pos_seg'][idx]))
            for idx in range(len(output[keyword]['neg'])):
                writer.writerow((keyword, 'neg', output[keyword]['neg'][idx], output[keyword]['neg_seg'][idx]))
        # print(pd.DataFrame(output))
        # pd.DataFrame(output).to_csv('D:/need_1.csv')

        # return output


for_test = Sentiment_seg('C:/Users/Data/Desktop/score_for_quency.csv',r'C:\Users\Data\Desktop\高露洁_ForJack.csv','str')
for_test.get_sentiment_seg()
