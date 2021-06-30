# -*- coding: utf-8 -*-
"""
#功能：通通股票分析软件框架 获取字王股票数据包
#版本：Ver1.00
#设计人：独狼荷蒲
#电话:18578755056
#QQ：2775205
#百度：荷蒲指标
#开始设计日期: 2018-07-08
#公众号:独狼股票分析
#使用者请同意最后<版权声明>
#最后修改日期:2018年9月14日
#主程序：HP_main.py
"""
import pandas as pd  
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
import datetime as dt

#先修改正确的数据路径
daylinefilespath = 'D:\\zwDat\\cn\\Day'

def readzwdata(stockcode='', sday='1991-01-01', eday='2018-12-14'):
    filename = daylinefilespath  +'\\' + str(stockcode).zfill(6) + '.csv'
    try:
        rawdata = pd.read_csv(filename, parse_dates = True, index_col = 0, encoding = 'gbk')
        rawdata = rawdata[rawdata.index>=sday]
        rawdata = rawdata[rawdata.index <= eday]
    except IOError:
        rawdata=None
        raise Exception('IoError when reading dayline data file: ' + filename)
    return rawdata

def zwtots(df1):  #字王数据格式转ts格式
    a=[x.strftime("%Y-%m-%d") for x in df1.index]
    df1.insert(0,'date',a)
    df1=df1.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    return df1


def readstkData(rootpath, stockcode, sday, eday):

    returndata = pd.DataFrame()
    for yearnum in range(0,int((eday - sday).days / 365.25)+1):
        theyear = sday + dt.timedelta(days = yearnum * 365)
        # build file name
        #filename = rootpath  + theyear.strftime('%Y') + '\\' + str(stockcode).zfill(6) + '.csv'
        filename = rootpath  +'\\' + str(stockcode).zfill(6) + '.csv'
        
        try:
            rawdata = pd.read_csv(filename, parse_dates = True, index_col = 0, encoding = 'gbk')
        except IOError:
           raise Exception('IoError when reading dayline data file: ' + filename)

        returndata = pd.concat([rawdata, returndata])
    
    # Wash data
    returndata = returndata.sort_index()
    returndata.index.name = 'DateTime'
    returndata.drop('amount', axis=1, inplace = True)
    #print(returndata)
    #returndata.columns = ['Open', 'High', 'Close', 'Low', 'Volume']

    returndata = returndata[returndata.index < eday.strftime('%Y-%m-%d')]
    
    #returndata.rename(columns={'Close':'close'}, inplace=True)    
    #print(returndata)
    return returndata


def loadstkData(stock_b_code):
        daylinefilespath = 'D:\\zwDat\\cn\\Day\\'
        #stock_b_code = '000001' #平安银行

        startdate = dt.date(2016, 10, 1)
        enddate = dt.date(2017, 1, 30)
        plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
        plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

        days = readstkData(daylinefilespath, stock_b_code, startdate, enddate)
        
        #print(days)
    
        daysreshape = days.reset_index()
        
        
        daysreshape['date']=mdates.date2num(daysreshape['DateTime'].astype(dt.date))
        #print(daysreshape )
        
        daysreshape = daysreshape.reindex(columns=['date','open','high','low','close'])   
        return daysreshape,days 


################独狼荷蒲软件版权声明###################
'''
独狼荷蒲软件(或通通软件)版权声明
1、独狼荷蒲软件(或通通软件)均为软件作者设计,或开源软件改进而来，仅供学习和研究使用，不得用于任何商业用途。
2、用户必须明白，请用户在使用前必须详细阅读并遵守软件作者的“使用许可协议”。
3、作者不承担用户因使用这些软件对自己和他人造成任何形式的损失或伤害。
4、作者拥有核心算法的版权，未经明确许可，任何人不得非法复制；不得盗版。作者对其自行开发的或和他人共同开发的所有内容，
    包括设计、布局结构、服务等拥有全部知识产权。没有作者的明确许可，任何人不得作全部或部分复制或仿造。

独狼荷蒲软件
QQ: 2775205
Tel: 18578755056
公众号:独狼股票分析
'''