#内存不够跑不动
import csv
def fetch_feature(sample_filename,feature_filename):
    reader = csv.reader(open(sample_filename,'r'))
    writer = csv.writer(open(feature_filename,'w'))
    #需要的特征
    user_item_click=dict()
    user_item_buy = dict()
    user_item_hide=dict()
    user_item_basket=dict()
    user_item_pairs=set()

    user_click=dict()
    user_buy=dict()
    user_hide=dict()
    user_basket=dict()

    item_clicked=dict()
    item_buyed=dict()
    item_hide=dict()
    item_basket=dict()
    for line in reader:
        if line==['user_id', 'item_id', 'behavior_type', 'user_geohash', 'item_category', 'time']:
            continue
        elif line[5].find('2014-12-17'):
            user_item_click[(line[0],line[1])]=0



