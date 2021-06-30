# -*- coding: utf-8 -*-
"""
#仿通达新大智慧公式基础库  Ver1.00
#版本：Ver1.00
#设计人：独狼荷蒲
#电话:18578755056
#QQ：2775205
#百度：荷蒲指标
#开始设计日期: 2018-07-08
#公众号:独狼股票分析
#使用者请同意最后<版权声明>
#最后修改日期:2020年01月22日
*********************************************
通达信公式转为python公式的过程
1.‘:=’为赋值语句，用程序替换‘:=’为python的赋值命令‘=。
2.‘:’为公式的赋值带输出画线命令，再替换‘:’为‘=’，‘:’前为输出变量，顺序写到return 返回参数中。
3.全部命令转为英文大写。
4.删除绘图格式命令。
5.删除掉每行未分号; 。
6.参数可写到函数参数表中.例如: def KDJ(N=9, M1=3, M2=3):

例如通达信 KDJ指标公式描述如下。
参数表 N:=9, M1:=3, M2:=3
RSV:=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100;
K:SMA(RSV,M1,1);
D:SMA(K,M2,1);
J:3*K-2*D;

def KDJ(N=9, M1=3, M2=3):
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = EMA(RSV, (M1 * 2 - 1))
    D = EMA(K, (M2 * 2 - 1))
    J = 3*K-2*D
    return K, D, J
###################基本函数库##############################
"""
import os
import math
import datetime as dt
import pandas as pd  
import numpy  as np
import time
import HP_tdx as htdx
from HP_formula import *

global tdxapi
global Cw,Base2
global Mydf
global Close,Low,High,Open,Vol,Amo
global Vol
global Period,Date,Time,Year,Month,Weekday,Day,Hour,Minute
global Code,Market,Setcode,Name,Py
global Mindiff,Tqflag,Useddatanum,Multiplier
global Totalcapital,Capital,Type2
Tqflag=0 
Type2=10


def readbase(nMarket =0,code='000776'):
    global Cw
    global Code,Market,Setcode,Name,Py
    global Mindiff,Tqflag,Useddatanum,Multiplier
    global Totalcapital,Capital,Type2
    if nMarket<0:
        nMarket=htdx.get_market(code)
    Code=code
    Market=nMarket
    Cw= htdx.tdxapi.get_finance_info(nMarket, code)
    Totalcapital=Cw['zongguben']
    Capital=int(Cw['liutongguben']/100)
    return Cw

def readbase2(nMarket = 0,codex='000776'):
    global Mindiff,Tqflag,Useddatanum,Multiplier
    global Base2,Name,Py
    base=None
    if nMarket==0:
        base=pd.read_csv('../../../Downloads/xb2e/data/sz.csv', encoding='gbk')
        base= base.drop('Unnamed: 0', axis=1)
        base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]
        if codex!='':
            base2=base[base['code']==codex]
        #print(base2)
    elif nMarket==1:
        base=pd.read_csv('../../../Downloads/xb2e/data/sh.csv', encoding='gbk')
        base= base.drop('Unnamed: 0', axis=1)
        base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]
        if codex!='':
            base2=base[base['code']==codex]
        #print(base2)
    if nMarket==0 or nMarket==1:
        columns=list(base2.columns)
        Base2={}
        try:
            [values]=base2.values
            #print(columns,values)
            Base2={}
            for i in range(len(columns)):
                Base2[columns[i]]=values[i]
            Mindiff=Base2['decimal_point']
            Multiplier=Base2['volunit']    
            Name=Base2['name']
            Py= Base2['py']
        except:            
            Base2={}
    return Base2


#(nCategory, nMarket, sStockCode, nStart, nCount) 
#获取市场内指定范围的证券K 线， 
#指定开始位置和指定K 线数量，指定数量最大值为800。 
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
def get_security_bars(nCategory=4,nMarket =-1,code='000776',\
                    nStart=0, nCount=240):
    global tdxapi
    global Cw,Base2
    global Mydf
    global Close,Low,High,Open,Vol,Amo
    global Vol
    global Period,Date,Time,Year,Month,Weekday,Day,Hour,Minute
    global Code,Market,Setcode,Name,Py
    global Mindiff,Tqflag,Useddatanum,Multiplier
    if nMarket<0:
        nMarket=htdx.get_market(code)
    Code=code
    Setcode=Market=nMarket 
    Period=nCategory
    Cw=readbase(Market,Code)
    Base2=readbase2(Market,Code)
    result =htdx.tdxapi.get_security_bars(nCategory, nMarket,code, nStart, nCount)
    Mydf=htdx.tdxapi.to_df(result)
    Useddatanum =len(Mydf)
    Mydf['date']=Mydf['datetime']
    Mydf['volume']=Mydf['vol']
    Close=Mydf['close']
    High=Mydf['high']
    Open=Mydf['open']
    Low=Mydf['low']
    Vol=Mydf['volume']
    Amo=Mydf['amount']
    Date=Mydf['date']
    Year=Mydf['year']
    Month=Mydf['month']
    Day=Mydf['day']
    Hour=Mydf['hour']
    Minute=Mydf['minute']
    Time=Hour*100+Minute
    return Mydf


def WEEKDAY():
    now = dt.datetime.now()
    return now.weekday()

#取得当前客户端机器为星期几(1,2,3,4,5,6,0)
def MACHINEWEEK():
    return dt.datetime.now().weekday()    

#取得当前客户端机器从1900以来的的年月日,
def MACHINEDATE():
    today=dt.date.today()   #获取今天日期
    date=today.year*10000+today.month*100+today.day-19000000
    return date

#取得当前客户端机器的时间,比如11:01:15时为110115
def MACHINETIME():
    today=dt.datetime.now()
    time=today.hour*10000+today.minute*100+today.second
    return time

def FINANCE(n):
    global Cw,Base2
    global Mydf
    global Close,Low,High,Open,Vol,Amo
    global Vol
    global Period,Date,Time,Year,Month,Weekday,Day,Hour,Minute
    global Code,Market,Setcode,Name,Py
    global Mindiff,Tqflag,Useddatanum,Multiplier
    global Totalcapital,Capital,Type2
    if n==1:
        return Cw['zongguben' ]
    elif n==2:
        return Setcode
    elif n==3:
        return Base2['type2']
    elif n==4:
        return 0
    elif n==5:
        if Base2['type2']==5:
            return 1
        else:
            return 0
    elif n==6:
        if Cw['bgu']>0:
            return 1
        else:
            return 0
    elif n==7:
        return Cw['liutongguben']
    elif n==8:
        return Cw['gudongrenshu' ]
    elif n==9:
        return (Cw['zongzichan']-Cw['jingzichan'])/Cw['zongzichan']
    elif n==10:
        return Cw['zongzichan']
    elif n==11:
        return Cw['liudongzichan']
    elif n==12:
        return Cw['gudingzichan']
    elif n==13:
        return Cw['wuxingzichan']
    elif n==14:
        return 0
    elif n==15:
        return Cw['liudongfuzhai']
    elif n==16:    
        return 0
    elif n==17:
        return Cw['zibengongjijin']
    elif n==18: #每股公积金
        return Cw['zibengongjijin']/Cw['zongguben']
    elif n==19:
        return Cw['jingzichan']/Cw['zongguben']
    elif n==20:
        return Cw['zhuyingshouru']
    elif n==21: #营业成本
        return Cw['zhuyingshouru']-Cw['zhuyinglirun']
    elif n==22:
        return Cw['zhuyingshouru']
    elif n==23: #营业利润
        return Cw['zhuyinglirun']
    elif n==24: #投资收益
        return Cw['touzishouyu']    
    elif n==25: #经营现金流量
        return Cw['jingyingxianjinliu']      
    elif n==26: #总现金流量
        return Cw['zongxianjinliu']         
    elif n==27: #存货
        return Cw['cunhuo' ]
    elif n==28: #营业利润
        return Cw['zhuyinglirun']
    elif n==29: #税后利润
        return Cw['shuihoulirun' ]    
    elif n==30: #净利润
        return Cw['jinglirun' ]      
    elif n==31: #未分配利润
        return Cw['weifenpeilirun' ]        
    elif n==32: #每股未分配利润
        return Cw['zhuyingshouru']/Cw['zongguben']
    elif n==33: # 每股收益(折算为全年收益),对于沪深品种有效
        return Cw['jinglirun' ]/Cw['zongguben']/10
    elif n==34: #每股净资产
        return Cw['jingzichan' ]/Cw['zongguben']/10

    return None


def CW():
    return Cw

def MYDF():
    return Mydf

def BASE2():
    return Base2

def CODE():
    return Code

def NAME():
    return Name

def PY():
    return Py

def MARKET():
    return Market

def SETCODE():
    return Market

def PERIOD():
    return Period

def TOTALCAPITAL():
    return Totalcapital

def  CAPITAL():
    return Capital

def TYPE2():
    return Type2

def CLOSE():
    return Close

def C():
    return Close

def LOW():
    return Low

def L():
    return Low

def HIGH():
    return High

def H():
    return High

def OPEN():
    return Open

def O():
    return Open

def VOL():
    return Vol

def V():
    return Vol

def VOLUME():
    return Vol

def AMO():
    return Amo

def AMOUNT():
    return Amo

def MINDIFF():
    return Mindiff

def TQFLAG():
    return Tqflag

def USEDDATANUM():
    return Useddatanum

def MULTIPLIER():
    return Multiplier

def DATE():
   return Date

def TIME():
    return Time

def YEAR():
    return Year

def MONTH():
    return Month

def DAY():
    return Day

def HOUR():
    return Hour

def MINUTE():
    return Minute

#自选股数据转通达信股票列表
def getzxg(z):
    z2=z.split(chr(10))
    l=[]
    for i in range(1,len(z2)):
        z3=z2[i]
        l.append((int(z3[0:1]),z3[1:9]))
    return l

def getzxgfile(file='ZXG.blk'):
    f = open(file,'r')
    z=f.read()
    f.close()
    return getzxg(z)

#通达信股票列表转自选股数据转
def putzxg(l):
    s=''
    for i in range(len(l)):
        l2,l3=l[i]
        s=s+chr(10)+str(l2)+l3
    return s

def putzxgfile(l,file='ZXG2.blk'):
    f = open(file,'w')
    s=putzxg(l)
    f.write(s)
    f.close()
    return s


#测试
if __name__ == '__main__':
    tdxapi=htdx.TdxInit(ip='180.153.18.171')
    df=get_security_bars()
    print(df)
#    df=get_security_bars()
#    print(df)
#    print(df.columns)
#    now = dt.datetime.now()
#    print( MACHINETIME())
#    x=readbase2()
    
#    x=WINNER(C)
    print(CW())
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