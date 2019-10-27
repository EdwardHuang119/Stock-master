# -*- coding: utf-8 -*-


import Test.TushareProApi

from Test.TushareProApi import GetdatlyfromCname
from Test.TushareProApi import Getconcept_detail
from Test.TushareProApi import Getdailyfromconcept
from Test.TushareProApi import moneyflowlist
import Test.QyptTableView
from Test.QyptTableView import Dataframdatashow


show = True
show_func = print if show else lambda a: a

# daily = GetdatlyfromCname('宋城演A', '20190101', '20191002')
conceptlist = Getdailyfromconcept('TS355', 20191009, 20191010)

# Dataframdatashow(conceptlist)
# Dataframdatashow(Getconcept_detail('TS328',''))
Dataframdatashow(moneyflowlist(stock_list,'','20190601','20191018'))

