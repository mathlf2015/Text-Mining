import os
import jieba



class Load_Sentiment_Dict():
    def __init__(self):
        jieba.load_userdict('D:/project_reviews_analysis/usr_dict.txt')

    def inject_jeba(self,file_path):
        file_set = os.listdir(os.chdir(file_path))
        for file in file_set:
            jieba.load_userdict(file)


    def loadDict(self,fileName, score):
        wordDict = {}
        with open(fileName) as fin:
            for line in fin:
                word = line.strip()
                wordDict[word] = score
        return wordDict

    def appendDict(self,wordDict, fileName, score):
        with open(fileName) as fin:
            for line in fin:
                word = line.strip()
                wordDict[word] = score

    def loadExtentDict(self,fileName):
        extentDict = {}
        for i in range(6):
            with open(fileName + str(i + 1)+".txt") as fin :
                for line in fin:
                    word = line.strip()
                    extentDict[word] = i + 1
        return extentDict

    def get_txt_data(self,filepath, para):
        if para == 'lines':
            txt_file1 = open(filepath, 'r', encoding='utf')
            txt_tmp1 = txt_file1.readlines()
            txt_tmp2 = ''.join(txt_tmp1)
            txt_data1 = txt_tmp2.split('\n')
            txt_file1.close()
            return txt_data1
        elif para == 'line':
            txt_file2 = open(filepath, 'r', encoding='utf')
            txt_tmp = txt_file2.readline()
            txt_data2 = txt_tmp
            txt_file2.close()
            return txt_data2



class Text_Processing():
    def __init__(self):
        jieba.load_userdict('D:/project_reviews_analysis/usr_dict.txt')
        
    def cut_sentence_2(self,words):
        # words = (words).decode('utf8')
        start = 0
        i = 0  # i is the position of words
        token = 'meaningless'
        sents = []
        punt_list = ',.!?;~，。！？；～… \n'
        for word in words:
            if word not in punt_list:
                i += 1
                token = list(words[start:i + 2]).pop()
                # print token
            elif word in punt_list and token in punt_list:
                i += 1
                token = list(words[start:i + 2]).pop()
            else:
                sents.append(words[start:i + 1])
                start = i + 1
                i += 1
        if start < len(words):
            sents.append(words[start:])
        return sents

    def segmentation(self,sentence, para):
        if para == 'str':
            seg_list = jieba.cut(sentence)
            seg_result = ' '.join(seg_list)
            return seg_result
        elif para == 'list':
            seg_list2 = jieba.cut(sentence)
            seg_result2 = []
            for w in seg_list2:
                seg_result2.append(w)
            return seg_result2

