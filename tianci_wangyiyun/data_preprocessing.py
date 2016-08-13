#内存不够跑不动
import csv
def fetch_feature(sample_filename,feature_filename):
    reader = csv.reader(open(sample_filename,'r'))
    writer = csv.writer(open(feature_filename,'w'))
###################################定义统计变量###########################################
    usr_click = dict()
    usr_buy =dict()
    usr_hide = dict()
    usr_basket =dict()
    user_item_click=dict()#(u,i)点击次数
    usr_item_hide=dict()#(u,i)收藏次数
    usr_item_shop_basket=dict()#(u,i)购物车次数
    #num=0
    user_item_pair=set()#(u,i)对
    usr_item_time = dict()
    usr_item_shop=dict()#(用户-item购买次数)
    for line in csv.reader(open(sample_filename,'r')):
        #print(line)
        if line ==['user_id','item_category', 'item_id','time', 'behavior_type', 'count']:
            continue
        elif line[3].find('31')<0 and line[3].find('30')<0:
            user_item_click[(line[0],line[2])]=0
            usr_item_shop[(line[0],line[2])]=0
            usr_item_shop_basket[(line[0],line[2])]=0
            usr_item_hide[(line[0],line[2])]=0
            usr_click [line[0]]=0
            usr_buy[line[0]] =0
            usr_hide[line[0]] = 0
            usr_basket[line[0]] =0
            usr_item_time[(line[0],line[2])] =set()
    for line in reader:
        #print(line)
        if line[3].find('31')<0 and line[3].find('30')<0:
            dis_day = 30-int(line[3])
            usr_item_time[((line[0],line[2]))].add(dis_day)
            if line[4]=='1':
                user_item_click[(line[0],line[2])] = user_item_click[(line[0],line[2])]+int(line[5])
                usr_click[line[0]] = usr_click[line[0]]+int(line[5])
            elif line[4]=='2':
                usr_item_hide[(line[0],line[2])] = usr_item_hide[(line[0],line[2])]+int(line[5])
                usr_hide[line[0]] = usr_hide[line[0]]+int(line[5])
            elif line[4]=='3':
                usr_item_shop_basket[(line[0],line[2])] = usr_item_shop_basket[(line[0],line[2])]+int(line[5])
                usr_basket[line[0]] = usr_basket[line[0]]+int(line[5])
            else:
                usr_item_shop[(line[0],line[2])] = usr_item_shop[(line[0],line[2])]+int(line[5])
                usr_buy[line[0]] = usr_buy[line[0]]+int(line[5])
            user_item_pair.add((line[0],line[2]))
    #print(user_item_click)
    print('half,done')
    for k in user_item_pair:
        sort_user_item_time=sorted(list(usr_item_time[k]))
        eraliest_time=sort_user_item_time[-1]
        latest_time=sort_user_item_time[0]
        writer.writerow((k[0],k[1],user_item_click[k],usr_item_hide[k],usr_item_shop_basket[k],usr_item_shop[k],usr_click[k[0]],usr_hide[k[0]],usr_basket[k[0]],usr_buy[k[0]],eraliest_time,latest_time))
fetch_feature('E:/mydata/fresh_comp_offline/data_summary_part_1.csv','E:/mydata/fresh_comp_offline/data_feature.csv')
