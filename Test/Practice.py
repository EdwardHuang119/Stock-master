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



show = True
show_func = print if show else lambda a: a

# Chinadaily = Getdailyfromtscode('','20200508','20200508')


if __name__ == "__main__":
    Chinadaily = Getdailyfromtscode('','20200508','20200508')



# 连接数据库
    db,cursor = connect_db()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s " % data)
    db.close()





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

