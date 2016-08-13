import pandas as pd
df_train = pd.read_csv('E:/mydata/edx_data/NYTimesBlogTrain.csv')
df_test = pd.read_csv('E:/mydata/edx_data/NYTimesBlogTest.csv')
#print(df_train.head())
full = pd.concat((df_train,df_test))
full.index = range(len(full))
train_index = full[~full['Popular'].isnull()].index
test_index = full[full['Popular'].isnull()].index
y = full['Popular'].values[train_index]
del full['Popular']

#提取文本中的人物，组织，城市，国家的信息
#nltk.sent_tokenize(text)将文本分成句子
#nltk.word_tokenize(sent)将句子分为每个词
#nltk.pos_tag(nltk.word_tokenize(sent))得到每个词的词性
# nltk.ne_chunk（）识别文本中的实体
import nltk
def extraEntities(text):
    entities ={}
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if type(chunk)!=tuple:
                term = str(chunk)
                term = '_'.join(' '.join(term.split('/')).split()[1::2])
                entities[term.strip()] = 1
    return ' '.join(dict(entities).keys())

full['entities'] = full.Abstract.fillna('').apply(extraEntities)
#print(full['entities'].values[:10])

full['freqHeadline'] = full.Headline.map(full.Headline.value_counts())

#得到哑变量的稀疏矩阵
from pandas.core.categorical import Categorical
from scipy.sparse import csr_matrix,hstack
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
#from_array(data, **kwargs)	Make a Categorical type from a single array-like object.
#hstack横向拼接
#可以用pandas的get_dummies实现
def sprase_dummies(categorical_values):
    categories = Categorical.from_array(categorical_values)
    N = len(categorical_values)
    row_numbers = np.arange(N,dtype = np.int)
    ones = np.ones((N,))
    return csr_matrix((ones,(row_numbers,categories.codes)))

#将摘要用词频分词
co = CountVectorizer(min_df=2,token_pattern=r'\w{1,}',stop_words='english',strip_accents='unicode',lowercase=True)
entities_dummies = co.fit_transform(full['entities'])
#将类别型变量转化为哑变量
dum_1 = sprase_dummies(full['NewsDesk'].fillna('empty'))
dum_2 = sprase_dummies(full['SectionName'].fillna('empty'))
dum_3 = sprase_dummies(full['SubsectionName'].fillna('empty'))
#将数值型变量稀疏化
num_sprase = full.loc[:,(full.dtypes != np.dtype('O')).values].to_sparse()
sparsefull = hstack((entities_dummies,num_sprase,dum_1,dum_2,dum_3),format="csr")
print(sparsefull.shape)

from sklearn.linear_model import LogisticRegression
from sklearn.grid_search import GridSearchCV

parameters = {'penalty':('l1', 'l2'), 'C':np.logspace(-2, 2, 50)}
seed = 0
clf = LogisticRegression(random_state=seed)
gr = GridSearchCV(clf, parameters, scoring="roc_auc",  cv=4)
gr.fit(sparsefull[train_index,:], y)
print ("CV score:", gr.best_score_)
pred_lr = gr.best_estimator_.predict_proba(sparsefull[test_index,:])[:,1]

from sklearn.ensemble import GradientBoostingClassifier

parameters = {'max_depth':[6], 'min_samples_leaf':[10]}

clf = GradientBoostingClassifier(n_estimators=100, random_state=seed)
gr = GridSearchCV(clf, parameters, scoring="roc_auc",  cv=4)
gr.fit(sparsefull[train_index,:].toarray(), y)
print ("CV score:", gr.best_score_)
pred_gbc = gr.best_estimator_.predict_proba(sparsefull[:,test_index])[:,1]


out = full[['UniqueID']].ix[test_index]
out['probability'] = (pred_gbc+pred_lr)/2
out.to_csv('E:/mydata/edx_data/output.csv',index=False,encoding='utf-8')






















