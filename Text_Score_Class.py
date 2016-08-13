import csv
import numpy as np
from Load_Data_Class import Load_Sentiment_Dict
from Load_Data_Class import Text_Processing


class Text_Score():

    def __init__(self,rawdata_file,score_file,seg_file):
        self.seg_file = seg_file
        self.rawdata_file = rawdata_file
        self.score_file = score_file
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
        self.mostdict = Data_Load.get_txt_data('D:/project_reviews_analysis/Sentiment dictionary features/most.txt', 'lines')
        self.verydict = Data_Load.get_txt_data('D:/project_reviews_analysis/Sentiment dictionary features/very.txt', 'lines')
        self.moredict = Data_Load.get_txt_data('D:/project_reviews_analysis/Sentiment dictionary features/more.txt', 'lines')
        self.ishdict = Data_Load.get_txt_data('D:/project_reviews_analysis/Sentiment dictionary features/ish.txt', 'lines')
        self.insufficientdict = Data_Load.get_txt_data(
            'D:/project_reviews_analysis/Sentiment dictionary features/insufficiently.txt', 'lines')
        self.inversedict = Data_Load.loadDict(u"sentimentDict/否定词语.txt", -1)

        self.sentiment_stopwords = Data_Load.get_txt_data('D:/project_reviews_analysis/Preprocessing module/sentiment_stopword.txt',
                                           'lines')
    def match(self,word, sentiment_value):
        if word in self.mostdict:
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

    def sentence_sentiment_score(self,file):
        reader = csv.reader(open(file, 'r'))
        cuted_review = []
        for cell in reader:
            if len(cell[1]) != 0:
                cuted_review.append(self.tp.cut_sentence_2(cell[1]))
        single_review_count = []
        all_review_count = []
        for review in cuted_review:
            for sent in review:
                seg_sent = self.tp.segmentation(sent, 'list')
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
            #print(single_review_count)
            all_review_count.append(
                single_review_count)  # [[[s11_score], [s12_score], ...], [[s21_score], [s22_score], ...], ...]
            single_review_count = []

        return all_review_count

    def all_review_sentiment_score(self,senti_score_list):
        score = []
        for review in senti_score_list:
            score_array = np.array(review)
            Pos = np.sum(score_array[:, 0])
            Neg = np.sum(score_array[:, 1])
            AvgPos = np.mean(score_array[:, 0])
            AvgNeg = np.mean(score_array[:, 1])
            StdPos = np.std(score_array[:, 0])
            StdNeg = np.std(score_array[:, 1])
            score.append([Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg])
        return score

    def store_sentiment_dictionary_score(self):
        sentiment_score = self.all_review_sentiment_score(self.sentence_sentiment_score(self.rawdata_file))

        f = csv.writer(open(self.score_file, 'w'), lineterminator='\n')
        for i in sentiment_score:
            f.writerow((str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]), str(i[5])))


    def get_seg_output(self):
        reader = csv.reader(open(self.rawdata_file, 'r'))
        cuted_review = []
        for cell in reader:
            if len(cell[1]) != 0:
                cuted_review.append(self.tp.cut_sentence_2(cell[1]))

                
        writer =csv.writer(open(self.seg_file,'w'),lineterminator='\n')
        for review in cuted_review:
            temp = []
            for sent in review:
                seg_sent = self.tp.segmentation(sent, 'list')
                temp.extend([word for word in seg_sent if word not in self.sentiment_stopwords and word != ' '])
            #print(temp)
            writer.writerow((temp,))




#test = Text_Score('D:/测试数据/test_1.csv', 'D:/测试数据/result_1_copy.csv')
#test.store_sentiment_dictionary_score()
#test.get_seg_output('D:/测试数据/seg_1.csv')


