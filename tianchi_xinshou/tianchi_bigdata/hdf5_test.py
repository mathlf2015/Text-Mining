import h5py
import pandas as pd
import numpy as np
def get_date(i):
    output =[]
    f = pd.read_csv('E:/mydata/fresh_comp_offline/data_summary_concat.csv',chunksize=1000000)
    for each in f:
        output.append(each[each['time']==i])
        print('ing')
    return pd.concat(output, ignore_index=True)
file = h5py.File('E:/mydata/fresh_comp_offline/data_31.h5','w')
data=get_date(31)
print(data.head(),data.info())
#30,31都命名为test
file.create_dataset('test',data=data)
file.close()
#hdf5格式的打开
file = h5py.File('E:/mydata/fresh_comp_offline/data_30.h5','r')
b=file['test'][:]
print(b.shape,b.dtype)

#快速导入大的csv文件
import h5py
import numpy as np
d = np.loadtxt('data.csv')
h = h5py.File('data.hdf5', 'w')
dset = h.create_dataset('data', data=d)