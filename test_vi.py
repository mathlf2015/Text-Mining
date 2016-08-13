import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import plotly.plotly as py
from Concernword_Analysis_Class import Concernword_Analysis
#质量，包装，性价比，效果，物流，价格，真假，商家信誉/服务水平
keyword_set = ['质量','包装','性价比','效果','物流','价格','真假','商家信誉/服务水平']


def get_analysis(score_name,rawdata_name,style):
    test_concernword = Concernword_Analysis(style, 'D:/project_review/concernwords_2.csv',rawdata_name, 'D:/test_add.csv')
    ind_dict = test_concernword.get_ind_dict()
    df = pd.read_csv(score_name,header=None)
    result =[]
    for i in keyword_set:
        #print(i)
        result.append(df.ix[ind_dict[i],[2,3]].mean().values)
    output = DataFrame(result,index = ['quality', 'packaging', 'value', 'effect', 'logistics', ' price ', 'true or false',
                      'service level'],columns=['pos','neg'])
    output['neg'] = -output['neg']
    return output


def get_analysis_pic(item_1_rawdata,item_1_score,item_2_rawdata,item_2_score,style):
    analysis_1 = get_analysis(item_1_score,item_1_rawdata,style)
    analysis_2 = get_analysis(item_2_score,item_2_rawdata,style)
    # print(analysis_1)
    # print(analysis_2)
    analysis = pd.merge(analysis_1,analysis_2,left_index=True,right_index=True)
    analysis.columns = [['item_1','item_1','item_2','item_2'],['pos','neg','pos','neg']]
    analysis.columns.names=['item','sentiment']
    # analysis['item_1']= analysis_1[0] - analysis_1[1]
    # analysis['item_2']= analysis_2[0] - analysis_2[1]
    #analysis.index =['质量','包装','性价比','效果','物流','价格','真假','商家信誉/服务水平']
    #'quality', 'packaging', 'value', 'effect', 'logistics' and' price ', 'true', 'business credit/service level'
    #analysis.index =['quality', 'packaging', 'value', 'effect', 'logistics' ,' price ', 'true or false', 'service level']
    #print(analysis)
    analysis.plot(kind='bar',rot=20)

    plt.show()
    #plt.savefig('D:/测试数据/analysis_%s.png'%style,dpi=400,bbox_inches='tight')

#get_analysis_pic('D:/测试数据/test_1.csv','D:/测试数据/result_1.csv','D:/测试数据/test_2.csv','D:/测试数据/result_2.csv','str')

# import numpy as np
# data = DataFrame(np.arange(6).reshape((2, 3)),
#                  index=pd.Index(['Ohio', 'Colorado'], name='state'),
#                  columns=pd.Index(['one', 'two', 'three'], name='number'))
# print(data)
# result = data.stack()
# df = DataFrame({'left': result, 'right': result + 5},
#                columns=pd.Index(['left', 'right'], name='side'))
# df_1 = df.unstack('state')
#
#
# #df_1['Ohio']= -df_1['Ohio']
# print(df_1)
# df_1.plot(kind='bar',rot=20)
# plt.show()

# import plotly
# from plotly.graph_objs import Scatter, Layout
# plotly.offline.plot({
# "data": [
#     Scatter(x=[1, 2, 3, 4], y=[4, 1, 3, 7])
# ],
# "layout": Layout(
#     title="hello world"
# )
# })


import plotly
from plotly import tools
import plotly.graph_objs as go
import numpy as np
'''trace0 = go.Bar(
    x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    y=[20, 14, 25, 16, 18, 22, 19, 15, 12, 16, 14, 17],

    name='Primary Product',
    marker=dict(
        color='rgb(49,130,189)'
    )
)
trace1 = go.Bar(
    x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    y=[19, 14, 22, 14, 16, 19, 15, 14, 10, 12, 12, 16],

    name='Secondary Product',
    marker=dict(
        color='rgb(204,204,204)',
    )
)

data = [trace0, trace1]
layout = go.Layout(
    xaxis=dict(tickangle=-45),
    barmode='group',
)

fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='angled-text-bar')'''



#x = [1, 2, 3, 4]
analysis_1 = get_analysis('D:/测试数据/result_1.csv','D:/测试数据/test_1.csv','str')
analysis_2 = get_analysis('D:/测试数据/result_2.csv','D:/测试数据/test_2.csv','str')
x = ['quality', 'packaging', 'value', 'effect', 'logistics' ,' price ', 'true or false', 'service level']
trace1 = {
    'x': x,
    'y': analysis_1['pos'],
    'name': 'item_1',
    'type': 'bar',
    'marker': dict(
    color='rgb(49,130,189)')
};
trace2 = {
    'x': x,
    'y': analysis_1['neg'],
    'name': 'item_1',
    'type': 'bar',
    'marker': dict(
    color='rgb(49,130,189)')
};
trace3 = {
    'x': x,
    'y': analysis_2['pos'],
    'name': 'item_2',
    'type': 'bar',
    'marker':  dict(color='rgb(204,204,204)'
)
}

trace4 = {
    'x': x,
    'y': analysis_2['neg'],
    'name': 'item_2',
    'type': 'bar',
    'marker':  dict(color='rgb(204,204,204)')
}
fig = tools.make_subplots(1, 1)
data = [trace1, trace2];
layout = {
    'xaxis': {'title': 'sentiment'},
    'yaxis': {'title': 'attribute'},
    'barmode': 'overlay',
    'title': 'Comparison of two commodities'
};
fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 1, 1)
fig.append_trace(trace3, 1, 1)
fig['layout'].update(layout)

# data_2 = [trace3, trace4];
#plotly.offline.plot({'data': data, 'layout': layout}, filename='result.html')
plotly.offline.plot(fig, filename='result.html')



'''import plotly.plotly as py
from plotly import tools
from plotly.graph_objs import Bar, Data, Figure, Layout, Marker, Scatter

x_0 = [1, 2, 4, 6, 7, 7]
x_1 = [10, 10, 10, 10, 10, 10]
y_0 = [2, 3, 4, 2, 3, 3]

trace1 = Bar(
    x=x_0,
    marker=Marker(color='#001f3f'),
    orientation='h',
)

trace2 = Bar(
    x=x_1,
    marker=Marker(color='#0074D9'),
    orientation='h',
)

trace3 = Scatter(y=y_0)

fig = tools.make_subplots(1, 2)
fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 1, 1)
fig.append_trace(trace3, 1, 2)
fig['layout'].update(barmode='stack')
plotly.offline.plot(fig, filename='oecd-networth-saving-bar-line')'''