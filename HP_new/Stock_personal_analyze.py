#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

from formula_QSDD import *
from Test.TushareProApi import *
from Test.TryTensentCloud import *
from datetime import date
from dateutil.relativedelta import relativedelta
import datetime


# end_date = date.today()+ relativedelta(days=-9)
end_date = date.today()
start_date = end_date + relativedelta(months=-9)


def ts_name_get(stock_basic,ts_code):
    name = stock_basic[stock_basic['ts_code']== ts_code]['name']
    # name_s = pd.merge(ts_code,stock_basic,on='ts_code',how='left',right_index=False)
    # print(name_s)
    # name = name_s['name']
    return name

def QSDD_any_zone(con_code_list,filename,start_date,end_date):
    stock_basic = pro.query('stock_basic', exchange='', list_status='L',
                            fields='ts_code,name')
    code_anaylze = pd.DataFrame()
    for i in range(len(con_code_list)):
        code_anaylze_per = QSDD_perstock_withname(stock_basic,con_code_list[i],start_date,end_date)
        # code_anaylze['name'] = code_anaylze.apply(lambda x: ts_name_get(stock_basic, x['ts_code']), axis=1)
        code_anaylze_per_tail = code_anaylze_per.tail(10)
        code_anaylze = pd.concat([code_anaylze, code_anaylze_per_tail], ignore_index=False)
        i=i+1
    show_func(code_anaylze)
    filename = filename+'（' + str(end_date) + ')'
    Tocsv(code_anaylze, '', filename)
    return code_anaylze

list_HS300 = ['000300.SH','399300.SZ']
list_SZ500 = ['000905.SH','399905.SZ']


if __name__ == "__main__":
    # 确定对应的分析周期
    end_date = date.today()
    start_date = end_date + relativedelta(months=-9)
    # 获取上证500的QSDD指标分析
    code_zone = index_weight(list_SZ500, '20210730', '20210815', '20210910')
    con_code_list = code_zone['con_code'].tolist()
    QSDD_any_zone(con_code_list,'上证500',start_date,end_date)
    # 对于当天的趋势顶底做个分析看看

    '''
    stock_basic = pro.query('stock_basic', exchange='', list_status='L',
                                                    fields='ts_code,name')
    # show_func(stock_basic)
    code_zone = index_weight(list_SZ500, '20210730', '20210815', '20210910')
    con_code_list = code_zone['con_code'].tolist()
    # con_code_list=['000732.SZ','000738.SZ']
    # show_func(con_code_list)
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

    filename= '上证500（'+str(Today)+')'
    Tocsv(code_anaylze,'',filename)
    '''