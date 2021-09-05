#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

def minperiod(QSDD):
    if pd.isnull(QSDD['HHV_High_14']) or pd.isnull(QSDD['LLV_Low_14']):
        minperiod = np.nan
    else:
        minperiod= 100+(-100*(QSDD['HHV_High_14'] - QSDD['Close'])/(QSDD['HHV_High_14']-QSDD['LLV_Low_14']))
        # minperiod = 100+minperiod
    return minperiod

QSDD['minperiod'] = QSDD.apply(minperiod,axis=1)
show_func(QSDD)