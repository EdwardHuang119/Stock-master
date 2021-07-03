# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from HP_formula import *
import tushare as ts

global CLOSE,LOW,HIGH,OPEN,VOL
def MACD(SHORT=12, LONG=26, M=9):
    """
    MACD 指数平滑移动平均线
    """
    DIFF = EMA(CLOSE, SHORT) - EMA(CLOSE, LONG)
    DEA = EMA(DIFF, M)
    MACD = (DIFF - DEA) * 2

    return DIFF,DEA,MACD


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

d1,d2,d3=MACD()

mydf = mydf.join(pd.Series( d1,name='DIFF'))  
mydf = mydf.join(pd.Series( d2,name='DEA'))  
mydf = mydf.join(pd.Series( d3,name='MACD')) 
mydf['S0']=0  #增加上轨80轨迹线

mydf['co1']=EMA(CLOSE, 12)
mydf['co2']= EMA(CLOSE, 26)
mydf['co3']=mydf['co1']-mydf['co2']
print(mydf)
#mydf['X20']=20  #增加下轨20轨迹线

#mydf=mydf.tail(100)  #显示最后100条数据线 

#下面是绘线语句
mydf.S0.plot.line()
#mydf.X20.plot.line()
mydf.DIFF.plot.line(legend=True)
mydf.DEA.plot.line(legend=True)
mydf.MACD.plot.line(legend=True)
