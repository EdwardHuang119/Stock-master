# -*- coding: utf-8 -*-

import Test.TushareProApi
from Test.TushareProApi import GetdatlyfromCname
from Test.TushareProApi import Getconcept_detail
from Test.TushareProApi import Getdailyfromconcept
from Test.TushareProApi import moneyflowlist
import Test.QyptTableView
from Test.QyptTableView import Dataframdatashow
from Test.TushareProApi import trade_cal
from Test.TushareProApi import trade_cal_list
from Test.TushareProApi import hk_daily
from Test.TushareProApi import Getdailyfromtscode
from Test.TushareProApi import hk_hold
from Test.TushareProApi import Tocsv
import tushare as ts
import pandas as pd
from pandas import Series
import sys
from configparser import ConfigParser


show = True
show_func = print if show else lambda a: a
# print(sys.platform)

# 获取一段时间的每个开盘日期。形成trade_cal_list
start_date = '20201117'
end_date = '20201124'
period = trade_cal_list(start_date,end_date,'')
start_date = str(period[0])
end_date = str(period[-1])
show_func(start_date,end_date)


# 获取到交易日期区间
# show_func(period[0])

# show(period[0])

# 循环获取港股通的每日流入流出内容
HK_hold_DataFrame = pd.DataFrame()
for i in range(len(period)):
    HK_hold_list_per = hk_hold(period[i],'','')
    HK_hold_DataFrame = pd.concat([HK_hold_DataFrame,HK_hold_list_per])
    i=i+1
# 对整个dataframe进行排序
HK_hold_DataFrame.sort_values(by=['ts_code','trade_date','exchange'],inplace=True)
Tocsv(HK_hold_DataFrame,'','HK_hold')
# show_func(HK_hold_DataFrame.head())

''''
if sys.platform == 'win32':
    HK_hold_DataFrame.to_csv('C:\\Users\\Edward & Bella\\Desktop\\stork\HK_HOLD\\HK_hold.csv',na_rep='0',encoding='utf_8_sig')
elif sys.platform == 'darwin':
    HK_hold_DataFrame.to_csv('/Users/Mac/Documents/Stock/HK_hold.csv',na_rep='0',encoding='utf_8_sig')

'''
# 整体获取一下港资持仓的变化情况，并且加入A股和H股的日线情况
# 读取CSV的内容
'''
if sys.platform == 'win32':
    HK_hold_Dataframe_csv = pd.read_csv('C:\\Users\\Edward & Bella\\Desktop\\stork\HK_HOLD\\HK_hold.csv')
elif sys.platform == 'darwin':
    HK_hold_Dataframe_csv = pd.read_csv('/Users/Mac/Documents/Stock/HK_hold.csv')
# 将日期转化为str类型
'''

HK_hold_DataFrame.insert(6,'vol_yesterday',HK_hold_DataFrame['vol'])
HK_hold_DataFrame.insert(8,'ratio_yesterday',HK_hold_DataFrame['ratio'])
Vollist = HK_hold_DataFrame['vol'].tolist()
Vollist.insert(0,0)
Vollist.pop()
# 开头新增一个0作为初始值，后面删除最尾巴数据，避免不对称
ratiolist = HK_hold_DataFrame['ratio'].tolist()
ratiolist.insert(0,0)
ratiolist.pop()
# 开头新增一个0作为初始值，后面删除最尾巴数据，避免不对称
HK_hold_DataFrame['vol_yesterday'] = Vollist
HK_hold_DataFrame['ratio_yesterday'] = ratiolist
# print(type(HK_hold_DataFrame['vol'].tolist()))


# 获取日期序列
# 将dataframe先把对应列转为list,之后通过set函数（list(set(list1))）进行有效值去重，之后通过sort进行排序
# 现将trade做成str类型
HK_hold_DataFrame['trade_date'] = HK_hold_DataFrame['trade_date'].apply(str)
# 将起始日的值上个交易日的信息赋值为0
HK_hold_DataFrame.loc[HK_hold_DataFrame['trade_date']==start_date,['vol_yesterday','ratio_yesterday']]=0


# 并入一下周期内股票的对应交易数据
Chinadaily = Getdailyfromtscode('',start_date,end_date)
# 获取全部的国内市场数据
hkdaily = hk_daily('',start_date,end_date)
# 获取全部的香港市场数据
chinaandhkmarket = pd.concat([Chinadaily,hkdaily])
HK_hold_DataFrame = pd.merge(HK_hold_DataFrame,chinaandhkmarket,on=['ts_code','trade_date'])
Tocsv(HK_hold_DataFrame,'','HK_hold_test')




if sys.platform == 'win32':
    HK_hold_Dataframe_csv = pd.read_csv('C:\\Users\\Edward & Bella\\Desktop\\stork\HK_HOLD\\HK_hold_test.csv')
elif sys.platform == 'darwin':
    HK_hold_Dataframe_csv = pd.read_csv('/Users/Mac/Documents/Stock/HK_hold_test.csv')
# show_func(HK_hold_Dataframe_csv)

HK_hold_Dataframe_csv['trade_date'] = HK_hold_Dataframe_csv['trade_date'].apply(str)
show_func(HK_hold_Dataframe_csv.head())

# 建立一个只有对应南下北上资金的股票清单
start_ratio=HK_hold_Dataframe_csv[(HK_hold_Dataframe_csv['trade_date']==start_date)]['ratio']
end_ratio=HK_hold_Dataframe_csv[HK_hold_Dataframe_csv['trade_date']==end_date]['ratio']
start_close = HK_hold_Dataframe_csv[(HK_hold_Dataframe_csv['trade_date']==start_date)]['close']
end_close = HK_hold_Dataframe_csv[(HK_hold_Dataframe_csv['trade_date']==end_date)]['close']
# show_func(end_ratio)
# 对dataframe去除重复
hk_hold_report_1 = pd.concat((HK_hold_Dataframe_csv['ts_code'],HK_hold_Dataframe_csv['name'],start_ratio),axis =1)
hk_hold_report_1.columns = ['ts_code','name','start_ratio']
hk_hold_report_1 = hk_hold_report_1.drop_duplicates('ts_code')
show_func(hk_hold_report_1.head())

hk_hold_report_2 = pd.concat((HK_hold_Dataframe_csv['ts_code'],HK_hold_Dataframe_csv['name'],end_ratio),axis =1)
hk_hold_report_2.columns = ['ts_code','name','end_ratio']
hk_hold_report_2 = hk_hold_report_2.dropna(axis=0,how='any')
show_func(hk_hold_report_2.head())

hk_hold_report_3 = pd.concat((HK_hold_Dataframe_csv['ts_code'],HK_hold_Dataframe_csv['name'],start_close),axis =1)
hk_hold_report_3.columns = ['ts_code','name','start_close']
hk_hold_report_3 = hk_hold_report_3.drop_duplicates('ts_code')
show_func(hk_hold_report_3.head())

hk_hold_report_4 = pd.concat((HK_hold_Dataframe_csv['ts_code'],HK_hold_Dataframe_csv['name'],end_close),axis =1)
hk_hold_report_4.columns = ['ts_code','name','end_close']
hk_hold_report_4 = hk_hold_report_4.dropna(axis=0,how='any')
show_func(hk_hold_report_4.head())

hk_hold_report_5 = pd.merge(hk_hold_report_1,hk_hold_report_2,on=['ts_code','name'])
hk_hold_report_5 = pd.merge(hk_hold_report_5,hk_hold_report_3,on=['ts_code','name'])
hk_hold_report_5 = pd.merge(hk_hold_report_5,hk_hold_report_4,on=['ts_code','name'])
# hk_hold_report_5 = hk_hold_report_5.dropna(axis=0,how='any')
hk_hold_report_5['ratio_change'] = hk_hold_report_5['end_ratio'] - hk_hold_report_5['start_ratio']
hk_hold_report_5['close_change'] = hk_hold_report_5['end_close'] - hk_hold_report_5['start_close']
hk_hold_report_5['ratio_change_per'] = hk_hold_report_5['ratio_change']/ hk_hold_report_5['start_ratio']
# hk_hold_report_5['ratio_change_per'] = hk_hold_report_5['close_change_per'].apply(lambda x: format(x, '.2%'))
hk_hold_report_5['close_change_per'] = hk_hold_report_5['close_change']/ hk_hold_report_5['start_close']
# hk_hold_report_5['close_change_per'] = hk_hold_report_5['close_change_per'].apply(lambda x: format(x, '.2%'))
show_func(hk_hold_report_5.head())
# show_func(hk_hold_report_5[(hk_hold_report_5['ratio_change']>0)&(hk_hold_report_5['close_change']<0)])

Tocsv(hk_hold_report_5,'','HK_hold_report(1117--1124)')

'''
trade_list = list(set(HK_hold_Dataframe_csv['trade_date'].tolist()))
trade_list.sort()
# 转为str否则日期无法读取
HK_hold_Dataframe_csv['trade_date'] = HK_hold_Dataframe_csv['trade_date'].apply(str)
A= HK_hold_Dataframe_csv[(HK_hold_Dataframe_csv['ts_code']=='601607.SH')&(HK_hold_Dataframe_csv['trade_date']==start_date)]['ratio'].values
B= HK_hold_Dataframe_csv[(HK_hold_Dataframe_csv['ts_code']=='601607.SH')&(HK_hold_Dataframe_csv['trade_date']==end_date)]['ratio'].values
print(A,B,B-A,(B-A)/A)
'''


'''
# HK_hold_DataFrame_percode = HK_hold_DataFrame[HK_hold_DataFrame['ts_code'] =='600000.SH']
# vol = HK_hold_DataFrame_percode.iloc[0:1,4]
# vol2 =HK_hold_DataFrame_percode.iloc[1:2,4]
# # vol2 = HK_hold_DataFrame_percode.loc[:1,'vol']
# # Hk_vol = HK_hold_DataFrame_percode['vol']
# vol12change = vol2-vol
# show_func(vol,vol2,vol12change)
'''
