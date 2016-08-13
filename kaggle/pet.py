import pandas as pd
df_train = pd.read_csv('E:/mydata/kaggle/pet_pre/train.csv')
df_test = pd.read_csv('E:/mydata/kaggle/pet_pre/test.csv')
full = pd.concat((df_train,df_test))

full.index = range(len(full))
full.drop(['Name','AnimalID','ID'],axis = 1,inplace=True)
train_index = full[~full['OutcomeType'].isnull()].index
test_index = full[full['OutcomeType'].isnull()].index
y = full['OutcomeType'].values[train_index]
del full['OutcomeType'],full['OutcomeSubtype'],full['DateTime']



print(full.info())
#print(len(y))
print(full.info())
#print(full.head(3))
def age_day(age_str):
    if type(age_str)==str:
        if 'year' in age_str:
            age = int(age_str.split(' ')[0])*365
        elif 'month' in age_str:
            age = int(age_str.split(' ')[0])*30
        elif 'week' in age_str:
            age = int(age_str.split(' ')[0])*7
        elif 'day' in age_str:
            age = int(age_str.split(' ')[0])
    else:
        age = 0
    return  age
full['AgeuponOutcome'] = full['AgeuponOutcome'].apply(age_day)
#Lhasa Apso/Miniature Poodle
def text_clean (text):
    return  ' '.join(text.split('/'))
#print(text_clean('Lhasa Apso/Miniature Poodle'))
full['Color'] = full['Color'].apply(text_clean)
full['Breed'] = full['Breed'].apply(text_clean)



full['SexuponOutcome']= full['SexuponOutcome'].fillna('empty')
dum_1 = pd.get_dummies(full[['AnimalType','SexuponOutcome']])
print(full.info())

full.drop(['AnimalType','SexuponOutcome'],inplace=True,axis=1)
from sklearn.feature_extraction.text import CountVectorizer

co = CountVectorizer(token_pattern=r'\w{1,}',stop_words='english',strip_accents='unicode',lowercase=True)
dum_2 =pd.DataFrame(  co.fit_transform(full['Breed']).toarray())
dum_3 =pd.DataFrame(co.fit_transform(full['Color']).toarray())
full.drop(['Breed','Color'],inplace=True,axis=1)
full =pd.concat((full,dum_1,dum_2,dum_3),axis=1)

print(full.isnull().sum())

from sklearn.linear_model import LogisticRegression
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import LabelEncoder
import numpy as np
X = full.values[train_index,:]
X_online = full.values[test_index,:]
class_le = LabelEncoder()
y = class_le.fit_transform(y)
print(y)
seed =0
param = {'penalty':('l1','l2'),'C':np.logspace(-2,2,50)}
clf = LogisticRegression(random_state=seed)
gr = GridSearchCV(clf,param,scoring='accuracy',cv=5)
gr.fit(X,y)
print('best score: %s'%gr.best_score_)


