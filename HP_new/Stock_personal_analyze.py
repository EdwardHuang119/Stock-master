#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

from formula_QSDD import *
from Test.TushareProApi import *
from Test.TryTensentCloud import *
from datetime import date
from dateutil.relativedelta import relativedelta
import datetime


Today = date.today()
start_date = date.today() + relativedelta(months=-9)


def ts_name_get(stock_basic,ts_code):
    name = stock_basic[stock_basic['ts_code']== ts_code]['name']
    # name_s = pd.merge(ts_code,stock_basic,on='ts_code',how='left',right_index=False)
    # print(name_s)
    # name = name_s['name']
    return name


# start_date = start_date.strftime('%Y%m%d')
# print(Today,start_date)

# index = index_basic()
# Tocsv(index,'','指数合集')
# show_func(index)
list_HS300 = ['000300.SH','399300.SZ']
list_SZ500 = ['000905.SH','399905.SZ']
# code_zone = index_weight(list_SZ500,'20210730','20210815','20210910')
# code_zone = index_weight('000905.SH','','20210901','20210917')
# Tocsv(code_zone,'','上证500指标')
# show_func(code_zone)

if __name__ == "__main__":
    stock_basic = pro.query('stock_basic', exchange='', list_status='L',
                                                    fields='ts_code,name')
    # show_func(stock_basic)
    code_zone = index_weight(list_SZ500, '20210730', '20210815', '20210910')
    con_code_list = code_zone['con_code'].tolist()
    # con_code_list=['000732.SZ','000738.SZ']
    show_func(con_code_list)
    code_anaylze = pd.DataFrame()
    for i in range(len(con_code_list)):
        code_anaylze_per = QSDD_perstock_withname(stock_basic,con_code_list[i],start_date,Today)
        # code_anaylze['name'] = code_anaylze.apply(lambda x: ts_name_get(stock_basic, x['ts_code']), axis=1)
        code_anaylze_per_tail = code_anaylze_per.tail(10)
        code_anaylze = pd.concat([code_anaylze, code_anaylze_per_tail], ignore_index=False)
        i=i+1
    show_func(code_anaylze)
    # code_anaylze['name'] =code_anaylze.apply(lambda x: ts_name_get(stock_basic, x['ts_code']), axis=1)
    # QSDD['name'] = QSDD.apply(lambda x: ts_name_get(stock_basic, x['ts_code']), axis=1)

    # filename= '上证500（'+str(Today)+')'
    # Tocsv(code_anaylze,'',filename)