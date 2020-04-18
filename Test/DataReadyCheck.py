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

trade_date = '20200414'
start_date = trade_date
end_date = trade_date
'''
hk_daily=hk_daily('', start_date, end_date)
if hk_daily.empty == True:
    print(start_date,"没有数据")
else:
    print(start_date,"有相关数据")
'''
hk_hold = hk_hold(start_date,'','')
if hk_hold.empty ==True:
    print(start_date,'对应沪港流通数据还不存在')
else:
    print(start_date,'对应沪港流通数据已经存在')