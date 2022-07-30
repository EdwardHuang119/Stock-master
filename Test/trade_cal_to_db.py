#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Test.TryTensentCloud import connect_db_engine
from Test.TushareProApi import trade_cal
import pandas as pd

show = True
show_func = print if show else lambda a: a

if __name__ == "__main__":
    engine = connect_db_engine()
    startdate = '20220101'
    enddate = '20221231'
    trade_cal_sse = trade_cal(startdate,enddate,'')
    trade_cal_hk = trade_cal(startdate,enddate,'XHKG')
    trade_cal = pd.concat([trade_cal_sse,trade_cal_hk],ignore_index=True)
    trade_cal['cal_date'] = pd.to_datetime(trade_cal['cal_date'],format='%Y%m%d')
    try:
        trade_cal.to_sql('stock_china_daily_temp', con=engine, if_exists='replace', index=False)
    except Exception as e:
        print(e)
    try:
        query_sql = """
                      insert into `trade_cal` (`cal_date`,`exchange`,`is_open`) select `cal_date`,`exchange`,`is_open` from `stock_china_daily_temp`;
                    """
        query_sql2 = """
                delete from stock_china_daily_temp
            """
        engine.execute(query_sql)
        print('数据已经导入到正式表')
        engine.execute(query_sql2)
        print('临时表数据已经删除')
    except Exception as ae:
        print(ae)
    # show_func(trade_cal)
    print('%s到%s的交易日历已经获取并存储数据库'%(startdate,enddate))
    engine.dispose()