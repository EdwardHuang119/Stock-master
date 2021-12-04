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

def ts_name_get(stock_basic,ts_code):
    ts_code_list = stock_basic['ts_code'].tolist()
    if ts_code in ts_code_list:
        name = stock_basic[stock_basic['ts_code']== ts_code]['name']
    else:
        name = '疑似退市股票'
    return name

def QSDD_perstock(stock,start_date,end_date):
    data = get_data(stock, start_date, end_date)
    data = data.reset_index()
    data = data_clean_A(data)
    # show_func(data)
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

def QSDD_perstock_withname(stock_basic,stock,start_date,end_date):
    data = get_data(stock, start_date, end_date)
    data = data.reset_index()
    data = data_clean_A(data)
    # show_func(data)
    QSDD = dataset(data)
    short = shortperiod(QSDD['HHV_High_14'], QSDD['LLV_Low_14'], QSDD['Close'])
    mid = minperiod(QSDD['HHV_High_34'], QSDD['LLV_Low_34'], QSDD['Close'])
    long = longperiod(QSDD['HHV_High_34'], QSDD['LLV_Low_34'], QSDD['Close'])
    QSDD['shortperiod'] = short
    QSDD['midperiod'] = mid
    QSDD['longperiod'] = long
    QSDD['ts_code'] = stock
    QSDD['name'] = QSDD.apply(lambda x: ts_name_get(stock_basic,x['ts_code']) ,axis=1)
    # show_func(QSDD.columns.values.tolist())
    QSDD = QSDD.reindex(columns=['ts_code','name','Close', 'HHV_High_14', 'LLV_Low_14', 'HHV_High_34', 'LLV_Low_34', 'shortperiod', 'midperiod', 'longperiod'])
    print(stock+'已经完成趋势顶底数据计算')
    return QSDD



# def ts_name_get(stock_basic,ts_code):
#     name = stock_basic[stock_basic['ts_code']== ts_code]['name']
#     return name

if __name__ == "__main__":
    # 测试过程，比对当日分析结果
    QSDD_data= Read_csv('中证1000（2021-12-04)','')
    date_list = list(set(QSDD_data.index.tolist()))
    date_list.sort()
    date_analys = date_list[-1]
    data_last = date_list[-2]
    # 切片出来两个新的dataframe,来标识出出来分析日和之前一天的QSDD都低于20的股票。之后分别做出来list来分析
    # 经过分析，决定直接取两个list，一个是分析日的股票list清单命名位ts_code_analys，一个分析日上一日的清单命名位ts_code_last
    QSDD_data_analys = QSDD_data.loc[date_analys]
    # QSDD_date_analys_A = QSDD_data_analys.loc[(QSDD_data_analys['midperiod'] <= 20.000000) & (QSDD_data_analys['shortperiod'] <= 20.000000) & (QSDD_data_analys['longperiod'] <= 20.000000)]
    QSDD_data_before = QSDD_data.loc[data_last]
    # QSDD_date_before_A = QSDD_data_before.loc[(QSDD_data_before['midperiod'] <= 20.000000) & (QSDD_data_before['shortperiod'] <= 20.000000) & (QSDD_data_before['longperiod'] <= 20.000000)]
    # 再弄出来股票代码的列表。用列表分析出来分析日新进入的，已经没有的，和持续再里面的。
    ts_code_analys = QSDD_data_analys.loc[(QSDD_data_analys['midperiod'] <= 20.000000) & (QSDD_data_analys['shortperiod'] <= 20.000000) & (QSDD_data_analys['longperiod'] <= 20.000000)]['ts_code'].tolist()
    ts_code_last = QSDD_data_before.loc[(QSDD_data_before['midperiod'] <= 20.000000) & (QSDD_data_before['shortperiod'] <= 20.000000) & (QSDD_data_before['longperiod'] <= 20.000000)]['ts_code'].tolist()
    ts_code_in = list(set(ts_code_analys).difference(set(ts_code_last)))
    ts_code_out = list(set(ts_code_last).difference(set(ts_code_analys)))
    ts_code_maintain = list(set(ts_code_analys).intersection(set(ts_code_last)))
    ts_code_union = list(set(ts_code_analys).union(set(ts_code_last)))
    # 思路：
    # 1）创造一个dataframe，然后循环读取union的合集列表。如果在ts_code_in就买入，ts_code_out则卖出，ts_code_maintain则保持，
    # 2）纳入一个Txt的输出模块，这个模块累计输出一些内容。


    show_func(len(ts_code_in),ts_code_in)
    show_func(len(ts_code_out),ts_code_out)
    show_func(len(ts_code_maintain),ts_code_maintain)
    show_func(len(ts_code_union),ts_code_union)
    # QSDD_date_before =
    # show_func(ts_code_test)


    '''
    stock_basic = pro.query('stock_basic', exchange='', list_status='L',
                                                    fields='ts_code,name')
    name = ts_name_get(stock_basic,'600068.SH')
    show_func(name)

    # Tocsv(stock_basic, '', 'stock_basic_test')
    QSDD_1= QSDD_perstock('300750.SZ','2021-01-01','2021-09-29')
    QSDD_1['name'] = QSDD_1.apply(lambda x: ts_name_get(stock_basic,x['ts_code']),axis=1)
    QSDD_2 =QSDD_perstock('000738.SZ','2021-01-01','2021-09-29')
    QSDD_2['name'] = QSDD_2.apply(lambda x: ts_name_get(stock_basic, x['ts_code']), axis=1)
    QSDD = pd.concat([QSDD_1, QSDD_2], ignore_index=False)
    
    QSDD_1= QSDD_perstock_withname(stock_basic,'300750.SZ','2021-01-01','2021-09-29')
    # QSDD_1['name'] = QSDD_1.apply(lambda x: ts_name_get(stock_basic,x['ts_code']),axis=1)
    QSDD_2 =QSDD_perstock_withname(stock_basic,'600068.SH','2021-01-01','2021-09-29')
    # QSDD_2['name'] = QSDD_2.apply(lambda x: ts_name_get(stock_basic, x['ts_code']), axis=1)
    QSDD = pd.concat([QSDD_1, QSDD_2], ignore_index=False)

    # QSDD = QSDD_perstock('300750.SZ', '2021-01-01', '2021-09-29')
    # QSDD = QSDD_perstock_withname(stock_basic,'300750.SZ','2021-01-01','2021-10-09')
    show_func(QSDD['ts_code'])
    # name = ts_name_get(stock_basic,QSDD['ts_code'])
    # show_func(name)
    # QSDD_withname = pd.merge(QSDD,stock_basic,on='ts_code',how='left',right_index=False)
    # QSDD['name']=np.nan
    # QSDD['name'] = QSDD.apply(lambda x: ts_name_get(stock_basic,x['ts_code']),axis=1)
    show_func(QSDD)
    # Tocsv(QSDD,'','QSDD_300750')
    # show_func(QSDD.tail(10))
    '''
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


