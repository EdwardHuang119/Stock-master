# -*- coding: utf-8 -*-


import Test.TushareProApi
from Test.TushareProApi import GetdatlyfromCname
from Test.TushareProApi import Getconcept_detail
from Test.TushareProApi import Getdailyfromconcept
from Test.TushareProApi import moneyflowlist
import Test.QyptTableView
from Test.QyptTableView import Dataframdatashow
from Test.TushareProApi import trade_cal
import sys
from Test.TushareProApi import Getdailyfromtscode
from Test.TushareProApi import Tocsv
from Test.TryTensentCloud import connect_db
from Test.TryTensentCloud import connect_db_engine
import pandas as pd



show = True
show_func = print if show else lambda a: a

# Chinadaily = Getdailyfromtscode('','20200508','20200508')


if __name__ == "__main__":
    Chinadaily = Getdailyfromtscode('','20200515','20200515')
    Chinadaily = Chinadaily.head()
    Chinadaily['trade_date'] = pd.to_datetime(Chinadaily['trade_date'],format='%Y%m%d')
    show_func(Chinadaily)
    # show_func(Chinadaily['trade_date'].dtype)
    # show_func(Chinadaily.dtypes)
    # show_func(len(Chinadaily))
    # show_func(Chinadaily.shape[1])
    for i in range(Chinadaily.shape[0]):
        try:
            c_len = Chinadaily.shape[0]
            resu0 = list(Chinadaily.ix[c_len-1-i])
            print(resu0)
        except Exception as aa:
            print(aa)
            print('No DATA Code: ' + str(i))
            continue
# 连接数据库
#     db,cursor = connect_db()
    # cursor.execute("SELECT VERSION()")
    # data = cursor.fetchone()
    # print("Database version : %s " % data)

    ''''
    engine = connect_db_engine()
    try:
        Chinadaily.to_sql('stock_china_daily', con=engine, if_exists='replace', index=False)
    except Exception as e:
        print(e)
    '''
    # db.close()





# daily = GetdatlyfromCname('宋城演A', '20190101', '20191002')
# conceptlist = Getdailyfromconcept('TS355', 20191009, 20191010)

# Dataframdatashow(conceptlist)
# Dataframdatashow(Getconcept_detail('TS328',''))
# Dataframdatashow(moneyflowlist(stock_list,'','20190601','20191018'))
# Dataframdatashow(moneyflowlist(stock_list,'','20190701','20191018'))
'''
# 交易日历的集合
A =trade_cal('20200101','20200215')
# show_func(type(A),A)
B =A.loc[A['is_open'] ==1]['cal_date'].tolist()
# B =B['cal_date'].tolist()
show_func(type(B),B)
'''
