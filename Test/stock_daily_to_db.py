#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from Test.TushareProApi import Getdailyfromtscode
from Test.TryTensentCloud import connect_db
from Test.TryTensentCloud import connect_db_engine
from Test.TushareProApi import Tocsv
import datetime


show = True
show_func = print if show else lambda a: a

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    Chinadaily = Getdailyfromtscode('','20190101','20200201')
    Chinadaily['trade_date'] = pd.to_datetime(Chinadaily['trade_date'],format='%Y%m%d')
    # show_func(Chinadaily)
    # Tocsv(Chinadaily, '', '1days')
    engine = connect_db_engine()
    try:
        Chinadaily.to_sql('stock_china_daily_temp', con=engine, if_exists='replace', index=False)
    except Exception as e:
        print(e)
    print('数据已经导入临时表，共导入数据%s条' % (str(Chinadaily.shape[0])))
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
    endtime = datetime.datetime.now()
    print('All finish')
    print('从',starttime,'开始，到',endtime,'结束，耗时为',endtime-starttime,'。共导入数据',Chinadaily.shape[0],'条。')
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