#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from Test.TushareProApi import *
from Test.TryTensentCloud import connect_db_engine,connect_db
import pandas as pd
import time

show = True
show_func = print if show else lambda a: a

def start_date_get():
    result = engine.execute("select max(trade_date) from stock_hk_hold ")
    for row in result:
        start_date = row['max(trade_date)'] + datetime.timedelta(days=1)
    return start_date

def HK_data_get_all(start_date,end_date):
    period = hk_tradecal(start_date, end_date)
    # show_func(period)
    HK_hold_DataFrame = pd.DataFrame()
    if period:
        # 如果区间有值。
        for i in range(len(period)):
            HK_hold_list_per = hk_hold(period[i], '', '')
            if HK_hold_list_per.empty:
                print('%s的数据尚未允许下载。需要和源数据确认' % (period[i]))
                break
            else:
                print('%s的数据已经完全获取' % (period[i]))
            HK_hold_DataFrame = pd.concat([HK_hold_DataFrame, HK_hold_list_per], ignore_index=True)
            time.sleep(2)
            i = i + 1
        if HK_hold_DataFrame.empty:
            pass
        else:
            HK_hold_DataFrame['trade_date'] = pd.to_datetime(HK_hold_DataFrame['trade_date'], format='%Y%m%d')
            # show_func(HK_hold_DataFrame.shape[0])
            # show_func(HK_hold_DataFrame)
    else:
        print('截止到%s的数据已经获取完整' % (end_date))
    return(HK_hold_DataFrame)

def HK_data_get_daybyday(start_date,end_date):
    period = hk_tradecal(start_date, end_date)
    # show_func(period)
    HK_hold_DataFrame = pd.DataFrame()
    if period:
        # 如果区间有值。
        for i in range(len(period)):
            HK_hold_DataFrame = hk_hold(period[i], '', '')
            if HK_hold_DataFrame.empty:
                print('%s的数据尚未允许下载。需要和源数据确认' % (period[i]))
                continue
            else:
                print('%s的数据已经完全获取' % (period[i]))
                HK_hold_DataFrame['trade_date'] = pd.to_datetime(HK_hold_DataFrame['trade_date'], format='%Y%m%d')
                # show_func(HK_hold_DataFrame)
                # print('此时可以insert')
                hk_hold_insert_db(HK_hold_DataFrame)
                time.sleep(2)
            i = i + 1
    else:
        print('截止到%s的数据已经获取完整' % (end_date))
    print('截止到%s的数据已经获取完整' % (end_date))


def hk_hold_insert_db(HK_hold_DataFrame):
    try:
        HK_hold_DataFrame.to_sql('stock_temp', con=engine, if_exists='replace', index=False)
        print('导入到临时表中,共导入了%s条' % (HK_hold_DataFrame.shape[0]))
    except Exception as e:
        print(e)
    try:
        query_sql = """
                    INSERT INTO `stock_hk_hold` (`trade_date`, `ts_code`, `name`, `vol`, `ratio`, `exchange`)
                    SELECT
                    `trade_date`, `ts_code`, `name`, `vol`, `ratio`, `exchange` FROM stock_temp;
                                             """
        query_sql2 = """
                                       delete from stock_temp
                                   """
        engine.execute(query_sql)
        print('数据已经导入到正式表')
        engine.execute(query_sql2)
        print('临时表数据已经删除')
    except Exception as ae:
        print(ae)

if __name__ == "__main__":
    # 港股通数据存储
    engine = connect_db_engine()
    starttime = datetime.datetime.now()
    '''
    result = engine.execute("select max(trade_date) from stock_hk_hold ")
    # 如果max(trade_date）等于当前日期，直接说截止到现在的信息都已经获取
    # 如果max(trade_date)和当前日期有差距，但到今天的所有日期都是休息日，则告知已经获取
    # 如果max(trade_date)和当前日期有差距，且中间任意有一天是交易日，则从"max(trade_date)+1"开始到当前日期
    for row in result:
        start_date = row['max(trade_date)'] + datetime.timedelta(days=1)
        # show_func(start_date, type(start_date))
        max_trade_date = row['max(trade_date)'].strftime('%Y%m%d')
    '''
    start_date = start_date_get()
    start_date = start_date.strftime('%Y%m%d')
    # 以当前日期为截止日endd_date
    time_temp = datetime.datetime.now()
    end_date = time_temp.strftime('%Y%m%d')
    # end_date = '20220605'
    # period = hk_tradecal(start_date,end_date)
    print(start_date,end_date)
    # dataframe = HK_data_get_all(start_date,end_date)
    # show_func(period)
    HK_data_get_daybyday(start_date,end_date)
    engine.dispose()
    '''
    HK_hold_DataFrame = pd.DataFrame()
    if period:
        # 如果没有任何区间的话。
        for i in range(len(period)):
            HK_hold_list_per = hk_hold(period[i], '', '')
            if HK_hold_list_per.empty:
                print('%s的数据尚未允许下载。需要和源数据确认' % (period[i]))
                break
            else:
                print('%s的数据已经完全获取' % (period[i]))
            HK_hold_DataFrame = pd.concat([HK_hold_DataFrame, HK_hold_list_per],ignore_index=True)
            i = i + 1
            time.sleep(2)
        if HK_hold_DataFrame.empty:
            pass
        else:
            HK_hold_DataFrame['trade_date'] = pd.to_datetime(HK_hold_DataFrame['trade_date'], format='%Y%m%d')
                # show_func(HK_hold_DataFrame.shape[0])
                # show_func(HK_hold_DataFrame)
            try:
                HK_hold_DataFrame.to_sql('stock_temp', con=engine, if_exists='replace', index=False)
                print('%s到%s的数据已经导入到临时表中,共导入了%s条' %(start_date,end_date,HK_hold_DataFrame.shape[0]))
            except Exception as e:
                print(e)
            try:
                query_sql = """
                INSERT INTO `stock_hk_hold` (`trade_date`, `ts_code`, `name`, `vol`, `ratio`, `exchange`)
                SELECT
                `trade_date`, `ts_code`, `name`, `vol`, `ratio`, `exchange` FROM stock_temp;
                                         """
                query_sql2 = """
                                   delete from stock_temp
                               """
                engine.execute(query_sql)
                print('数据已经导入到正式表')
                engine.execute(query_sql2)
                print('临时表数据已经删除')
            except Exception as ae:
                print(ae)
            engine.dispose()
            endtime = datetime.datetime.now()
            print('从', starttime, '开始，到', endtime, '结束，耗时为', endtime - starttime, '。共导入数据', HK_hold_DataFrame.shape[0], '条。')
    else:
        print('截止到%s的数据已经获取完整' % (end_date))
    '''