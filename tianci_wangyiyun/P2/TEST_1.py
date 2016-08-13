import pandas as pd
df_1 = pd.read_csv('E:\mydata\P2\p2_mars_tianchi_songs.csv', header=None)
#print(df.head())
print('歌手数目%d'%len(df_1.iloc[:,1].unique()))
print('歌曲数目%d'%len(df_1.iloc[:,0].unique()))
#song_id ,artist_id,publish_time,song_init_plays,Language,Gender
df_2= pd.read_csv('E:\mydata\P2\p2_mars_tianchi_user_actions.csv', header=None)