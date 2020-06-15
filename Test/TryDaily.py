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
from Test.TushareProApi import Tocsv
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
start_date = '20200409'
end_date = '20200413'
period = trade_cal_list(start_date,end_date,'')
start_date = str(period[0])
end_date = str(period[-1])

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
Tocsv(chinaandhkmarket,'','Chinadaily')



