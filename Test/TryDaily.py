#!/usr/bin/env python
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
from Test.TushareProApi import GetAlltscode
from Test.TushareProApi import Getdailyfromtscode
from Test.TushareProApi import hk_hold
import tushare as ts
import pandas as pd
from pandas import Series
import sys
from configparser import ConfigParser

show = True
show_func = print if show else lambda a: a
# print(sys.platform)

# 获取一段时间的每个开盘日期。形成trade_cal_list
start_date = '20191202'
end_date = '20191215'
period = trade_cal_list(start_date,end_date)

# 首先获取A股的情况
# 首先获取全量的股票代码？？
'''
China_daily = Getdailyfromtscode('',start_date,end_date)
print(type(China_daily))
print(China_daily)
'''

# tscodelist = GetAlltscode('','','','1')
# print(tscodelist)

Chinadaily = Getdailyfromtscode('',start_date,end_date)
# 获取全部的国内市场数据
hkdaily = hk_daily('',start_date,end_date)
# 获取全部的香港市场数据
chinaandhkmarket = pd.concat([Chinadaily,hkdaily])
print(chinaandhkmarket)


# print(type(hkdaily))
'''
if sys.platform == 'win32':
    Chinadaily.to_csv('C:\\Users\\Edward & Bella\\Desktop\\stork\HK_HOLD\\Chinadaily.csv',na_rep='0',encoding='utf_8_sig')
elif sys.platform == 'darwin':
    Chinadaily.to_csv('/Users/Mac/Documents/Stock/Chinadaily.csv',na_rep='0',encoding='utf_8_sig')
if sys.platform == 'win32':
    hkdaily.to_csv('C:\\Users\\Edward & Bella\\Desktop\\stork\HK_HOLD\\hkdaily.csv',na_rep='0',encoding='utf_8_sig')
elif sys.platform == 'darwin':
    hkdaily.to_csv('/Users/Mac/Documents/Stock/hkdaily.csv',na_rep='0',encoding='utf_8_sig')
'''
if sys.platform == 'win32':
    chinaandhkmarket.to_csv('C:\\Users\\Edward & Bella\\Desktop\\stork\HK_HOLD\\chinaandhkmarket.csv',na_rep='0',encoding='utf_8_sig')
elif sys.platform == 'darwin':
    chinaandhkmarket.to_csv('/Users/Mac/Documents/Stock/chinaandhkmarket.csv',na_rep='0',encoding='utf_8_sig')

