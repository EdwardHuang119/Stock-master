#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from Test.TushareProApi import trade_cal_list,hk_hold
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
    for row in result:
        start_date = row['max(trade_date)'] + datetime.timedelta(days=1)
    start_date = start_date.strftime('%Y%m%d')
    time_temp = datetime.datetime.now()
    end_date = time_temp.strftime('%Y%m%d')
    period = trade_cal_list(start_date, end_date, '')
    HK_hold_DataFrame = pd.DataFrame()
    if start_date == end_date:
        print('截止到%s的数据已经获取完整'%(end_date))
    else:
        for i in range(len(period)):
            HK_hold_list_per = hk_hold(period[i], '', '')
            HK_hold_DataFrame = pd.concat([HK_hold_DataFrame, HK_hold_list_per],ignore_index=True)
            print('%s的数据已经完全获取' % (period[i]))
            i = i + 1
            time.sleep(0.2)
        HK_hold_DataFrame['trade_date'] = pd.to_datetime(HK_hold_DataFrame['trade_date'], format='%Y%m%d')
        show_func(HK_hold_DataFrame.shape[0])
        show_func(HK_hold_DataFrame)
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
            print('数据已经导入到正是表')
            engine.execute(query_sql2)
            print('临时表数据已经删除')
        except Exception as ae:
            print(ae)
        engine.dispose()
        endtime = datetime.datetime.now()
        print('从', starttime, '开始，到', endtime, '结束，耗时为', endtime - starttime, '。共导入数据', HK_hold_DataFrame.shape[0], '条。')