# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from HP_formula import *
import tushare as ts

def RSI(N1=6, N2=12, N3=24):
    """
    RSI 相对强弱指标
    """
    LC = REF(CLOSE, 1)
    RSI1 = SMA(MAX(CLOSE - LC, 0), N1, 1) / SMA(ABS(CLOSE - LC), N1, 1) * 100
    RSI2 = SMA(MAX(CLOSE - LC, 0), N2, 1) / SMA(ABS(CLOSE - LC), N2, 1) * 100
    RSI3 = SMA(MAX(CLOSE - LC, 0), N3, 1) / SMA(ABS(CLOSE - LC), N3, 1) * 100

    return RSI1, RSI2, RSI3


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

r1,r2,r3=RSI()

mydf = mydf.join(pd.Series( r1,name='RSI1'))  
mydf = mydf.join(pd.Series( r2,name='RSI2'))  
mydf = mydf.join(pd.Series( r3,name='RSI3')) 
mydf['S80']=80  #增加上轨80轨迹线
mydf['X20']=20  #增加下轨20轨迹线

mydf=mydf.tail(100)  #显示最后100条数据线 

#下面是绘线语句
mydf.S80.plot.line()
mydf.X20.plot.line()
mydf.RSI1.plot.line(legend=True)
mydf.RSI2.plot.line(legend=True)
mydf.RSI3.plot.line(legend=True)



