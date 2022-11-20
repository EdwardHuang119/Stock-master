#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Test.TryTensentCloud import *
import datetime as dt
import pandas as pd

show = True
show_func = print if show else lambda a: a


def get_data(ts_code,start_date,end_date):
    engine = connect_db_engine()
    starttime = dt.datetime.now()
    print('%s开始获取数据'%(starttime))
    # sql = """select * from stock_china_daily where trade_date >= '2020-01-01'"""
    if type(ts_code) == str and str(ts_code) !='':
        sql= "select * from stock_china_daily where ts_code = '%s' and trade_date between '%s' and '%s' union  select * from stock_china_daily_1 where ts_code = '%s' and trade_date between '%s' and '%s' order by trade_date" % (
        ts_code, start_date, end_date, ts_code, start_date, end_date)
        print(sql)
        # exit()
        # sql = "select * from stock_china_daily where ts_code = '%s' and trade_date between '%s' and '%s'" %(ts_code,start_date,end_date)
    elif type(ts_code) == list:
        ts_code_tuple = tuple(ts_code)
        sql = "select * from stock_china_daily where ts_code in %s and trade_date between '%s' and '%s' union select * from stock_china_daily_1 where ts_code in %s and trade_date between '%s' and '%s' order by trade_date" % (ts_code_tuple, start_date, end_date,ts_code_tuple, start_date, end_date)
    elif type(ts_code) == str and str(ts_code) =='':
        sql = "select * from stock_china_daily where trade_date between '%s' and '%s' union select * from stock_china_daily_1 where trade_date between '%s' and '%s'" % (start_date, end_date,start_date, end_date)
    df = pd.read_sql_query(sql, engine)
    engine.dispose()
    endtime = dt.datetime.now()
    print('%s数据已经获取'%(endtime))
    return df

if __name__ == "__main__":
    df = get_data('600000.sh','2008-01-01','2022-01-01')
    show_func(df)