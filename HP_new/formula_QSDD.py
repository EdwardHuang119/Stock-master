#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from HP_formula import *
from Practice.KlinePractice import *

# 试一下趋势顶底的情况。首先要选择一个一个股票的3个月的数据。作为DATA
# DATA要适当的清洗和展示。例如先获取20日的数据，然后做个日线看一下。

# show_func(data.index.values)
# mpf.plot(data, type='candle', mav=(2, 5, 10), volume=True)

# 创建趋势顶底指标
# A := MA(-100 * (HHV(HIGH, 34) - CLOSE) / (HHV(HIGH, 34) - LLV(LOW, 34)), 19);
# B := -100 * (HHV(HIGH, 14) - CLOSE) / (HHV(HIGH, 14) - LLV(LOW, 14));
# D := EMA(-100 * (HHV(HIGH, 34) - CLOSE) / (HHV(HIGH, 34) - LLV(LOW, 34)), 4);
# 长期线: A + 100, COLOR9900FF;
# 短期线: B + 100, COLOR888888;
# 中期线: D + 100, COLORYELLOW, LINETHICK2;

def data_clean_A(data):
    data.drop(['change', 'pct_chg', 'amount', 'pre_close'], axis=1, inplace=True)
    data = data.reindex(columns=['trade_date','open', 'high', 'low', 'close', 'vol'])
    data.columns = ['Date','Open','High','Low','Close','Volume']
    pd_date = pd.DatetimeIndex(data['Date'].values)
    data['Date'] = pd_date
    data.set_index(["Date"],inplace=True)
    return data

def dataset(data):
    High = pd.Series(data['High'].values, index=data.index.values)
    Low = pd.Series(data['Low'].values, index=data.index.values)
    HHV_High_14 = HHV2(High, 14)
    LLV_Low_14 = LLV2(Low, 14)
    HHV_High_34 = HHV2(High, 34)
    LLV_Low_34 = LLV2(Low, 34)
    QSDD = pd.concat([data['Close'], HHV_High_14, LLV_Low_14, HHV_High_34, LLV_Low_34], axis=1)
    QSDD.columns = ['Close', 'HHV_High_14', 'LLV_Low_14', 'HHV_High_34', 'LLV_Low_34']
    return QSDD

def MA(Series, N):
    return pd.Series.rolling(Series, N).mean()

def shortperiod(HHV_High_14,LLV_Low_14,Close):
    HHV_High_14 = HHV_High_14.fillna(0)
    LLV_Low_14 = LLV_Low_14.fillna(0)
    shortperiod = 100 + (-100 * (HHV_High_14 - Close) / (HHV_High_14 - LLV_Low_14))
    shortperiod = shortperiod.replace([np.inf, -np.inf], np.nan)
    return shortperiod

def minperiod(HHV_High_34,LLV_Low_34,Close):
    HHV_High_34 = HHV_High_34.fillna(0)
    LLV_Low_34 = LLV_Low_34.fillna(0)
    mid_S = (-100 * (HHV_High_34 - Close) / (HHV_High_34 - LLV_Low_34))
    mid_S = pd.Series(mid_S)
    mid_S = EMA2(mid_S, 4)
    midperiod = mid_S + 100
    # midperiod.replace([np.inf, -np.inf], np.nan)
    return midperiod

def longperiod(HHV_High_34,LLV_Low_34,Close):
    HHV_High_34 = HHV_High_34.fillna(0)
    LLV_Low_34 = LLV_Low_34.fillna(0)
    lang_P =(-100 * (HHV_High_34 - Close) / (HHV_High_34 - LLV_Low_34))
    lang_S = pd.Series(lang_P)
    lang_S = lang_S.replace(np.inf, np.nan)
    test = MA(lang_S,19)
    langperiod =test+100
    return langperiod

def QSDD_perstock(stock,start_date,end_date):
    data = get_data(stock, start_date, end_date)
    data = data.reset_index()
    data = data_clean_A(data)
    show_func(data)
    QSDD = dataset(data)
    short = shortperiod(QSDD['HHV_High_14'], QSDD['LLV_Low_14'], QSDD['Close'])
    mid = minperiod(QSDD['HHV_High_34'], QSDD['LLV_Low_34'], QSDD['Close'])
    long = longperiod(QSDD['HHV_High_34'], QSDD['LLV_Low_34'], QSDD['Close'])
    QSDD['shortperiod'] = short
    QSDD['midperiod'] = mid
    QSDD['longperiod'] = long
    QSDD['ts_code'] = stock
    # show_func(QSDD.columns.values.tolist())
    QSDD = QSDD.reindex(columns=['ts_code','Close', 'HHV_High_14', 'LLV_Low_14', 'HHV_High_34', 'LLV_Low_34', 'shortperiod', 'midperiod', 'longperiod'])
    print(stock+'已经完成趋势顶底数据计算')
    return QSDD

if __name__ == "__main__":
    QSDD= QSDD_perstock('300750.SZ','2021-01-01','2021-09-20')
    Tocsv(QSDD,'','QSDD_300750')
    show_func(QSDD.tail(10))

'''
# QSDD['shortperiod'] = QSDD.apply(lambda x:shortperiod2(QSDD['HHV_High_14'],QSDD['LLV_Low_14'],QSDD['Close']),axis=1)
short = shortperiod(QSDD['HHV_High_14'],QSDD['LLV_Low_14'],QSDD['Close'])
mid= minperiod(QSDD['HHV_High_34'],QSDD['LLV_Low_34'],QSDD['Close'])
long = longperiod(QSDD['HHV_High_34'],QSDD['LLV_Low_34'],QSDD['Close'])
# show_func(longperiod)
QSDD['shortperiod'] = short
QSDD['midperiod'] = mid
QSDD['longperiod'] = long
Tocsv(QSDD,'','QSDD_TEST')

# show_func(type(QSDD.loc['2021-09-03','shortperiod']))
'''
'''
# 测试过程
High= pd.Series(data['High'].values,index=data.index.values)
Low = pd.Series(data['Low'].values,index=data.index.values)
HHV_High_14 = HHV2(High,14)
LLV_Low_14 = LLV2(Low,14)
HHV_High_34 = HHV2(High,34)
LLV_Low_34 = LLV2(Low,34)
QSDD=pd.concat([data['Close'],HHV_High_14,LLV_Low_14,HHV_High_34,LLV_Low_34],axis=1)
QSDD.columns = ['Close','HHV_High_14','LLV_Low_14','HHV_High_34','LLV_Low_34']
show_func(QSDD,QSDD.dtypes)
'''


