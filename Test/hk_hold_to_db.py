#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from Test.TushareProApi import *
from Test.TryTensentCloud import connect_db_engine,connect_db
import pandas as pd
import time

show = True
show_func = print if show else lambda a: a

if __name__ == "__main__":
    # 港股通数据存储
    engine = connect_db_engine()
    starttime = datetime.datetime.now()
    result = engine.execute("select max(trade_date) from stock_hk_hold ")
    # 如果max(trade_date）等于当前日期，直接说截止到现在的信息都已经获取
    # 如果max(trade_date)和当前日期有差距，但到今天的所有日期都是休息日，则告知已经获取
    # 如果max(trade_date)和当前日期有差距，且中间任意有一天是交易日，则从"max(trade_date)+1"开始到当前日期
    for row in result:
        start_date = row['max(trade_date)'] + datetime.timedelta(days=1)
        # show_func(start_date, type(start_date))
        max_trade_date = row['max(trade_date)'].strftime('%Y%m%d')

    # result2 = engine.execute("select * from trade_cal where exchange = 'XHKG' and cal_date = '%s' " % (start_date))
    # for row in result2:
    #     startdate_is_open = row['is_open']
    start_date = start_date.strftime('%Y%m%d')
    time_temp = datetime.datetime.now()
    end_date = time_temp.strftime('%Y%m%d')
    period = hk_tradecal(start_date,end_date)
    # show_func(period)
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
            time.sleep(0.8)
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