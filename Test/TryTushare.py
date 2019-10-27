#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
import numpy as np

# print(ts.__version__)

ts.set_token('22e74c8e4523bb24f26bcd5706617b2059c0e4e0f7f9df3559c5b000')
pro = ts.pro_api()
# ICBC = tushare.get_k_data(code='601398',start='20180101',end='20181008',ktype='D')
# ICBC = ts.get_k_data('601398',start='2018-01-01',end='2018-10-08',ktype='D'
'''''''''
# ICBC = pro.daily(ts_code='601398.SH', start_date='20180701', end_date='20180718')
SCYY = pro.daily(ts_code='300144.SZ', start_date='20180701', end_date='20180718')
# print(ts.top_list('2010-01-19'))
# print(ts.get_k_data())
# print(ICBC)
print(SCYY,type(SCYY))
'''''''''
data = pro.query('stock_basic', exchange='', list_status='L',fields='ts_code,symbol,name,area,industry,list_date,exchange,curr_type,is_hs')

print(data,type(data))
data1 = data.loc[data['name']=='宋城演艺']
print(data1)

code = str(data1['ts_code'].values[0])
# 首先data.value实际返回了一个list，用list的选取【0】之后在str，就变成了字符。
# code = str(code)
print(code,type(code))

Stock_daily = pro.daily(ts_code=code, start_date='20180701', end_date='20180718')
# Stock_daily1 = pro.daily(ts_code='300144.SZ', start_date='20180701', end_date='20180718')
print(Stock_daily)

# help()