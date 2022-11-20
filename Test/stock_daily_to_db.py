#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from Test.TushareProApi import *
from Test.TryTensentCloud import connect_db
from Test.TryTensentCloud import connect_db_engine
from Test.TushareProApi import Tocsv
import datetime


show = True
show_func = print if show else lambda a: a

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    # 首先获取一下数据库连接
    engine = connect_db_engine()
    # 获取一下数据库里面最大的daily日期
    result = engine.execute("select max(trade_date) from stock_china_daily ")
    for row in result:
        startdate =row['max(trade_date)']+datetime.timedelta(days=1)
        # 从数据库找到的最大日期开始，+1天作为起始日期
        max_trade_date = row['max(trade_date)'].strftime('%Y%m%d')
        #保留一下数据库最大日期
    '''
    result2 = engine.execute("select * from trade_cal where exchange = 'SSE' and cal_date = '%s' " % (startdate))
        #获取起始日期是否是节假日
    for row in result2:
        startdate_is_open = row['is_open']
    '''
    startdate=startdate.strftime('%Y%m%d')
    # startdate = '20120101'
    time_temp =datetime.datetime.now()
    enddate = time_temp.strftime('%Y%m%d')
    # enddate = '20121231'
    show_func(trade_cal_list(startdate,enddate,'SSE'))
    if trade_cal_list(startdate,enddate,'SSE'):
        # 数据库最大日期的第二天到现在没有有任何一个交易日，则开始执行
        Chinadaily = Getdailyfromtscode('',startdate,enddate)
        Chinadaily['trade_date'] = pd.to_datetime(Chinadaily['trade_date'],format='%Y%m%d')
        try:
            engine = connect_db_engine()
            Chinadaily.to_sql('stock_china_daily_temp', con=engine, if_exists='replace', index=False)
        except Exception as e:
            print(e)
        print('数据已经导入临时表，共导入数据%s条' % (str(Chinadaily.shape[0])))
        engine.dispose()
        # exit()
        try:
            query_sql = """
                          INSERT INTO `stock_china_daily` (`ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount`)
                select
                    `ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount` from stock_china_daily_temp;
                          """
            query_sql2 = """
                    delete from stock_china_daily_temp
                """
            engine.execute(query_sql)
            print('数据已经导入到正是表')
            engine.execute(query_sql2)
            print('临时表数据已经删除')
        except Exception as ae:
            print(ae)
        engine.dispose()
        print('All finish')
        endtime = datetime.datetime.now()
        print('从',starttime,'开始，到',endtime,'结束，耗时为',endtime-starttime,'。共导入数据',Chinadaily.shape[0],'条。')
    else:
        # 1）最大日期就到现在没有任何一天需要下载数据的话
        print('截止到%s的数据已经获取完整'%(enddate))
    '''
    db, cursor = connect_db()
    for i in range(Chinadaily.shape[0]):
        try:
            c_len = Chinadaily.shape[0]
            resu0 = list(Chinadaily.iloc[c_len-1-i])
            print(resu0)
        except Exception as aa:
            print(aa)
            print('No DATA Code: ' + str(i))
            continue
        try:
            insert_sql = "INSERT INTO stock_china_daily (`ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount`) VALUES ('%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s')" % (str(resu0[0]),str(resu0[1]),float(resu0[2]),float(resu0[3]),float(resu0[4]),float(resu0[5]),float(resu0[6]),float(resu0[7]),float(resu0[8]),float(resu0[9]),float(resu0[10]))
            # print(insert_sql)
            cursor.execute(insert_sql)
            db.commit()
        except Exception as ab:
            print(ab)
            continue
    cursor.close()
    db.close()
    endtime = datetime.datetime.now()
    print('All finish')
    print('从',starttime,'开始，到',endtime,'结束，耗时为',endtime-starttime,'。共导入数据',Chinadaily.shape[0],'条。')
    '''