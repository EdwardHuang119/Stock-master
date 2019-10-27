# -*- coding: utf-8 -*-
import numpy as np
import timeit
import pandas as pd
from abupy import ABuSymbolPd
from abupy import ABuMarketDrawing
import mpl_finance as mpf
import matplotlib.pyplot as plt
import platform


# np_list = np.arange(10000)

# np_list = np.ones(5)*3
# print(np_list)

# c=np.ones_like(np_list)
# print(c)

# help(np.linspace)
# np_list2 = np.linspace(0,1,10)
# print(np_list2)

# 创建一个序列并保存
# stock_cnt = 200
# view_days = 254
# stock_day_change = np.random.standard_normal((stock_cnt,view_days))
# np.save(r'C:\Users\Edward & Bella\Desktop\stork\stock_ day_ change\',stock_day_change)

if platform.system() == 'Windows':
    # 首先确认一下本机的运行环境是否是windows
    stock_day_change = np.load(r'C:\Users\Edward & Bella\Desktop\stork\stock_day_change\stock_day_change.npy')
else:
    stock_day_change = np
# print(stock_day_change)
# print(stock_day_change.shape)

# head是代表前五行的数据
# Trydataframe1 = pd.DataFrame(stock_day_change).head()
# Trydataframe2 = pd.DataFrame(stock_day_change).head(5)
# Trydataframe3 = pd.DataFrame(stock_day_change)[:5]
# print(Trydataframe3)

stock_symbols = []
for x in range(stock_day_change.shape[0]):
    stock_symbols.append('股票'+ str(x))
print(stock_symbols[:2])

# help(pd.DataFrame)
Trydataframe4 = pd.DataFrame(stock_day_change,index=stock_symbols).head(2)
days = pd.date_range('2017-01-01',periods=stock_day_change.shape[1],freq='1d')
Trydataframe5 = pd.DataFrame(stock_day_change,index=stock_symbols,columns=days).head(2)
# print(Trydataframe5)
Trydataframe6 = Trydataframe5.T
# print(Trydataframe6.head)

Trydataframe6_20 = Trydataframe6.resample('21D',how = 'mean')
# print(Trydataframe6_20)

# df_stock0=Trydataframe6['股票0']
# print(df_stock0)
# dt_stock0_draw = df_stock0.cumsum().plot()
# plt.show()

Trydataframe6_5 = Trydataframe6.resample('21D',how='ohlc')['股票0']
# print(Trydataframe6_5)
# print(Trydataframe6_5['open'])
print(Trydataframe6_5.columns)

ABuMarketDrawing.plot_candle_stick(Trydataframe6_5.index,Trydataframe6_5['open'].values,Trydataframe6_5['high'].values,Trydataframe6_5['low'].values,Trydataframe6_5['close'].values,np.random.random(len(Trydataframe6_5)),None,'stock',day_sum=False,html_bk=False,save=False)
# print(stock_day_change)
# print(stock_day_change[0:2,:5])
# tmp=stock_day_change[0:1,:5].copy()
# stock_day_change[0:2,0:5]=stock_day_change[-2:,-5:]
# print(stock_day_change[0:2,0:5],stock_day_change[-2:,-5:])
# mask = stock_day_change[0:2,0:5]>0.5
# print(mask)
# tmp_test = stock_day_change[0:2,0:5].copy()
# aa = tmp_test[mask]
# print(mask,aa)

# tmp_test = stock_day_change[-2:,-5:]
# print(tmp_test)
# tmp_test[(tmp_test>1)|(tmp_test<-1)]
# print(tmp_test)

# check = np.all(stock_day_change[:2,:5]>0)
# check2 = np.any(stock_day_change[:2,:5]>0)
# check3 = np.maximum(stock_day_change[0:2,0:5],stock_day_change[-2:,-5:])

# print(stock_day_change[:2,:5])
# print(stock_day_change[-2:,-5:]),
# print(check3)

# axis = 0 下减上，否则是右减左。
# diff1 = np.diff(stock_day_change[:2,:5])
# diff2 = np.diff(stock_day_change[:2,:5],axis=0)
# print(diff1)
# print(diff2）

# stock_day_change_four = stock_day_change[:4,:4]
# print(stock_day_change_four)
# print("最大涨幅："+format(np.max(stock_day_change_four,axis=1)))
# print("最大跌幅："+format(np.min(stock_day_change_four,axis=1)))
# print("振幅幅度："+format(np.std(stock_day_change_four,axis=1)))
# print("平均涨跌："+format(np.mean(stock_day_change_four,axis=1)))

