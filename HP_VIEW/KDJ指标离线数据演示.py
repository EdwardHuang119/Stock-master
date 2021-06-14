# -*- coding: utf-8 -*-
# KDJ指标演示
import numpy as np
import pandas as pd
from HP_formula import *
#import tushare as ts
import HP_data  as ts

def KDJ(N=9, M1=3, M2=3):
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = SMA(RSV,M1,1)
    D = SMA(K,M2,1)
    J = 3*K-2*D
    return K, D, J

#首先要对数据预处理
df = ts.get_k_data('600080',ktype='D')
mydf=df.copy()
CLOSE=mydf['close']
LOW=mydf['low']
HIGH=mydf['high']
OPEN=mydf['open']
VOL=mydf['volume']
C=mydf['close']
L=mydf['low']
H=mydf['high']
O=mydf['open']
V=mydf['volume']

k,d,j=KDJ()

mydf = mydf.join(pd.Series( k,name='K'))  
mydf = mydf.join(pd.Series( d,name='D'))  
mydf = mydf.join(pd.Series( j,name='J')) 
mydf['S80']=80  #增加上轨80轨迹线
mydf['X20']=20  #增加下轨20轨迹线

mydf=mydf.tail(100)  #显示最后100条数据线 

#下面是绘线语句
mydf.S80.plot.line()
mydf.X20.plot.line()
mydf.K.plot.line(legend=True)
mydf.D.plot.line(legend=True)
mydf.J.plot.line(legend=True)
