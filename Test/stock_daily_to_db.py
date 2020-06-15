#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from Test.TushareProApi import Getdailyfromtscode
from Test.TryTensentCloud import connect_db
from Test.TushareProApi import Tocsv
import datetime


show = True
show_func = print if show else lambda a: a

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    Chinadaily = Getdailyfromtscode('','20200501','20200527')
    Chinadaily['trade_date'] = pd.to_datetime(Chinadaily['trade_date'],format='%Y%m%d')
    # show_func(Chinadaily)
    # Tocsv(Chinadaily, '', '1days')
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