#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
import numpy as np
from Test.QyptTableView import Dataframdatashow


ts.set_token('22e74c8e4523bb24f26bcd5706617b2059c0e4e0f7f9df3559c5b000')
pro = ts.pro_api()
show_fuck = print()

def GetTscodefromCname(cnname):
    # 通过股票中文名称获取全部的TS_code，TS_code作为后续每次选择股票的基础信息
    stock_basic = pro.query('stock_basic', exchange='', list_status='L',fields='ts_code,symbol,name,area,industry,list_date,exchange,curr_type,is_hs')
    ts_code = stock_basic.loc[stock_basic['name'] == cnname]
    # code = str(ts_code['ts_code'].values[0])
    try:
        code = str(ts_code['ts_code'].values[0])
        # raise IndexError('index 0 is out of bounds for axis 0 with size 0')
    except IndexError:
        print('大哥你看看这个股票存在不？')
    else:
        return code

def Getdailyfromtscode(ts_code,start_date,end_date):
    # 通过ts_code来获取到日线信息
    if type(ts_code) == str:
        Stock_daily = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        return (Stock_daily)
    elif type(ts_code) == list:
        Stock_daily = pd.DataFrame()
        for i in range(len(ts_code)):
            Stock_daily_per = pro.daily(ts_code=ts_code[i], start_date=start_date, end_date=end_date)
            Stock_daily = pd.concat([Stock_daily,Stock_daily_per])
            i=i+1
        return (Stock_daily)

def GetdatlyfromCname(cnname,start_date,end_date):
    # 通过中文名字来获取股票日线行情，
    ts_code = GetTscodefromCname(cnname)
    # 通过中文名来首先获取ts——code
    if ts_code == None:
        return
    else:
        Stock_daily = Getdailyfromtscode(ts_code,start_date,end_date)
        # 通过tscode和开始以及截止日期来获取日线数据
        if Stock_daily.empty:
            print('选择日期没有任何该股票数据。')
        else:
            return (Stock_daily)

def Getconcept(name):
    # 获取到概念列表或者概念具体id
    # 获取全部的概念板块
    concept = pro.concept()
    # 首先把所有的概念元素都取出来
    if name =='':
        return concept
    # 如果name不输入就是说这个人想要看所有的元素
    elif name !='':
        # 如果输入来某个名称，那就是尝试返回一下一个对应的概念id
        conceptline = concept.loc[concept['name']==name]
        try:
            concept_id = conceptline['code'].values[0]
        #     记得哦 是values哦
        except IndexError:
            print('兄弟，这个概念不存在！')
        else:
            return concept_id


def Getconcept_detail(id,ts_code):
    # 通过概念id来确认某些概念在什么股票或者某些股票在某些行业
    if id =='' and ts_code =='':
        # 两个入参不能都为空
        print('大哥，概念id或者股票名称你好歹输入点什么')
    elif id =='' and ts_code != '':
        # 通过概念id来获取股票池
        concept_detail = pro.concept_detail(ts_code = ts_code,fields = 'id,concept_name,ts_code,name')
        return concept_detail
    elif id !='' and ts_code =='':
        # 通过股票来获取一个股票有多少个概念
        concept_detail = pro.concept_detail(id = id,fields = 'id,concept_name,ts_code,name')
        return  concept_detail
    else:
        # 没必要两个参数都输入
        print('大哥，概念id和股票名称输入一个就好了。')

def Getdailyfromconcept(concept_id,start_date,end_date):
    # 通过概念id，开始日期，结束日期来获取到股票日线信息
    stock_list_df = Getconcept_detail(concept_id,'')
    stock_array = [(code, name) for code, name in zip([stock_list_df['ts_code'].values][0], [stock_list_df['name'].values][0])]
    tscode_list = [stock_list_df['ts_code'].values][0]
    # 此时是哥array，需要转一个list
    tscode_list = tscode_list.tolist()
    Stock_daily = Getdailyfromtscode(tscode_list, start_date, end_date)
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 设置value的显示长度为1000，默认为50
    pd.set_option('max_colwidth', 2000)
  # return (stock_array,tscode_list)
    # Stock_daily=pd.set_option('max_colwidth', 200)
    return Stock_daily

def index_classify(level):
    # 申银万国行业区分
    index_list = pro.index_classify(level=level, src='SW')
    return index_list

def index_member(index_code,ts_code):
#     申银万国行业成分
    if index_code == '' and ts_code == '':
        print('大哥你要不然输入一个行业分类或者输入个股票代码呗')
    elif index_code !='' and ts_code =='':
        index_member_list = pro.index_member(index_code=index_code)
        return index_member_list
    elif index_code =='' and ts_code !='':
        index_member_list = pro.index_member(ts_code=ts_code)
        return index_member_list

def trade_cal(start_date,end_date):
    # 交易日历获取
    trade_cal = pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)
    return trade_cal

def moneyflow(ts_code,trade_date,start_date,end_date):
    # 查看个股资金流向
    if ts_code == '' and trade_date !='' and start_date ==''and end_date=='':
        moneyflowperday = pro.moneyflow(trade_date = trade_date)
        # 当日所有的股票流入流出
        return moneyflowperday
    elif ts_code !='' and trade_date !='' and start_date ==''and end_date=='':
        moneyflowpercodeday = pro.moneyflow(ts_code = ts_code,trade_date = trade_date)
        # 当日单个股票的流入流出
        return moneyflowpercodeday
    elif ts_code !='' and trade_date =='' and start_date !=''and end_date !='':
        moneyflowpercodeperide = pro.moneyflow(ts_code = ts_code,start_date = start_date,end_date = end_date)
        # 时间区间的单个股票的流入流出情况
        return moneyflowpercodeperide

def moneyflowlist(ts_code,trade_date,start_date,end_date):
    if type(ts_code) == list and type(trade_date) == str and start_date =='' and end_date =='':
        # 一个股票池和一个日期
        moneyflowpf =pd.DataFrame()
        for i in range(len(ts_code)):
            # moneyflowpercode = pro.moneyflow(ts_code=ts_code[i],trade_date=trade_date)
            moneyflowpercode = moneyflow(ts_code=ts_code[i], trade_date=trade_date,start_date='',end_date='')
            moneyflowpf = pd.concat([moneyflowpf,moneyflowpercode])
            i = i+1
        if moneyflowpf.shape[0] >= 4000:
            print('单股票单个日期返回结果超过4000（moneyflowlist）')
        else:
            return moneyflowpf
        # return moneyflowpf
    elif type(ts_code) == list and trade_date == '' and start_date !='' and end_date !='':
        # 一个股票池和多个日期
        moneyflowpf = pd.DataFrame()
        for i in range(len(ts_code)):
            moneyflowpercode = moneyflow(ts_code=ts_code[i], trade_date='', start_date=start_date, end_date=end_date)
            moneyflowpf = pd.concat([moneyflowpf, moneyflowpercode])
            i = i + 1
        if moneyflowpf.shape[0] >= 4000:
            print('单股票池多个日期返回结果超过4000（moneyflowlist）')
        else:
            return moneyflowpf
        # print('多个股票多个日期还没开发呢')
    elif type(ts_code) != list:
        print('朋友单个股票去调用moneyflow')



def stockcodelist(df,ts_code,name_code):
    # 将一个含有ts_code的dataframe改成返回ts_code的list或者含有ts_code和name的list
    if isinstance(df,pd.DataFrame):
        # print('兄弟给个dataframe过来呢。stockcodelist',type(pd))
    # 判断给的pd是不是dataframe，如果不是则报错。
        if ts_code !='' and name_code == '':
            stock_list = df[ts_code].tolist()
            return stock_list
    # 如果在只是给出了ts_code在整个dataframe里面的列名。则直接转换成只有ts_code的list。
        elif ts_code !='' and name_code !='':
            stock_array = [(ts_code, name) for ts_code, name in zip(df[ts_code], df[name_code])]
            stock_listwithname = list(stock_array)
            return stock_listwithname
    else:
        print('兄弟给个dataframe过来呢。stockcodelist')


if __name__ == "__main__":
    show=True
    show_func = print if show else lambda a: a
    # show_func(Getdailyfromconcept('TS355',20191009,20191010))
    # show_func(index_classify('L1'))
    # show_func(index_member('801780.SI',''))
    # show_func(index_member('','600928.SH'))
    # 如上是尝试通过某个已经知道的概念id来获取当时所有股票的涨幅情况
    # show_func(moneyflow('000001.SZ','20191016','',''))
    # show_func(moneyflowlist(['000001.SZ','601398.SH'],'20191016','',''))
    # concerp = show_func(Getconcept(''))
    stock_pf = Getconcept_detail('TS26','')
    # show_func(stock_pf)
    stock_list = stockcodelist(stock_pf,'ts_code','')
    # show_func(type(stock_list))
    # show_func(moneyflowlist(stock_list,'','20190601','20191018'))
    # Dataframdatashow(moneyflowlist(stock_list, '', '20190601', '20191018'))
    # moneyflowlist(stock_list, '', '20190601', '20191018').to_csv('DATa1.csv')
