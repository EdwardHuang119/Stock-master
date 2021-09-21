#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
import time
import numpy as np
# from Test.QyptTableView import Dataframdatashow
import sys
import os
from configparser import ConfigParser


ts.set_token('22e74c8e4523bb24f26bcd5706617b2059c0e4e0f7f9df3559c5b000')
pro = ts.pro_api()
# show_fuck = print()

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


def GetAlltscode(is_hs,list_status,exchange,codeonly):
    # 获取一下全部有效的tscode
    # 先梳理一下字典想取值
    is_hs_list =['N','H','S','']
    list_status_list = ['L','D','P','']
    exchange_list = ['SSE','SZSE','']
    codeonly_list = ['1','']
    if is_hs not in is_hs_list:
        print('字典项错误，is_hs代表"是否沪深港通标的"，字典项为N否 H沪股通 S深股通,空为全部')
    elif list_status not in list_status_list:
        print('字典项错误，list_status上市状态： 字典项为L上市 D退市 P暂停上市，默认L')
    elif exchange not in exchange_list:
        print('字典项错误，is_hs代表"交易所"，字典项为交易所 SSE上交所 SZSE深交所 HKEX港交所(未上线)')
    elif codeonly not in codeonly_list:
        print('字典项错误，oodeonly表示是否仅返回tscode的list，字典为空则表示返回dataframe,1代表返回tscode的list。')
    else:
        # 开始执行交易获取
        if codeonly == '':
            # 如果要全部一个包含多个信息的dataframe就输入0
            if list_status == '':
                list_status = 'L'
            #     如果list——status是空赋值为L
            tscode = pro.query('stock_basic', is_hs=is_hs, exchange=exchange, list_status=list_status, fields='ts_code,symbol,name,area,industry,list_date,exchange,curr_type,is_hs')
        elif codeonly == '1':
            # 不赋值就返回所有的股票的基础信息，返回dataframe
            tscode = pro.query('stock_basic', is_hs=is_hs, exchange=exchange, list_status= list_status, fields='ts_code,symbol,name,area,industry,list_date,exchange,curr_type,is_hs')
            tscode = tscode['ts_code'].to_list()
        return tscode




def Getdailyfromtscode(ts_code,start_date,end_date):
    # 通过ts_code来获取到日线信息
    if type(ts_code) == str and str(ts_code) != '':
        Stock_daily = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    elif type(ts_code) == list:
        Stock_daily = pd.DataFrame()
        for i in range(len(ts_code)):
            Stock_daily_per = pro.daily(ts_code=ts_code[i], start_date=start_date, end_date=end_date)
            Stock_daily = pd.concat([Stock_daily,Stock_daily_per],ignore_index=True)
            i=i+1
    elif ts_code =='':
        if str(start_date) != str(end_date):
            trade_cal_list_1 = trade_cal_list(start_date,end_date,'')
            Stock_daily = pd.DataFrame()
            for i in range(len(trade_cal_list_1)):
                Stock_daily_per = pro.daily(start_date = trade_cal_list_1[i],end_date = trade_cal_list_1[i])
                Stock_daily = pd.concat([Stock_daily,Stock_daily_per],ignore_index=True)
                print(trade_cal_list_1[i],'全部国内市场交易数据已经获取')
                time.sleep(20)
                i =i+1
        else:
            Stock_daily = pro.daily(start_date=start_date, end_date=end_date)
            # 可以允许起始和截至日期一致的
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
    if level !='':
        index_list = pro.index_classify(level=level, src='SW',fields='index_code,industry_name,level,industry_code')
    elif level == '':
        index_list = pro.index_classify(src='SW', fields='index_code,industry_name,level,industry_code')
        # index_list = pro.index_classify(src='SW')
    #     如果不指定fields会返回不足量。
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
            moneyflowpf = pd.concat([moneyflowpf,moneyflowpercode],ignore_index=True)
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
            moneyflowpf = pd.concat([moneyflowpf, moneyflowpercode],ignore_index=True)
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

def stk_rewards(ts_code):
    # 获取高管的薪酬
    stk_rewards = pro.stk_rewards(ts_code)
    return stk_rewards

def stock_company(exchange):
# 来获取上市公司的基本情况
# 通过输入市场来曲确认内容，交易所代码 ，SSE上交所 SZSE深交所
    if str(exchange) != "SSE" and str(exchange) != "SZSE":
        print('交易所代码 ，SSE上交所 SZSE深交所，请输入字典项')
    else:
        stock_company = pro.stock_company(exchange=exchange)
        return stock_company


def moneyflow_hsgt(trade_date,start_date,end_date):
# 获取沪股通、深股通、港股通每日资金流向数据，每次最多返回300条记录，总量不限制
    if trade_date !='':
        moneyflow_hsgt=pro.query('moneyflow_hsgt', trade_date=trade_date)
    elif trade_date =='' and start_date!='' and end_date !='':
        moneyflow_hsgt=pro.moneyflow_hsgt(start_date=start_date, end_date=end_date)
    elif trade_date =='' and start_date =='' or end_date =='':
        print('当trade_date为空时，start_date和end_date不可以同时为空。')
    return moneyflow_hsgt

def hk_hold(trade_date,start_date,end_date):
# 沪深港股通持股明细
    if trade_date !='':
        hk_hold=pro.hk_hold(trade_date=trade_date)
    elif trade_date =='' and start_date!='' and end_date!='':
        hk_hold=pro.hk_hold(start_date=start_date,end_date=end_date)
    elif trade_date =='' and start_date =='' or end_date =='':
        print('当trade_date为空时，start_date和end_date不可以同时为空。')
    return hk_hold

def trade_cal(start_date,end_date,exchange):
    if str(exchange)=='':
        trade_cal=pro.trade_cal(exchange='SSE', start_date=start_date, end_date=end_date)
    else:
        trade_cal = pro.trade_cal(exchange=exchange, start_date=start_date, end_date=end_date)
    return trade_cal

def trade_cal_list(start_date,end_date,exchange):
    A =trade_cal(start_date,end_date,exchange)
    trade_cal_list =A.loc[A['is_open'] ==1]['cal_date'].tolist()
    return trade_cal_list

def hk_tradecal(start_date,end_date):
    A=pro.hk_tradecal(start_date=start_date, end_date=end_date)
    # A=hk_tradecal(start_date,end_date)
    hk_tradecal_list = A.loc[A['is_open']==1]['cal_date'].tolist()
    hk_tradecal_list.sort()
    return hk_tradecal_list

def hk_basic():
    hk_basic = pro.hk_basic()
    return hk_basic

def hk_daily(ts_code,start_date,end_date):
    if type(ts_code)==str and str(ts_code) !='':
        hk_daily=pro.hk_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    elif type(ts_code) == list:
        hk_daily = pd.DataFrame()
        for i in range(len(ts_code)):
            hk_daily_per = pro.hk_daily(ts_code=ts_code[i], start_date=start_date, end_date=end_date)
            hk_daily = pd.concat([hk_daily, hk_daily_per],ignore_index=True)
            i = i + 1
    elif ts_code == '':
        if str(start_date) != str(end_date):
            trade_cal_list_1 = trade_cal_list(start_date,end_date,'XHKG')
            hk_daily = pd.DataFrame()
            for i in range(len(trade_cal_list_1)):
                hk_daily_per = pro.hk_daily(trade_date = trade_cal_list_1[i])
                hk_daily = pd.concat([hk_daily,hk_daily_per],ignore_index=True)
                print(trade_cal_list_1[i],'全部香港市场交易数据已经获取')
                time.sleep(2)
                i =i+1
        else:
            hk_daily =pro.hk_daily(trade_date = start_date)
    return hk_daily

def Tocsv(dataframe,filepathinput,name):
    configname = 'config.conf'
    fatherpath = os.path.abspath(os.path.dirname(os.getcwd()))
    configpath = fatherpath + '/confing' + '//' + configname
    cf = ConfigParser()
    cf.read(configpath)
    if sys.platform == 'win32':
        pathprefix = 'win'
    elif sys.platform == 'darwin':
        pathprefix = 'mac'
    if filepathinput =='':
        pathosread = 'filepath'
    else:
        pathosread = 'filepath'+'_'+filepathinput
    filesearch = pathprefix+pathosread
    filepath = cf.get('fileswrite',filesearch)
    fullname = filepath+name+'.csv'
    dataframe.to_csv(fullname, na_rep='0', encoding='utf_8_sig')
    print('TOCSV结束',fullname,'已经存储')
    return

def Read_csv(name,filepathinput):
    configname = 'config.conf'
    fatherpath = os.path.abspath(os.path.dirname(os.getcwd()))
    configpath = fatherpath + '/confing' + '//' + configname
    cf = ConfigParser()
    cf.read(configpath)
    if sys.platform == 'win32':
        pathprefix = 'win'
    elif sys.platform == 'darwin':
        pathprefix = 'mac'
    if filepathinput =='':
        pathosread = 'filepath'
    else:
        pathosread = 'filepath'+'_'+filepathinput
    filesearch = pathprefix + pathosread
    filepath = cf.get('fileswrite', filesearch)
    fullname = filepath + name + '.csv'
    dataframe = pd.read_csv(fullname,index_col=0)
    return dataframe

def index_daily(ts_code,start_date,end_date):
    index_daily = pro.index_daily(ts_code,start_date,end_date)
    return index_daily

def index_basic():
    index_basic_list = ['MSCI','CSI','SSE','SZSE','CICC','SW','OTH']
    index_basic = pd.DataFrame()
    for i in range(len(index_basic_list)):
        index_basic_per = pro.index_basic(market=index_basic_list[i])
        index_basic = pd.concat([index_basic,index_basic_per],ignore_index=True)
        i = i+1
    return index_basic

def index_weight(index_code,trade_date,start_date,end_date):
    index_weight = pd.DataFrame()
    if type(index_code) == str:
        if str(trade_date) !='':
            index_weight = pro.index_weight(index_code=index_code,trade_date=trade_date)
        else:
            index_weight = pro.index_weight(index_code=index_code,start_date=start_date,end_date=end_date)
    elif type(index_code) == list:
        if str(trade_date) != '':
            for i in range(len(index_code)):
                index_weight_per = pro.index_weight(index_code=index_code[i],trade_date=trade_date)
                index_weight = pd.concat([index_weight, index_weight_per], ignore_index=True)
                i = i + 1
        else:
            for i in range(len(index_code)):
                index_weight_per = pro.index_weight(index_code=index_code[i],tstart_date=start_date,end_date=end_date)
                index_weight = pd.concat([index_weight, index_weight_per], ignore_index=True)
                i = i + 1
    return index_weight

def daily_pro(ts_code,start_date,end_date,adj,freq,ma,factors,adjfactor):
    daily_pro = ts.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date,adj=adj,freq=freq,ma=ma,factors=factors,adjfactor=adjfactor)
    return daily_pro

def index_sw_daily(ts_code,start_date,end_date):
    # index_sw_daily = pro.sw_daily(trade_date = 20200630)
    index_sw_daily = pro.sw_daily(ts_code =ts_code,start_date = start_date,end_date = end_date)
    return index_sw_daily

def index_sw_daily_trade(trade_date):
    index_sw_daily = pro.sw_daily(trade_date = trade_date)
    return index_sw_daily

def fund_basic(market):
    if market =='':
        fund_basic = pro.fund_basic()
    else:
        fund_basic = pro.fund_basic(market=market)
    return fund_basic

def fund_nav(ts_code,end_date,market):
    fund_nav = pro.fund_nav(ts_code=ts_code,end_date=end_date,market=market)
    return fund_nav

def fund_portfolio(ts_code):
    fund_portfolio = pd.DataFrame()
    if type(ts_code) ==list:
        for i in range(len(ts_code)):
            fund_portfolio_per = pro.fund_portfolio(ts_code=ts_code[i])
            fund_portfolio = pd.concat([fund_portfolio, fund_portfolio_per], ignore_index=True)
            i = i + 1
    elif type(ts_code)==str and str(ts_code) !='':
        fund_portfolio = pro.fund_portfolio(ts_code=ts_code)
    return fund_portfolio






if __name__ == "__main__":
    show=True
    show_func = print if show else lambda a: a
    ind = pro.index_weight(index_code='399300.SZ',start_date = '20210501',end_date = '20210915' )
    show_func(ind)
    # df = pro.index_daily(ts_code='801011.SI', start_date='20200501', end_date='20200826')
    # df = index_sw_daily()
    # df = pro.index_classify(src='SW',fields='index_code,industry_name,level,industry_code')
    # df = index_classify('')
    # df2 = index_sw_daily(ts_code='801710.SI',start_date=20200101,end_date=20200831)
    # df2['trade_date'] = pd.to_datetime(df2['trade_date'], format='%Y%m%d')
    # show_func(df)


    # Tocsv(df,'','index_sw_daily')
    # show_func(index_daily('857333.SI','2020-01-01','2020-08-26'))
    # Tocsv(index_basic(),'','index_basic')
    # show_func(index_basic())

    # PRO日线获取
    # daily_pro_2 = daily_pro('000876.SZ','20190101','20200620','None','D',[5,10,20,60],[],'True')
    # daily_pro_1 = ts.pro_bar(ts_code='601398.SH',start_date='20200101',end_date='20200620',adj='None',freq='D',ma=[5,10],factors=[],adjfactor=False)
    # Tocsv(daily_pro_2,'','0625_2')
    # show_func(daily_pro_2)
    # show_func(daily_pro_1)

    # Chinadaily = Getdailyfromtscode('', start_date, end_date)
    # df = pro.index_daily(ts_code='801710.SI', trade_date = '20200413',start_date='20200413', end_date='20200414')
    # show_func(df)
    # show_func(Getdailyfromconcept('TS355',20191009,20191010))
    # show_func(index_classify('L1'))
    # show_func(index_member('801780.SI',''))
    # show_func(index_member('','600928.SH'))
    # 如上是尝试通过某个已经知道的概念id来获取当时所有股票的涨幅情况
    # show_func(moneyflow('000001.SZ','20191016','',''))
    # show_func(moneyflowlist(['000001.SZ','601398.SH'],'20191016','',''))
    # concerp = show_func(Getconcept(''))
    # stock_pf = Getconcept_detail('TS26','')
    # show_func(stock_pf)
    # stock_list = stockcodelist(stock_pf,'ts_code','')
    # show_func(type(stock_list))
    # show_func(moneyflowlist(stock_list,'','20190601','20191018'))
    # Dataframdatashow(moneyflowlist(stock_list, '', '20190601', '20191018'))
    # moneyflowlist(stock_list, '', '20190601', '20191018').to_csv('DATa1.csv')
    # code = GetTscodefromCname('渝农商行')
    # show_func(code)
    # data = stk_rewards('601077.SH')
    # cc = data[data['name'].str.contains(r'蔡')]
    # 最好的获取某个人薪酬的模糊查询方案
    # data = stk_rewards('601077.SH')
    # show_func(cc)
    # Dataframdatashow(data)
    # 上市公司基本请情况
    # stock_company = stock_company("SSE")
    # show_func(stock_company)
    # Dataframdatashow(stock_company)
    # 各股通的流入信息调用情况
    # 用trade来调用
    # moneyflow_hsgt = moneyflow_hsgt('20200122','','')
    # 用startdate和enddate来调用
    # moneyflow_hsgt = moneyflow_hsgt('', '20191221', '20200123')
    # show_func(moneyflow_hsgt)
# #     港股通持股明细
#     hk_hold_detail=hk_hold('','20200102','20200103')
#     show_func(hk_hold_detail)
#     获取一段时间的整体工作日历时间，为很多逐个日子拼接dataframe做准备
#     show_func(trade_cal_list('20191201','20200215'))

