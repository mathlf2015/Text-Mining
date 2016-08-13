#将数据分块，修改时间，对时间聚合
import pandas as pd
f = pd.read_csv('E:/mydata/fresh_comp_offline/tianchi_fresh_comp_train_user.csv')
#a = f.get_chunk()
#print(a.head(),type(a))
#a.to_csv(r'E:\mydata\fresh_comp_offline\test.csv',index=False)
'''def date_change(time):
    striped = time.split()[0]
    month,day = striped.split('-')[1],striped.split('-')[2]
    if month == '11':
        return int(day) -17
    else:
        return int(day)+13
def get_chunk_list(x):
    chunks = []
    for each in f:
        each.drop('user_geohash',axis=1,inplace=True)
        each.drop_duplicates()
        each['time'] = each['time'].map(date_change)
        chunks.append(each)
    return chunks
chunks = get_chunk_list(f)
#每次只能跑动3块
for i in range(19,22):
    fil_list = ['E:/mydata/fresh_comp_offline/data_summary_part_{}.csv'.format(str(i)) for i in range(20,23)]
    test_chunk = chunks[i]
    chunk_test = test_chunk.groupby(['user_id','item_category','item_id','time'])['behavior_type'].apply(pd.value_counts)
    chunk_test.to_csv(fil_list[i-19])
print('done')'''