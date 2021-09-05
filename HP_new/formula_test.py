#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from HP_formula import *
from Practice.KlinePractice import *

# 试一下趋势顶底的情况。首先要选择一个一个股票的3个月的数据。作为DATA
# DATA要适当的清洗和展示。例如先获取20日的数据，然后做个日线看一下。

data = get_data('600298.SH','2021-01-01','2021-09-03')
data = data.reset_index()
data = data_clean(data)
# show_func(data.index.values)
# mpf.plot(data, type='candle', mav=(2, 5, 10), volume=True)

# 创建趋势顶底指标
# A := MA(-100 * (HHV(HIGH, 34) - CLOSE) / (HHV(HIGH, 34) - LLV(LOW, 34)), 19);
# B := -100 * (HHV(HIGH, 14) - CLOSE) / (HHV(HIGH, 14) - LLV(LOW, 14));
# D := EMA(-100 * (HHV(HIGH, 34) - CLOSE) / (HHV(HIGH, 34) - LLV(LOW, 34)), 4);
# 长期线: A + 100, COLOR9900FF;
# 短期线: B + 100, COLOR888888;
# 中期线: D + 100, COLORYELLOW, LINETHICK2;
# def HHV(data,field,period):

High= pd.Series(data['High'].values,index=data.index.values)
Low = pd.Series(data['Low'].values,index=data.index.values)
HHV_High_14 = HHV2(High,14)

LLV_Low_14 = LLV2(Low,14)
HHV_High_34 = HHV2(High,34)
LLV_Low_34 = LLV2(Low,34)

show_func(HHV_High_14)
show_func(LLV_Low_14)

QSDD=pd.concat([data['Close'],HHV_High_14,LLV_Low_14,HHV_High_34,LLV_Low_34],axis=1)
QSDD.columns = ['Close','HHV_High_14','LLV_Low_14','HHV_High_34','LLV_Low_34']
show_func(QSDD)

def shortperiod(QSDD):
    if pd.isnull(QSDD['HHV_High_14']) or pd.isnull(QSDD['LLV_Low_14']):
        shortperiod = np.nan
    else:
        shortperiod= 100+(-100*(QSDD['HHV_High_14'] - QSDD['Close'])/(QSDD['HHV_High_14']-QSDD['LLV_Low_14']))
        # show_func(shortperiod.tolist())
        # shortperiod = shortperiod.tolist()
        # shortperiod = shortperiod(0:)
        # shortperiod = pd.Series(shortperiod)
    return shortperiod,print(shortperiod),print(type(shortperiod))

# def EMA(Series, N):
#     var=pd.Series.ewm(Series, span=N, min_periods=N - 1, adjust=True).mean()
#     if N>0:
#         var[0]=0
#         #y=0
#         a=2.00000000/(N+1)
#         for i in range(1,N):
#             y=pd.Series.ewm(Series, span=i, min_periods=i - 1, adjust=True).mean()
#             y1=a*Series[i]+(1-a)*y[i-1]
#             var[i]=y1
#     return var

def longperiod(QSDD):
    out= {}
    if pd.isnull(QSDD['HHV_High_34']) or pd.isnull(QSDD['LLV_Low_34']):
        midperiod = np.nan
        langperiod = np.nan
    else:
        mid_S=(-100*(QSDD['HHV_High_34']-QSDD['Close'])/(QSDD['HHV_High_34'] - QSDD['LLV_Low_34']))
        mid_S=pd.Series(mid_S)
        # print(type(mid_S))
        mid_S =EMA2(mid_S,4)
        midperiod = mid_S+100
        lang_S =(-100 * (QSDD['HHV_High_34'] - QSDD['Close']) / (QSDD['HHV_High_34'] - QSDD['LLV_Low_34']))
        lang_S = pd.Series(lang_S)
        lang_S=MA(lang_S,19)
        langperiod =lang_S+100
    out['midperiod'] = midperiod
    out['langperiod'] = langperiod
    return pd.Series(out),print(out)

# QSDD=shortperiod(QSDD)
# QSDD['shortperiod'] = QSDD.apply(shortperiod,axis=1)
# QSDD[['midperiod','langperiod']] = QSDD.apply(longperiod,axis=1)
# Tocsv(QSDD,'','QSDD_TEST')
show_func(QSDD)