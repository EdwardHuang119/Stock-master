# -*- coding: utf-8 -*-
"""
#功能：通通股票分析软件框架 字王股票数据包
#版本：Ver1.00
#设计人：独狼荷蒲
#电话:18578755056
#QQ：2775205
#百度：荷蒲指标
#开始设计日期: 2018-07-08
#公众号:独狼股票分析
#使用者请同意最后<版权声明>
#最后修改日期:2018年12月16日
#主程序：HP_main.py
"""

from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import datetime as dt
from matplotlib import dates as mdates
import HP_VIEW.HP_global as g
from HP_VIEW.HP_set import *


##数据处理
#g.datapath = '\\xxdata'

#数字股票代码转换字符串股票代码
def stockname(n):
    '''
    函数说明
    数字股票代码转换字符串股票代码
    stockname(n)
    参数: n 整型
    返回：字符串
    '''
    s=str(n) #把数字转为字符串
    s=s.strip() #删除字符串前后空格
    if (len(s)<6 and len(s)>0):   #如果字符串长度在1-5之间，前面用0补够6位长度。
        s=s.zfill(6)+'.SZ'  #深圳股后缀加.SZ
    if len(s)==6:   #上海股票一般100000以上数字。
        if s[0:1]=='0':  #第一位为0，是深圳股票代码
            s=s+'.SZ'  #深圳股后缀加.SZ
        else:   #否则是上海股票代码
            s=s+'.SH'  #深圳股后缀加.SH
    return s

def stockname2(n):
    '''
    函数说明
    数字股票代码转换字符串股票代码
    stockname(n)
    参数: n 整型
    返回：字符串
    '''
    s=str(n) #把数字转为字符串
    s=s.strip() #删除字符串前后空格
    if (len(s)<6 and len(s)>0):   #如果字符串长度在1-5之间，前面用0补够6位长度。
        s=s.zfill(6)+'.SZ'  #深圳股后缀加.SZ
    if len(s)==6:   #上海股票一般100000以上数字。
        if s[0:1]=='0':  #第一位为0，是深圳股票代码
            s='SZ'+s  #深圳股后缀加.SZ
        else:   #否则是上海股票代码
            s='SH'+s  #深圳股后缀加.SH
    return s


def jqtots(df1):  #聚宽格式转ts格式
    a=[x.strftime("%Y-%m-%d") for x in df1.index]
    df1.insert(0,'date',a)
    df1=df1.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    return df1

def jqtots2(df1):  #聚宽格式转ts格式
    #a=[x.strftime("%Y-%m-%d") for x in df1.index]
    df1.insert(0,'date',df1.index)
    df1=df1.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    return df1


def tstojq(df1):  #ts格式转聚宽格式
    a=[dt.datetime.strptime(x,'%Y-%m-%d') for x in df1['date']]
    df1.insert(0,'date2',a)
    df1=df1.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    df1.index=df1['date2']
    del df1['date2']
    del df1['date']
    return df1

def put_stock_basics(base):
    base.to_csv(g.datapath+'\\stock_base.csv' , encoding= 'gbk')
    return base

def get_stock_basics():
    base=pd.read_csv(g.datapath+'\\stock_base.csv' , encoding= 'gbk')
    base= base.set_index(base.code)   
    base= base.drop('code', axis=1)
    return base

def get_today_all():
    base=pd.read_csv(g.datapath+'\\realtime.csv' , encoding= 'gbk')
    base.drop(base.columns[0:1], axis=1,inplace=True)    
    base=base.reset_index(level=None, drop=True ,col_level=0, col_fill='')
    a=[str(x).zfill(6) for x in base.code]
    base.code=a
    return base

def get_index():
    base=pd.read_csv(g.datapath+'\\index.csv' , encoding= 'gbk')
    base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]
    base= base.set_index(base.code)   
    base= base.drop('code', axis=1)
    return base

#业绩报告
def get_report_data(y,n):
    base=pd.read_csv(g.datapath+'\\report.csv' , encoding= 'gbk')
    base=base[base.year==y]
    base=base[base.no==n]
    base= base.drop('year', axis=1)
    base= base.drop('no',axis=1)
    base=base.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    base=base.drop(base.columns[0], axis=1)
    base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]
    return base

#盈利能力
def get_profit_data(y,n):
    base=pd.read_csv(g.datapath+'\\profit.csv' , encoding= 'gbk')
    base=base[base.year==y]
    base=base[base.no==n]
    base= base.drop('year', axis=1)
    base= base.drop('no',axis=1)
    base=base.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    base=base.drop(base.columns[0], axis=1)
    base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]
    return base

#营运能力
def get_operation_data(y,n):
    base=pd.read_csv(g.datapath+'\\operation.csv' , encoding= 'gbk')
    base=base[base.year==y]
    base=base[base.no==n]
    base= base.drop('year', axis=1)
    base= base.drop('no',axis=1)
    base=base.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    base=base.drop(base.columns[0], axis=1)
    base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]
    return base

#成长能力
def get_growth_data(y,n):
    base=pd.read_csv(g.datapath+'\\growth.csv' , encoding= 'gbk')
    base=base[base.year==y]
    base=base[base.no==n]
    base= base.drop('year', axis=1)
    base= base.drop('no',axis=1)
    base=base.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    base=base.drop(base.columns[0], axis=1)
    base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]
    return base


#偿债能力
def get_debtpaying_data(y,n):
    base=pd.read_csv(g.datapath+'\\debtpaying.csv' , encoding= 'gbk')
    base=base[base.year==y]
    base=base[base.no==n]
    base= base.drop('year', axis=1)
    base= base.drop('no',axis=1)
    base=base.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    base=base.drop(base.columns[0], axis=1)
    base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]
    return base

#现金流量
def get_cashflow_data(y,n):
    base=pd.read_csv(g.datapath+'\\cashflow.csv' , encoding= 'gbk')
    base=base[base.year==y]
    base=base[base.no==n]
    base= base.drop('year', axis=1)
    base= base.drop('no',axis=1)
    base=base.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    base=base.drop(base.columns[0], axis=1)
    base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]
    return base

def get_k_data(ss,ktype='D',start='1991-01-01',end='2018-10-15',index=False,autype='qfq'):
    pp=''
    if autype=='None':
        pp=pp+'none\\'
    if autype=='hfq':
        pp=pp+'hfq\\'
    if index==True:
        pp=pp+'index'
        
    kk=''    
    if ktype=='D':
        kk=kk+'\\day\\'
    if ktype=='W':
        kk=kk+'\\week\\'
    if ktype=='M':
        kk=kk+'\\month\\'    
    if ktype=='5':
        kk=kk+'\\minute\\5\\'
        pp=''
       
    ss1=kk+pp+ss+'.csv'
    base=pd.read_csv(g.datapath+ss1 , encoding= 'gbk')
    base.drop(base.columns[0:1], axis=1,inplace=True) 
    base=base[base.date>=start]
    base=base[base.date<=end]
    base=base.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]
    return base
        

#双色球
def get_ssq():
    base=pd.read_csv(g.datapath+'\\cp\ssq.csv' , encoding= 'gbk')
    return base

#大乐透
def get_dlt():
    base=pd.read_csv(g.datapath+'\\cp\dlt.csv' , encoding= 'gbk')
    return base

#####################################################
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