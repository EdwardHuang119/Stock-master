# -*- coding: utf-8 -*-
#pytdx小白量化框架数据接口
##pip install pytdx
#买<零基础搭建量化投资系统>,送小白量化软件源代码。
#独狼荷蒲qq:2775205
#通通python量化群:524949939
#电话微信:18578755056
import datetime as dt
import pandas as pd
from pytdx.exhq import TdxExHq_API, TDXParams
global tdxapiex

#市场

MARKET_SZ = 0  # 深圳
MARKET_SH = 1  # 上海

#K线种类
# K 线种类
# 0 -   5 分钟K 线
# 1 -   15 分钟K 线
# 2 -   30 分钟K 线
# 3 -   1 小时K 线
# 4 -   日K 线
# 5 -   周K 线
# 6 -   月K 线
# 7 -   1 分钟
# 8 -   1 分钟K 线
# 9 -   日K 线
# 10 -  季K 线
# 11 -  年K 线

KLINE_TYPE_5MIN = 0
KLINE_TYPE_15MIN = 1
KLINE_TYPE_30MIN = 2
KLINE_TYPE_1HOUR = 3
KLINE_TYPE_DAILY = 4
KLINE_TYPE_WEEKLY = 5
KLINE_TYPE_MONTHLY = 6
KLINE_TYPE_EXHQ_1MIN = 7
KLINE_TYPE_1MIN = 8
KLINE_TYPE_RI_K = 9
KLINE_TYPE_3MONTH = 10
KLINE_TYPE_YEARLY = 11


# ref : https://github.com/rainx/pytdx/issues/7
# 分笔行情最多2000条
MAX_TRANSACTION_COUNT = 2000
# k先数据最多800条
MAX_KLINE_COUNT = 800


# 板块相关参数
BLOCK_SZ = "block_zs.dat"
BLOCK_FG = "block_fg.dat"
BLOCK_GN = "block_gn.dat"
BLOCK_DEFAULT = "block.dat"

#连接扩展行情
def TdxexInit(ip='106.14.95.149',port=7727):
    global tdxapiex
    tdxapiex = TdxExHq_API(auto_retry=True, raise_exception=False)
    try:
        is_tdx_ex_connect = tdxapiex.connect(ip, port, time_out=30)
    except Exception as e:
        #print('time out to connect to pytdx')
        print(e)
    if is_tdx_ex_connect is not False:# 失败了返回False，成功了返回地址
        pass
        #print('connect to pytdx extend api successful')
    else:
        tdxapiex=None
    return tdxapiex

#断开扩展行情
def disconnect():
    global tdxapiex
    tdxapiex.disconnect()

#获取市场代码
def get_markets():
    global tdxapiex
    result= tdxapiex.get_markets()
    df=tdxapiex.to_df(result)
    return df


#查询市场中商品数量
def get_instrument_count():
    global tdxapiex
    return tdxapiex.get_instrument_count()
      
#    df4=GetSecurityList()

#获取股票代码表
def GetSecurityList():
    global tdxapiex
    nStart = 0
    nEnd=500
    m=tdxapiex.get_instrument_count()
    df=tdxapiex.to_df(tdxapiex.get_instrument_info(nStart, nEnd))
    df=pd.DataFrame(columns = ['code','name','pre_close']) 
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    nStart = 500
    nEnd=1000
    while nStart<m:
        result = tdxapiex.get_instrument_info(nStart, nEnd)
        df2=tdxapiex.to_df(result)
        df=df.append( df2,ignore_index=True)            
        nStart=nStart+500
        nEnd=nEnd+500
        
    return df


#查询五档行情
def get_instrument_quote(nMarket=47, sStockCode="IF1709"):
    result=tdxapiex.get_instrument_quote(nMarket,sStockCode)
    df5=tdxapiex.to_df(result)
    return df5


#查询当前分时行情
def get_minute_time_data(nMarket=47, sStockCode="IF1709"):
    result=tdxapiex.get_minute_time_data(nMarket,sStockCode)
    df6=tdxapiex.to_df(result)
    return df6

#查询历史分时行情
#参数 市场ID，证券代码，日期
def get_history_minute_time_data(nMarket=31,sStockCode= "00020", nData=20200110):
    result=tdxapiex.get_history_minute_time_data(nMarket,sStockCode, nData)
    df5=tdxapiex.to_df(result)
    return df5


#查询k线数据
#参数： K线周期， 市场ID， 证券代码，起始位置， 数量
#参数： 
#nCategory -> K 线种类 
#0 5 分钟K 线 
#1 15 分钟K 线 
#2 30 分钟K 线 
#3 1 小时K 线 
#4 日K 线 
#5 周K 线 
#6 月K 线 
#7 1 分钟 
#8 1 分钟K 线 
#9 日K 线 
#10 季K 线 
#11 年K 线 
#nMarket -> 市场代码0:深圳，1:上海 
#sStockCode -> 证券代码； 
#nStart -> 指定的范围开始位置； 
#nCount -> 用户要请求的K 线数目，最大值为800。

def get_instrument_bars(nCategory=9,nMarket = 31,code="00020",\
                    nStart=0, nCount=100):
    result=tdxapiex.get_instrument_bars(nCategory, nMarket,code, nStart, nCount)
    df5=tdxapiex.to_df(result)
    return df5

#查询分笔成交
def get_transaction_data(nMarket = 31,code="00020"):
    result=tdxapiex.get_transaction_data( nMarket,code)
    df5=tdxapiex.to_df(result)
    return df5



#查询历史分笔成交
#参数：市场ID，证券代码, 日期,偏移量
#市场ID可以通过 get_markets 获得
#日期格式 YYYYMMDD 如 20170810
#注意，这个接口最多返回1800条记录, 如果有超过1800条记录的请求，我们有一个start 参数作为便宜量，可以取出超过1800条记录
#    如期货的数据：这个接口可以取出1800条之前的记录，数量也是1800条    
def get_history_transaction_data(nMarket=47,sCode="IFL0",nDate=20200110,nStart=0):
    result=tdxapiex.get_history_transaction_data(nMarket,sCode,nDate,nStart)
    df5=tdxapiex.to_df(result)
    return df5    




#测试
if __name__ == '__main__':
    global tdxapiex
    tdxapiex=TdxexInit()
    mk=get_markets()
    print(mk)

#    #查询分笔成交
#    df=get_transaction_data()
#    print(df)
#    
    
    #获取市场代码
    df=tdxapiex.to_df(tdxapiex.get_markets())
    print(df.index)
    print(df.at[1,'market'])
#    print(df.iloc[1,'market'])
    #查询代码列表

    #查询市场中商品数量
    df4=GetSecurityList()
    df4.to_csv('./data/hqex.csv' , encoding= 'gbk')
    print(df4)

#    #查询五档行情
#    result=tdxapiex.get_instrument_quote(47, "IF1709")
#    df5=tdxapiex.to_df(result)
#    print(df5)
    
#    #查询分时行情
#    df6=tdxapiex.get_minute_time_data(47, "IF1709")
#    print(df6)   
#    
    #查询历史分时行情
    #参数 市场ID，证券代码，日期
#    df7=get_history_transaction_data()
#    print(df7)
    
    #查询k线数据
    #参数： K线周期， 市场ID， 证券代码，起始位置， 数量
    dd8=tdxapiex.get_instrument_bars(TDXParams.KLINE_TYPE_DAILY, 30, "AUL8", 0, 1800)  #黄金日线数据
    df8=tdxapiex.to_df(dd8)    
    print(df8)    
#    
#    #查询分笔成交
#    df9=tdxapiex.get_transaction_data(31, "00020")
#    print(df9)    
#    '''
#    注意，这个接口最多返回1800条记录, 如果有超过1800条记录的请求，我们有一个start 参数作为便宜量，可以取出超过1800条记录
#    如期货的数据：这个接口可以取出1800条之前的记录，数量也是1800条
#    '''
#    df9=tdxapiex.get_history_transaction_data(47, "IFL0", 20170810, start=1800)
#    print(df9)   
#    
#    #查询历史分笔成交
#    #参数：市场ID，证券代码, 日期
#    #市场ID可以通过 get_markets 获得
#    #日期格式 YYYYMMDD 如 20170810
#获取港股美团行情
    dd9=tdxapiex.get_history_transaction_data(31, "03690", 20200810)
    df9=tdxapiex.to_df(dd9)
    print(df9) 

#获取期货 黄金主连
#    dd9=tdxapiex.get_history_transaction_data(30, "AUL8", 20210122)
#    df9=tdxapiex.to_df(dd9)
#    print(df9)  

#    print(tdxapiex.to_df(tdxapiex.get_instrument_info(0, 1000) )  )