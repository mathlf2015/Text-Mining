import pandas as pd
df_train = pd.read_csv(r'E:\mydata\loan\train_u6lujuX_CVtuZ9i.csv')
df_test = pd.read_csv(r'E:\mydata\loan\test_Y3wMUE5_7gLdaTN.csv')
df_train['Loan_Status'] = df_train['Loan_Status'].map({'Y':1,'N':0}).astype(int)
full = pd.concat((df_train,df_test))
print(full.info())
full.index = range(len(full))
train_index = full[~full['Loan_Status'].isnull()].index
test_index = full[full['Loan_Status'].isnull()].index
y = full.Loan_Status.values[train_index]
del full['Loan_Status']

full[['Dependents','Gender','Married','Self_Employed']] = full[['Dependents','Gender','Married','Self_Employed']].fillna('empty')

full['LoanAmount'] = full.groupby(['Dependents','Self_Employed'])['LoanAmount'].apply(lambda x:x.fillna(x.median()))
full['Loan_Amount_Term'] = full.groupby(['Dependents','Self_Employed','Married'])['Loan_Amount_Term'].apply(lambda x:x.fillna(x.median()))
full['Credit_History'] =full.groupby(['Dependents','Self_Employed'])['Credit_History'].apply(lambda x:x.fillna(x.mean()))
#print(full.isnull().sum())
full = full.join(pd.get_dummies(full[['Dependents','Gender','Married','Self_Employed','Education','Property_Area']]))
full = full.drop(['Dependents','Gender','Married','Self_Employed','Education','Property_Area','Loan_ID'], axis=1)
#print(full.info())
#print(full.head())

print(u'模型建立')
from sklearn.cross_validation import train_test_split
X = full.values[train_index]
X_online = full.values[test_index]
'''X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=0)
from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier
clf = GradientBoostingClassifier(n_estimators=1000,learning_rate=0.1,max_depth=1,random_state=0)
clf.fit(X_train,y_train)
y_pred = clf.predict(X_train)
print('train score%3f'%accuracy_score(y_train,y_pred))
print('test score%3f'%clf.score(X_test,y_test))
y_online_pred = clf.predict(X_online)'''

seed = 0
'''from sklearn.linear_model import LogisticRegression
from sklearn.grid_search import GridSearchCV
import numpy as np
param = {'penalty':('l1','l2'),'C':np.logspace(-2,2,50)}
clf = LogisticRegression(random_state=seed)
gr = GridSearchCV(clf,param,scoring='accuracy',cv=10)
gr.fit(X,y)
print('best score: %s'%gr.best_score_)
y_online_pred = gr.predict(X_online)'''

from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier
param = {'max_depth':[6],'min_samples_leaf':[10]}
clf = GradientBoostingClassifier(n_estimators=10,random_state=seed)
gr = GridSearchCV(clf,param,scoring='accuracy',cv=10)
gr.fit(X,y)
print('best score: %s'%gr.best_score_)
y_online_pred = gr.predict(X_online)
upload = pd.DataFrame()
upload['Loan_ID'] = df_test['Loan_ID']
upload['Loan_Status'] = y_online_pred
upload['Loan_Status'] = upload['Loan_Status'].map({1:'Y',0:'N'})
upload.to_csv('E:/mydata/loan/upload.csv',index=False,encoding='utf-8')
