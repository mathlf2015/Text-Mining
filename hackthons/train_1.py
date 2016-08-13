import pandas as pd
df = pd.read_csv(r'E:\mydata\loan\train_u6lujuX_CVtuZ9i.csv')
df_test = pd.read_csv(r'E:\mydata\loan\test_Y3wMUE5_7gLdaTN.csv')
#print(df_test.isnull().sum())
print(u'数据探索')
print(df.info())
print(df.isnull().sum())
print(df.head(10))
print(df.isnull().sum())
#print(df.describe())
#print(u'删除却是记录后样本数%d'%len(df.dropna()))
print(u'记录数%d'%len(df))

print(u'数据预处理')
print(u'将特征变为数值型')
'''import matplotlib.pyplot as plt
fig,axes = plt.subplots(3,2)
df['Gender'].value_counts().plot(kind='bar',ax=axes[0,0], title='Gender')
df['Married'].value_counts().plot(kind='bar',ax = axes[0,1],title='Married')
df['Dependents'].value_counts().plot(kind='bar',ax=axes[1,0],title='Dependents')
df['Self_Employed'].value_counts().plot(kind='bar',ax=axes[1,1],title='Self_Employed')
df['LoanAmount'].hist(bins=10,ax=axes[2,0])
df['Credit_History'].plot()
plt.show()'''
#性别特征
def data_clean(data):
    df = data
    df['Gender'] = df['Gender'].fillna('Male')
    #print(df['Gender'].isnull().sum())
    #print(df.dtypes)
    #婚姻特征
    df['Married'] = df['Married'].fillna('Yes')
    #print(df.dtypes)
    #家庭人数
    df['Dependents'] = df['Dependents'].fillna('0')
    df['Self_Employed'] = df['Self_Employed'].fillna('No')
    df['LoanAmount'] = df.groupby(['Dependents','Self_Employed'])['LoanAmount'].apply(lambda x:x.fillna(x.median()))
    df['Loan_Amount_Term'] = df.groupby(['Dependents','Self_Employed','Married'])['Loan_Amount_Term'].apply(lambda x:x.fillna(x.median()))
    df['Credit_History'] = df.groupby(['Dependents','Self_Employed','Married'])['Credit_History'].apply(lambda x:x.fillna(x.median()))
    #类型装换
    df['Gender'] = df['Gender'].map({'Male':0,'Female':1}).astype(int)
    df['Married'] = df['Married'].map({'Yes':1,'No':0}).astype(int)
    df['Self_Employed'] = df['Self_Employed'].map({'Yes':1,'No':0}).astype(int)
    df['Dependents'] = df['Dependents'].map({'0':0,'1':1,'2':2,'3+':3}).astype(int)
    map_dict_p= {x:y for y,x in enumerate(df['Property_Area'].unique())}
    #print(map_dict_p)
    df['Property_Area'] = df['Property_Area'].map(map_dict_p).astype(int)
    map_dict_e = {x:y for y,x in enumerate(df['Education'].unique())}
    #print(map_dict_e)
    df['Education'] = df['Education'].map(map_dict_e).astype(int)
    #print(df.isnull().sum())
    #print(df.info())
    return df
df = data_clean(df)
df['Loan_Status'] = df['Loan_Status'].map({'Y':1,'N':0}).astype(int)
df_test = data_clean(df_test)
print(df.isnull().sum())
print(df_test.isnull().sum())

print(u'模型建立')
from sklearn.cross_validation import train_test_split
X, y = df.iloc[:, 1:-1].values, df.iloc[:, -1].values
X_online = df_test.iloc[:,1:].values
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=0)
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
'''rf = RandomForestClassifier(criterion='entropy',n_estimators=100,max_depth=3)
rf.fit(X_train,y_train)
y_pred = rf.predict(X_train)
from sklearn.svm import SVC
svm = SVC(kernel='rbf', random_state=0, gamma=0.10, C=0.8)
svm.fit(X_train, y_train)
y_pred = svm.predict(X_train)
print('test score%3f'%svm.score(X_test,y_test))
print('train score%3f'%accuracy_score(y_train,y_pred))
print('test score%3f'%rf.score(X_test,y_test))
y_online_pred = rf.predict(X_online)
upload = pd.DataFrame()
upload['Loan_ID'] = df_test['Loan_ID']
upload['Loan_Status'] = y_online_pred
upload['Loan_Status'] = upload['Loan_Status'].map({1:'Y',0:'N'})
upload.to_csv('E:/mydata/loan/upload.csv',index=False,encoding='utf-8')'''

from sklearn.ensemble import GradientBoostingClassifier
clf = GradientBoostingClassifier(n_estimators=10,learning_rate=0.1,max_depth=1,random_state=0)
clf.fit(X_train,y_train)
y_pred = clf.predict(X_train)
print('train score%3f'%accuracy_score(y_train,y_pred))
print('test score%3f'%clf.score(X_test,y_test))
y_online_pred = clf.predict(X_online)
upload = pd.DataFrame()
upload['Loan_ID'] = df_test['Loan_ID']
upload['Loan_Status'] = y_online_pred
upload['Loan_Status'] = upload['Loan_Status'].map({1:'Y',0:'N'})
upload.to_csv('E:/mydata/loan/upload.csv',index=False,encoding='utf-8')
'''import numpy as np
from sklearn.cross_validation import cross_val_score
scores = cross_val_score(estimator=clf,X=X_train,y=y_train,cv=10,n_jobs=1)
print('CV accuracy scores: %s' % scores)
print('CV accuracy: %.5f +/- %.5f' % (np.mean(scores), np.std(scores)))'''