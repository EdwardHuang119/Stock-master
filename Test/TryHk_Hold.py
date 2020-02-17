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
from Test.TushareProApi import hk_hold
import tushare as ts
import pandas as pd
import sys
from configparser import ConfigParser


show = True
show_func = print if show else lambda a: a
# print(sys.platform)

# 获取一段时间的每个开盘日期。形成trade_cal_list
start_date = '20191201'
end_date = '20200215'
period = trade_cal_list(start_date,end_date)
# show_func(period[0])

# show(period[0])
'''''''''
# 循环获取港股通的每日流入流出内容
HK_hold_DataFrame = pd.DataFrame()
for i in range(len(period)):
    HK_hold_list_per = hk_hold(period[i],'','')
    HK_hold_DataFrame = pd.concat([HK_hold_DataFrame,HK_hold_list_per])
    i=i+1
show_func(HK_hold_DataFrame.head())
HK_hold_DataFrame.to_csv('C:\\Users\\Edward & Bella\\Desktop\\stork\HK_HOLD\\HK_hold.csv',na_rep='0',encoding='utf_8_sig')
'''''''''
# 读取CSV的内容
HK_hold_Dataframe_csv = pd.read_csv('C:\\Users\\Edward & Bella\\Desktop\\stork\HK_HOLD\\HK_hold.csv')
# 将日期转化为str类型
HK_hold_Dataframe_csv['trade_date'] = HK_hold_Dataframe_csv['trade_date'].apply(str)
# 获取日期序列
# 将dataframe先把对应列转为list,之后通过set函数（list(set(list1))）进行有效值去重，之后通过sort进行排序
# show_func(HK_hold_Dataframe_csv.head())
trade_list = list(set(HK_hold_Dataframe_csv['trade_date'].tolist()))
trade_list.sort()
show_func(trade_list)
# print(trade_list[0],trade_list.index(20191202))
A= HK_hold_Dataframe_csv[(HK_hold_Dataframe_csv['ts_code']=='601607.SH')&(HK_hold_Dataframe_csv['trade_date']=='20191202')]




print(A)



# HK_hold_DataFrame_percode = HK_hold_DataFrame[HK_hold_DataFrame['ts_code'] =='600000.SH']
# vol = HK_hold_DataFrame_percode.iloc[0:1,4]
# vol2 =HK_hold_DataFrame_percode.iloc[1:2,4]
# # vol2 = HK_hold_DataFrame_percode.loc[:1,'vol']
# # Hk_vol = HK_hold_DataFrame_percode['vol']
# vol12change = vol2-vol
# show_func(vol,vol2,vol12change)

