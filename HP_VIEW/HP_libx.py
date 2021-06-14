"""
独狼股票函数库  Ver1.00
日期: 2018-07-08
QQ: 2775205
Tel: 18578755056
最后修改日期:2018-07-19

###################基本函数库##############################
使用说明
df 指标序列
tp 指标字段,例如close
n  周期数
al 字段别名,可以省略
----------------------------------------------------
import hplibx as mylib
平均移动线函数
def MA(df,tp, n) 		#移动平均,Moving Average  
使用 df=(df,'close',5)

def EMA(df,tp, n)  	#指数移动平均.Exponential Moving Average      

上穿函数
def CROSS(df,tp1,tp2)

#取前n周期数值函数    
def REF(df,tp,n)    

#取后n周期数值函数
def REFX(df,tp, n)

#Standard Deviation#标准偏差  
def STDDEV(df,tp,n):  

#取前n周期数值的最高价
def HHV(df,tp, n,al=''):     

#取前n周期数值的最低价
def LLV(df,tp, n,al=''):  

#取前n周期数值大于0的次数
def COUNT(df,tp, n,al=''):  

#求前n周期数值和
def SUM(df,tp, n,al=''):  
    
 #Winner当前价格获利率
def WINNER(df,price, tp1,al=''):  
    
#求动态移动平均。
#DMA(X,A),求X的A日动态移动平均。
def DMA(df,tp1,tp2,al=''):     

#大于等于函数
def EGT(df,tp1,tp2,al=''): 
    
#小于等于函数
def ELT(df,tp1,tp2,al=''):  

#等于函数
def EQUAL(df,tp1,tp2,al=''): 

#大于函数
def GT(df,tp1,tp2,al=''):  

#小于函数
def LT(df,tp1,tp2,al=''):  

#并且函数
def AND(df,tp1,tp2,al=''): 

#或者函数
def OR(df,tp1,tp2,al=''):     
###################指标库########################    
def ACCDIST(df, n):  			#积累/分配,Accumulation/Distribution  
def ADX(df, n, n_ADX):  	#定向运动平均指数,Average Directional Movement Index  
def ATR(df, n):  					#平均真实范围.Average True Range
def BBANDS(df, n):				#布林带.Bollinger Bands  
def CCI(df, n):  					#商品通道指数,Commodity Channel Index  
def COPP(df, n):  				#COPPOCK曲线,Coppock Curve 
def Chaikin(df):					#蔡金振荡器,Chaikin Oscillator  
def DONCH(df, n):  				#奇安通道,Donchian Channel  
def EOM(df, n):  					#缓解运动,Ease of Movement
def FORCE(df, n):					#力指数,Force Index 
def KELCH(df, n):  				#Keltner通道,Keltner Channel
def KST(df, r1, r2, r3, r4, n1, n2, n3, n4):  # KST振荡器,KST Oscillator 
def MACD(df, n_fast, n_slow): 
	#MACD指标信号和MACD的区别, MACD Signal and MACD difference   

def MFI(df, n):						#资金流量指标和比率,Money Flow Index and Ratio
def MOM(df, n):  					#动量.Momentum  
def MassI(df):						#质量指数,Mass Index    
def OBV(df, n):  					#平衡量,On-balance volume
def PPSR(df):  						#支点，支撑和阻力.Pivot Points, Supports and Resistances  
def ROC(df, n):  					#变化率.Rate of Change 
def RSI(df, n):  					#相对强弱指标,Relative Strength Index
def STDDEV(df, n):  			#标准偏差,#Standard Deviation
def STO(df, n):  					#随机指标D,Stochastic oscillator %D  
def STOK(df):  						#随机指标K,Stochastic oscillator %K  
def TRIX(df, n):  				#矩阵,#Trix  
def TSI(df, r, s):  			#真实强度指数,True Strength Index
def ULTOSC(df):  					#最终振荡器,Ultimate Oscillator 
def Vortex(df, n): 				#涡指标,#Vortex Indicator     
    
"""
import platform
import pandas as pd  
import numpy  
import math as m
from HP_VIEW.HP_global import *


#版本号
def VER():
    return 1.00

#版本号
def Ver():
    return 1.00

#聚宽股票代码转换
def jqsn(s):
    if (len(s)<6 and len(s)>0):
        s=s.zfill(6)+'.XSHE'
    if len(s)==6:
        if s[0:1]=='0':
            s=s+'.XSHE'
        else:
            s=s+'.XSHG'
    return s

##############内部函数库########################
def ema(c_list,n=12):
    y_list=[]
    _n = 1    
    for c in c_list: 
        if c == c_list[0]:
            y = c
        elif _n<n:
            y= c*2/(_n+1) + (1- 2/(_n+1))*y_list[-1] 
        else:
            y=c*2/(n+1)+(1-2/(n+1))*y_list[-1]
        y_list.append(y)
        _n = _n+1        
    return y_list

##############基本函数库#########################
def G_MA(Series,n):
    G_pyver=int(platform.python_version()[0:1])
    G_ma=None
    if G_pyver==2:
        G_MAstr='pd.rolling_mean(Series,n)'
        G_ma=eval(G_MAstr)
    else :
        G_MAstr='Series.rolling(window=n,center=False).mean()'
        G_ma=eval(G_MAstr)
    return G_ma


#复制函数
def COPY(df,tp1,al=''):  
    if (al.strip()==''):
        na=tp1+'_2'
    else:
        na=al 
    i = 0 
    ZB_l = []
    y=0
    while i < len(df):  
        y=df.get_value(i, tp1)
        ZB_l.append(y)  
        i = i + 1          
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df
    
#替换函数
def REPLACE(df,tp1,x):  
    df[tp1]=x
    return df

#ONLYONE函数
def ONLYONE(df,tp1):  
    i=0
    while i < len(df):  
        if  df[tp1][i]>0 :
            df[tp1]=0
            df[tp1][i]=1
            break
        i=i+1

    return df    

#大于等于函数
def EGTN(df,tp1,x,al=''):  
    if (al.strip()==''):
        na=tp1+'_EGTN_' + str(x)
    else:
        na=al 
    i = 0  
    ZB_l = []
    y=0
    while i < len(df):  
        if (df.get_value(i, tp1) >= x) :
                y=1
        else:
                y=0
        ZB_l.append(y)  
        i = i + 1          
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df

#小于等于函数
def ELTN(df,tp1,x,al=''):  
    if (al.strip()==''):
        na=tp1+'_ELTN' + str(x)
    else:
        na=al 
    i = 0  
    ZB_l = []
    y=0
    while i < len(df):  
        if (df.get_value(i, tp1) <= x) :
                y=1
        else:
                y=0
        ZB_l.append(y)  
        i = i + 1          
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df    


#大于等于函数
def EGT(df,tp1,tp2,al=''):  
    if (al.strip()==''):
        na=tp1+'_EGT_' + tp2
    else:
        na=al 
    i = 0  
    ZB_l = []
    y=0
    while i < len(df):  
        if (df.get_value(i, tp1) >= df.get_value(i, tp2)):
                y=1
        else:
                y=0
        ZB_l.append(y)  
        i = i + 1          
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df

#小于等于函数
def ELT(df,tp1,tp2,al=''):  
    if (al.strip()==''):
        na=tp1+'_ELT_' + tp2
    else:
        na=al 
    i = 0  
    ZB_l = []
    y=0
    while i < len(df):  
        if (df.get_value(i, tp1) <= df.get_value(i, tp2)):
                y=1
        else:
                y=0
        ZB_l.append(y)  
        i = i + 1          
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df    

#等于函数
def EQUAL(df,tp1,tp2,al=''):  
    if (al.strip()==''):
        na=tp1+'_EQUAL_' + tp2
    else:
        na=al 
    i = 0  
    ZB_l = []
    y=0
    while i < len(df):  
        if (df.get_value(i, tp1)  == df.get_value(i, tp2)):
                y=1
        else:
                y=0
        ZB_l.append(y)  
        i = i + 1          
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df

#大于函数
def GT(df,tp1,tp2,al=''):  
    if (al.strip()==''):
        na=tp1+'_GT_' + tp2
    else:
        na=al 
    i = 0  
    ZB_l = []
    y=0
    while i < len(df):  
        if (df.get_value(i, tp1) > df.get_value(i, tp2)):
                y=1
        else:
                y=0
        ZB_l.append(y)  
        i = i + 1          
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df

#小于函数
def LT(df,tp1,tp2,al=''):  
    if (al.strip()==''):
        na=tp1+'_LT_' + tp2
    else:
        na=al 
    i = 0  
    ZB_l = []
    y=0
    while i < len(df):  
        if (df.get_value(i, tp1) < df.get_value(i, tp2)):
                y=1
        else:
                y=0
        ZB_l.append(y)  
        i = i + 1          
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df


#并且函数
def AND(df,tp1,tp2,al=''):  
    if (al.strip()==''):
        na=tp1+'_AND_' + tp2
    else:
        na=al 
    i = 0 
    ZB_l = []
    y=0
    while i < len(df):  
        if (df.get_value(i, tp1) >0 and df.get_value(i, tp2)>0):
                y=1
        else:
                y=0
        ZB_l.append(y)  
        i = i + 1          
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df
    
#或者函数
def OR(df,tp1,tp2,al=''):  
    if (al.strip()==''):
        na=tp1+'_AND_' + tp2
    else:
        na=al 
    i = 0 
    ZB_l = []
    y=0
    while i < len(df)-1:  
        if (df.get_value(i, tp1) >0 or df.get_value(i, tp2)>0):
                y=1
        else:
                y=0
        ZB_l.append(y)  
        i = i + 1          
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df


#WW:= IF(L>CC, 0, IF(H<CC, 1, (CC-L+0.01)/(H-L+0.01))); { 每日获利盘 }
#Winner2:DMA(ww, VOL/CAPITAL)*100; { 获利盘 };
#Winner当前价格获利率
def WINNER(df,price, tp1,al=''):  
    if price==0.0:
        price=df.get_value(len(df)-1, 'close')
    if (al.strip()==''):
        na='WINNER_' + tp1
    else:
        na=al 
    i = 0  
    ZB_l = []
    y=0
    while i < len(df):  
        if (df.get_value(i, 'low') <price):
            y=0.0
        elif (df.get_value(i, 'high') >price):
            y=1.00
        else:
            y=(price-df.get_value(i, 'low')+0.01)/(df.get_value(i, 'high')-df.get_value(i, 'low')+0.01)
        yy=y
        ZB_l.append(yy)  
        i = i + 1          
        
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df


#Moving Average 平均线 
def MA(df,tp, n,al=''):  
    if (tp.strip()==''):
        tp1='close'
    else:
        tp1=tp
    if (al.strip()==''):
        na=tp1+'_MA_' + str(n)
    else:
        na=al
    #MA = pd.Series(pd.rolling_mean(df[tp1],window=n,center=False), name =na)   
    MA = pd.Series(df[tp1].rolling(window=n,center=False).mean(), name =na )
    df = df.join(MA)  
    return df

#Exponential Moving Average  
def EMA(df,tp, n,al=''):  
    if (tp.strip()==''):
        tp1='close'
    else:
        tp1=tp
    if (al.strip()==''):
        na=tp1+'_EMA_' + str(n)
    else:
        na=al
    #EMA = pd.Series(pd.ewma(df[tp1], span = n, min_periods = n - 1), name = na)  
    EMA = pd.Series(df[tp1].ewm(span = n, min_periods = n - 1,adjust=True,ignore_na=False).mean(), name = na)  
    df = df.join(EMA)  
    return df


#求动态移动平均。
#DMA(X,A),求X的A日动态移动平均。
#算法: 若Y=DMA(X,A)
#则 Y=A*X+(1-A)*Y',其中Y'表示上一周期Y值,A必须小于1。
#例如：DMA(CLOSE,VOL/CAPITAL)表示求以换手率作平滑因子的平均价
def DMA(df,tp1,tp2,al=''):  
    if (al.strip()==''):
        na='DMA_'+tp1+'_' + tp2
    else:
        na=al 
    i = 1 
    ZB_l = [0]
    y=df.get_value(i-1, tp1)*df.get_value(i-1, tp2)
    i=i+1
    while i < df.index[-1]:  
        y=df.get_value(i-1, tp1)*df.get_value(i-1, tp2)+(1-df.get_value(i-1, tp2))*y
        ZB_l.append(y)  
        i = i + 1          
        
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df

#上穿函数
def CROSS(df,tp1,tp2,al=''):  
    if (al.strip()==''):
        na=tp1+'_CROSS_' + tp2
    else:
        na=al 
    i = 1  
    CR_l = [0]
    y=0
    while i < len(df):  
        if ((df.get_value(i-1, tp1) <df.get_value(i-1, tp2)) and (df.get_value(i, tp1) >=df.get_value(i, tp2))):
                y=1
        else:
                y=0
        CR_l.append(y)  
        i = i + 1          
        
    CR_s = pd.Series(CR_l)  
    CR = pd.Series(CR_s, name = na)  
    df = df.join(CR)   
    return df

#取前n周期数值函数
def REF(df,tp, n,al=''):  
    if (tp.strip()==''):
        tp1='close'
    else:
        tp1=tp
    if (al.strip()==''):
        na=tp1+'_REF_' + str(n)
    else:
        na=al
    i = 0 
    ZB_l = []
    y = 0
    while i < n: 
        y=df.get_value(i, tp1)   
        ZB_l.append(y) 
        i=i+1
    while i < len(df):  
        y=df.get_value(i-n, tp1)        
        ZB_l.append(y)  
        i = i + 1          
        
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df

#取后n周期数值函数
def REFX(df,tp, n,al=''):  
    if (tp.strip()==''):
        tp1='close'
    else:
        tp1=tp
    if (al.strip()==''):
        na=tp1+'_REFX_' + str(n)
    else:
        na=al
    i = 0 
    ZB_l = []
    y=0
    while i < len(df)-n: 
         y=df.get_value(i+n, tp1)   
         ZB_l.append(y) 
         i=i+1
    while i < len(df):  
        y=df.get_value(i, tp1)        
        ZB_l.append(y)  
        i = i + 1          
        
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df


#Standard Deviation#标准偏差  
def STDDEV(df,tp,n):  
    df = df.join(pd.Series(pd.rolling_std(df[tp], n), name = tp+'_STD_' + str(n)))  
    return df  

#取前n周期数值的最高价
def HHV(df,tp, n,al=''):  
    if (tp.strip()==''):
        tp1='close'
    else:
        tp1=tp
    if (al.strip()==''):
        na=tp1+'_HHV_' + str(n)
    else:
        na=al
    i = 0 
    ZB_l = []
    y=df.get_value(i, tp1)  
    while i < n: 
         if y<df.get_value(i, tp1):  
             y=df.get_value(i, tp1)  
         ZB_l.append(y) 
         i=i+1
    while i < len(df):  
        j=1
        y=df.get_value(i, tp1)  
        while j < n: 
            if y<df.get_value(i-j, tp1)  :
                y=df.get_value(i-j, tp1)
            j=j+1
        ZB_l.append(y)  
        i = i + 1          
        
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df

#取前n周期数值的最低价
def LLV(df,tp, n,al=''):  
    if (tp.strip()==''):
        tp1='close'
    else:
        tp1=tp
    if (al.strip()==''):
        na=tp1+'_HHV_' + str(n)
    else:
        na=al
    i = 0 
    ZB_l = []
    y=df.get_value(0, tp1)  
    while i < n: 
         if y>df.get_value(i, tp1):  
             y=df.get_value(i, tp1)  
         ZB_l.append(y) 
         i=i+1
    while i < len(df):  
        j=1
        y=df.get_value(i, tp1)  
        while j < n: 
            if y>df.get_value(i-j, tp1)  :
                y=df.get_value(i-j, tp1)
            j=j+1
        ZB_l.append(y)  
        i = i + 1          
        
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df


#取前n周期数值大于0的次数
def COUNT(df,tp, n,al=''):  
    if (tp.strip()==''):
        tp1='close'
    else:
        tp1=tp
    if (al.strip()==''):
        na=tp1+'_COUNT_' + str(n)
    else:
        na=al
    i = 0 
    ZB_l = []
    y=0  
    while i < n: 
         if df.get_value(i, tp1)>0:  
             y=y+1  
         ZB_l.append(y) 
         i=i+1
    while i < len(df)+1:  
        j=1
        y=0  
        while j < n: 
            if df.get_value(i-j, tp1)>0  :
                y=y=y+1
            j=j+1
        ZB_l.append(y)  
        i = i + 1          
        
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df

#求前n周期数值和
def SUM(df,tp, n,al=''):  
    if (tp.strip()==''):
        tp1='close'
    else:
        tp1=tp
    if (al.strip()==''):
        na=tp1+'_SUM_' + str(n)
    else:
        na=al
    i = 0 
    ZB_l = []
    y=0  
    while i < n: 
         y=y+ df.get_value(i, tp1)  
         ZB_l.append(y) 
         i=i+1
    while i < len(df):  
        j=1
        y=0  
        while j < n: 
            y=y+ df.get_value(i-j, tp1)  
            j=j+1
        ZB_l.append(y)  
        i = i + 1          
        
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df   

#SMA(X,N,M)，求X的N日移动平均，M为权重。算法:若Y=SMA(X,N,M) 则 Y=(M*X+(N-M)*Y')/N，其中Y'表示上一周期Y值，N必须大于M。
def SMA(df,tp,n,m,al=''):
    if (tp.strip()==''):
        tp1='close'
    else:
        tp1=tp
    if (al.strip()==''):
        na=tp1+'_SMA_' + str(n)
    else:
        na=al
    i = 0 
    ZB_l = []
    y=1
    while i < len(df):
        y=(df.get_value(i, tp1)*m+(n-m)*y)/n
        ZB_l.append(y) 
        i=i+1
   
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)   
    return df       
    
################指标库#########################
#RSV:=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100;
#K:SMA(RSV,M1,1);
#D:SMA(K,M2,1);
#J:3*K-2*D;

def KDJ(df,n,m1,m2):  
    i = 0 
    RSV=0.0000
    ZB_l = []
    yl= df.get_value(0, 'low')  
    yh= df.get_value(0, 'high')  
    while i < n: 
        if yl>df.get_value(i, 'low')  :
            yl=df.get_value(i, 'low')
        if yh<df.get_value(i, 'high')  :
            yh=df.get_value(i, 'high')
        i=i+1
        RSV= (df.get_value(i, 'close')-yl)/(yh-yl)*100.0000
        ZB_l.append(RSV) 
    while i < len(df):  
        j=0
        yl= df.get_value(i, 'low')  
        yh= df.get_value(i, 'high')   
        while j < n: 
            if yl>df.get_value(i-j, 'low')  :
                yl=df.get_value(i-j, 'low')
            if yh<df.get_value(i-j, 'high')  :
                yh=df.get_value(i-j, 'high')
            j=j+1
        if yh !=yl :
            RSV= (df.get_value(i, 'close')-yl)/(yh-yl)*100.0000  
        else:
            RSV=50
        ZB_l.append(RSV)  
        i = i + 1          
        
    ZB_s = pd.Series(ZB_l)  
    rsv=ZB_s
    ZB = pd.Series(ZB_s, name = 'RSV')
    df = df.join(ZB)   
   
    i = 0 
    ZB_l = []
    y=1
    while i < len(df):
        y=(rsv[i]*1+(m1-1)*y)/m1
        ZB_l.append(y) 
        i=i+1
   
    ZB_s = pd.Series(ZB_l)  
    k=ZB_s 
    ZB = pd.Series(ZB_s, name = 'K')  
    df = df.join(ZB)   
    
    i = 0 
    ZB_l = []
    y=1
    while i < len(df):
        y=(k[i]*1+(m2-1)*y)/m2
        ZB_l.append(y) 
        i=i+1
   
    ZB_s = pd.Series(ZB_l)  
    d=ZB_s 
    ZB = pd.Series(ZB_s, name = 'D')  
    df = df.join(ZB)   
        
    j=3*k-2*d
    
    ZB = pd.Series(j, name = 'J')  
    df = df.join(ZB)   
    return df   

def OBVX(df, n,m):  
    i = 0  
    OBV = [0]  
    while i < df.index[-1]:  
        if df.get_value(i + 1, 'close') - df.get_value(i, 'close') > 0:  
            OBV.append(df.get_value(i + 1, 'volume'))  
        if df.get_value(i + 1, 'close') - df.get_value(i, 'close') == 0:  
            OBV.append(0)  
        if df.get_value(i + 1, 'close') - df.get_value(i, 'close') < 0:  
            OBV.append(-df.get_value(i + 1, 'volume'))  
        i = i + 1  
    OBV = pd.Series(OBV,name = 'OBV')  
    df=df.join(OBV)
    OBV_ma = pd.Series(pd.rolling_mean(OBV, n), name = 'OBV_' + str(n))  
    df = df.join(OBV_ma)  
    OBV_ma = pd.Series(pd.rolling_mean(OBV, m), name = 'OBV_' + str(m))  
    df = df.join(OBV_ma)  
    return df

#Relative Strength Index  
def RSIX(df, n,al=''):  
    if (al.strip()==''):
        na=tp1+'RSI_' + str(n)
    else:
        na=al
    i = 0  
    UpI = [0]  
    DoI = [0]  
    while i + 1 <= df.index[-1]:  
        UpMove = df.get_value(i + 1, 'high') - df.get_value(i, 'high')  
        DoMove = df.get_value(i, 'low') - df.get_value(i + 1, 'low')  
        if UpMove > DoMove and UpMove > 0:  
            UpD = UpMove  
        else: UpD = 0  
        UpI.append(UpD)  
        if DoMove > UpMove and DoMove > 0:  
            DoD = DoMove  
        else: DoD = 0  
        DoI.append(DoD)  
        i = i + 1  
    UpI = pd.Series(UpI)  
    DoI = pd.Series(DoI)  
    PosDI = pd.Series(pd.ewma(UpI, span = n, min_periods = n - 1))  
    NegDI = pd.Series(pd.ewma(DoI, span = n, min_periods = n - 1))  
    RSI = pd.Series(PosDI*100.00 / (PosDI + NegDI), name = na)  
    df = df.join(RSI)  
    return df



def MACDX(df, n_long, n_short,m): 
    d1=pd.Series(pd.ewma(df['close'], span = n_long, min_periods = n_long - 1))  
    #d1= pd.Series(df['close'].ewm(span = n_long, min_periods = n_long - 1,adjust=True,ignore_na=False).mean())  
    d2=pd.Series(pd.ewma(df['close'], span = n_short, min_periods = n_short - 1))  
    #d2= pd.Series(df['close'].ewm(span = n_short, min_periods = n_short - 1,adjust=True,ignore_na=False).mean())  
    diff = pd.Series(d1 - d2)
    #dea=pd.Series(pd.ewma(diff, span = m, min_periods = m - 1))  
    dea= pd.Series(diff.ewm(span = m, min_periods = m - 1,adjust=True,ignore_na=False).mean())  
    DIFF= pd.Series(diff,name='DIFF')
    DEA= pd.Series(dea,name='DEA')
    MACD = pd.Series(2*(diff-dea), name = 'MACD')  
    df = df.join(DIFF)  
    df = df.join(DEA)  
    df = df.join(MACD)  
    return df   

#MACD, MACD Signal and MACD difference  
def MACD(df, n_fast, n_slow):  
    EMAfast = pd.Series(pd.ewma(df['close'], span = n_fast, min_periods = n_slow - 1))  
    EMAslow = pd.Series(pd.ewma(df['close'], span = n_slow, min_periods = n_slow - 1))  
    MACD = pd.Series(EMAfast - EMAslow, name = 'MACD_' + str(n_fast) + '_' + str(n_slow))  
    MACDsign = pd.Series(pd.ewma(MACD, span = 9, min_periods = 8), name = 'MACDsign_' + str(n_fast) + '_' + str(n_slow))  
    MACDdiff = pd.Series(MACD - MACDsign, name = 'MACDdiff_' + str(n_fast) + '_' + str(n_slow))  
    df = df.join(MACD)  
    df = df.join(MACDsign)  
    df = df.join(MACDdiff)  
    return df

#Momentum  
def MOM(df, n):  
    M = pd.Series(df['close'].diff(n), name = 'Momentum_' + str(n))  
    df = df.join(M)  
    return df

#Rate of Change  
def ROC(df, n):  
    M = df['close'].diff(n - 1)  
    N = df['close'].shift(n - 1)  
    ROC = pd.Series(M / N, name = 'ROC_' + str(n))  
    df = df.join(ROC)  
    return df

#Average True Range  
def ATR(df, n):  
    i = 0  
    TR_l = [0]  
    while i < len(df.index):  
        TR = max(df.get_value(i + 1, 'high'), df.get_value(i, 'close')) - min(df.get_value(i + 1, 'low'), df.get_value(i, 'close'))  
        TR_l.append(TR)  
        i = i + 1  
    TR_s = pd.Series(TR_l)  
    ATR = pd.Series(pd.ewma(TR_s, span = n, min_periods = n), name = 'ATR_' + str(n))  
    df = df.join(ATR)  
    return df

#Bollinger Bands  
def BBANDS(df, n):  
    MA = pd.Series(pd.rolling_mean(df['close'], n))  
    MSD = pd.Series(pd.rolling_std(df['close'], n))  
    b1 = 4 * MSD / MA  
    B1 = pd.Series(b1, name = 'BollingerB_' + str(n))  
    df = df.join(B1)  
    b2 = (df['close'] - MA + 2 * MSD) / (4 * MSD)  
    B2 = pd.Series(b2, name = 'Bollinger%b_' + str(n))  
    df = df.join(B2)  
    return df

#Pivot Points, Supports and Resistances  
def PPSR(df):  
    PP = pd.Series((df['high'] + df['low'] + df['close']) / 3)  
    R1 = pd.Series(2 * PP - df['low'])  
    S1 = pd.Series(2 * PP - df['high'])  
    R2 = pd.Series(PP + df['high'] - df['low'])  
    S2 = pd.Series(PP - df['high'] + df['low'])  
    R3 = pd.Series(df['high'] + 2 * (PP - df['low']))  
    S3 = pd.Series(df['low'] - 2 * (df['high'] - PP))  
    psr = {'PP':PP, 'R1':R1, 'S1':S1, 'R2':R2, 'S2':S2, 'R3':R3, 'S3':S3}  
    PSR = pd.DataFrame(psr)  
    df = df.join(PSR)  
    return df

#Stochastic oscillator %K  
def STOK(df):  
    SOk = pd.Series((df['close'] - df['low']) / (df['high'] - df['low']), name = 'SO%k')  
    df = df.join(SOk)  
    return df

#Stochastic oscillator %D  
def STO(df, n):  
    SOk = pd.Series((df['close'] - df['low']) / (df['high'] - df['low']), name = 'SO%k')  
    SOd = pd.Series(pd.ewma(SOk, span = n, min_periods = n - 1), name = 'SO%d_' + str(n))  
    df = df.join(SOd)  
    return df

#Trix  
def TRIX(df, n):  
    EX1 = pd.ewma(df['close'], span = n, min_periods = n - 1)  
    EX2 = pd.ewma(EX1, span = n, min_periods = n - 1)  
    EX3 = pd.ewma(EX2, span = n, min_periods = n - 1)  
    i = 0  
    ROC_l = [0]  
    while i + 1 <= df.index[-1]:  
        ROC = (EX3[i + 1] - EX3[i]) / EX3[i]  
        ROC_l.append(ROC)  
        i = i + 1  
    Trix = pd.Series(ROC_l, name = 'Trix_' + str(n))  
    df = df.join(Trix)  
    return df

#Average Directional Movement Index  
def ADX(df, n, n_ADX):  
    i = 0  
    UpI = []  
    DoI = []  
    while i + 1 <= df.index[-1]:  
        UpMove = df.get_value(i + 1, 'high') - df.get_value(i, 'high')  
        DoMove = df.get_value(i, 'low') - df.get_value(i + 1, 'low')  
        if UpMove > DoMove and UpMove > 0:  
            UpD = UpMove  
        else: UpD = 0  
        UpI.append(UpD)  
        if DoMove > UpMove and DoMove > 0:  
            DoD = DoMove  
        else: DoD = 0  
        DoI.append(DoD)  
        i = i + 1  
    i = 0  
    TR_l = [0]  
    while i < df.index[-1]:  
        TR = max(df.get_value(i + 1, 'high'), df.get_value(i, 'close')) - min(df.get_value(i + 1, 'low'), df.get_value(i, 'close'))  
        TR_l.append(TR)  
        i = i + 1  
    TR_s = pd.Series(TR_l)  
    ATR = pd.Series(pd.ewma(TR_s, span = n, min_periods = n))  
    UpI = pd.Series(UpI)  
    DoI = pd.Series(DoI)  
    PosDI = pd.Series(pd.ewma(UpI, span = n, min_periods = n - 1) / ATR)  
    NegDI = pd.Series(pd.ewma(DoI, span = n, min_periods = n - 1) / ATR)  
    ADX = pd.Series(pd.ewma(abs(PosDI - NegDI) / (PosDI + NegDI), span = n_ADX, min_periods = n_ADX - 1), name = 'ADX_' + str(n) + '_' + str(n_ADX))  
    df = df.join(ADX)  
    return df



#Mass Index  
def MassI(df):  
    Range = df['high'] - df['low']  
    EX1 = pd.ewma(Range, span = 9, min_periods = 8)  
    EX2 = pd.ewma(EX1, span = 9, min_periods = 8)  
    Mass = EX1 / EX2  
    MassI = pd.Series(pd.rolling_sum(Mass, 25), name = 'Mass Index')  
    df = df.join(MassI)  
    return df

#Vortex Indicator: http://www.vortexindicator.com/VFX_VORTEX.PDF  
def Vortex(df, n):  
    i = 0  
    TR = [0]  
    while i < df.index[-1]:  
        Range = max(df.get_value(i + 1, 'high'), df.get_value(i, 'close')) - min(df.get_value(i + 1, 'low'), df.get_value(i, 'close'))  
        TR.append(Range)  
        i = i + 1  
    i = 0  
    VM = [0]  
    while i < df.index[-1]:  
        Range = abs(df.get_value(i + 1, 'high') - df.get_value(i, 'low')) - abs(df.get_value(i + 1, 'low') - df.get_value(i, 'high'))  
        VM.append(Range)  
        i = i + 1  
    VI = pd.Series(pd.rolling_sum(pd.Series(VM), n) / pd.rolling_sum(pd.Series(TR), n), name = 'Vortex_' + str(n))  
    df = df.join(VI)  
    return df





#KST Oscillator  
def KST(df, r1, r2, r3, r4, n1, n2, n3, n4):  
    M = df['close'].diff(r1 - 1)  
    N = df['close'].shift(r1 - 1)  
    ROC1 = M / N  
    M = df['close'].diff(r2 - 1)  
    N = df['close'].shift(r2 - 1)  
    ROC2 = M / N  
    M = df['close'].diff(r3 - 1)  
    N = df['close'].shift(r3 - 1)  
    ROC3 = M / N  
    M = df['close'].diff(r4 - 1)  
    N = df['close'].shift(r4 - 1)  
    ROC4 = M / N  
    KST = pd.Series(pd.rolling_sum(ROC1, n1) + pd.rolling_sum(ROC2, n2) * 2 + pd.rolling_sum(ROC3, n3) * 3 + pd.rolling_sum(ROC4, n4) * 4, name = 'KST_' + str(r1) + '_' + str(r2) + '_' + str(r3) + '_' + str(r4) + '_' + str(n1) + '_' + str(n2) + '_' + str(n3) + '_' + str(n4))  
    df = df.join(KST)  
    return df

#Relative Strength Index  
def RSI(df, n):  
    i = 0  
    UpI = [0]  
    DoI = [0]  
    while i + 1 <= df.index[-1]:  
        UpMove = df.get_value(i + 1, 'high') - df.get_value(i, 'high')  
        DoMove = df.get_value(i, 'low') - df.get_value(i + 1, 'low')  
        if UpMove > DoMove and UpMove > 0:  
            UpD = UpMove  
        else: UpD = 0  
        UpI.append(UpD)  
        if DoMove > UpMove and DoMove > 0:  
            DoD = DoMove  
        else: DoD = 0  
        DoI.append(DoD)  
        i = i + 1  
    UpI = pd.Series(UpI)  
    DoI = pd.Series(DoI)  
    PosDI = pd.Series(pd.ewma(UpI, span = n, min_periods = n - 1))  
    NegDI = pd.Series(pd.ewma(DoI, span = n, min_periods = n - 1))  
    RSI = pd.Series(PosDI / (PosDI + NegDI), name = 'RSI_' + str(n))  
    df = df.join(RSI)  
    return df

#True Strength Index  
def TSI(df, r, s):  
    M = pd.Series(df['close'].diff(1))  
    aM = abs(M)  
    EMA1 = pd.Series(pd.ewma(M, span = r, min_periods = r - 1))  
    aEMA1 = pd.Series(pd.ewma(aM, span = r, min_periods = r - 1))  
    EMA2 = pd.Series(pd.ewma(EMA1, span = s, min_periods = s - 1))  
    aEMA2 = pd.Series(pd.ewma(aEMA1, span = s, min_periods = s - 1))  
    TSI = pd.Series(EMA2 / aEMA2, name = 'TSI_' + str(r) + '_' + str(s))  
    df = df.join(TSI)  
    return df

#Accumulation/Distribution  
def ACCDIST(df, n):  
    ad = (2 * df['close'] - df['high'] - df['low']) / (df['high'] - df['low']) * df['volume']  
    M = ad.diff(n - 1)  
    N = ad.shift(n - 1)  
    ROC = M / N  
    AD = pd.Series(ROC, name = 'Acc/Dist_ROC_' + str(n))  
    df = df.join(AD)  
    return df

#Chaikin Oscillator  
def Chaikin(df):  
    ad = (2 * df['close'] - df['high'] - df['low']) / (df['high'] - df['low']) * df['volume']  
    Chaikin = pd.Series(pd.ewma(ad, span = 3, min_periods = 2) - pd.ewma(ad, span = 10, min_periods = 9), name = 'Chaikin')  
    df = df.join(Chaikin)  
    return df

#Money Flow Index and Ratio  
def MFI(df, n):  
    PP = (df['high'] + df['low'] + df['close']) / 3  
    i = 0  
    PosMF = [0]  
    while i < df.index[-1]:  
        if PP[i + 1] > PP[i]:  
            PosMF.append(PP[i + 1] * df.get_value(i + 1, 'volume'))  
        else:  
            PosMF.append(0)  
        i = i + 1  
    PosMF = pd.Series(PosMF)  
    TotMF = PP * df['volume']  
    MFR = pd.Series(PosMF / TotMF)  
    MFI = pd.Series(pd.rolling_mean(MFR, n), name = 'MFI_' + str(n))  
    df = df.join(MFI)  
    return df

#On-balance volume  
def OBV(df, n):  
    i = 0  
    OBV = [0]  
    while i < df.index[-1]:  
        if df.get_value(i + 1, 'close') - df.get_value(i, 'close') > 0:  
            OBV.append(df.get_value(i + 1, 'volume'))  
        if df.get_value(i + 1, 'close') - df.get_value(i, 'close') == 0:  
            OBV.append(0)  
        if df.get_value(i + 1, 'close') - df.get_value(i, 'close') < 0:  
            OBV.append(-df.get_value(i + 1, 'volume'))  
        i = i + 1  
    OBV = pd.Series(OBV)  
    OBV_ma = pd.Series(pd.rolling_mean(OBV, n), name = 'OBV_' + str(n))  
    df = df.join(OBV_ma)  
    return df

#Force Index  
def FORCE(df, n):  
    F = pd.Series(df['close'].diff(n) * df['volume'].diff(n), name = 'Force_' + str(n))  
    df = df.join(F)  
    return df

#Ease of Movement  
def EOM(df, n):  
    EoM = (df['high'].diff(1) + df['low'].diff(1)) * (df['high'] - df['low']) / (2 * df['volume'])  
    Eom_ma = pd.Series(pd.rolling_mean(EoM, n), name = 'EoM_' + str(n))  
    df = df.join(Eom_ma)  
    return df

#Commodity Channel Index  
def CCI(df, n):  
    PP = (df['high'] + df['low'] + df['close']) / 3  
    CCI = pd.Series((PP - pd.rolling_mean(PP, n)) / pd.rolling_std(PP, n), name = 'CCI_' + str(n))  
    df = df.join(CCI)  
    return df

#Coppock Curve  
def COPP(df, n):  
    M = df['close'].diff(int(n * 11 / 10) - 1)  
    N = df['close'].shift(int(n * 11 / 10) - 1)  
    ROC1 = M / N  
    M = df['close'].diff(int(n * 14 / 10) - 1)  
    N = df['close'].shift(int(n * 14 / 10) - 1)  
    ROC2 = M / N  
    Copp = pd.Series(pd.ewma(ROC1 + ROC2, span = n, min_periods = n), name = 'Copp_' + str(n))  
    df = df.join(Copp)  
    return df

#Keltner Channel  
def KELCH(df, n):  
    KelChM = pd.Series(pd.rolling_mean((df['high'] + df['low'] + df['close']) / 3, n), name = 'KelChM_' + str(n))  
    KelChU = pd.Series(pd.rolling_mean((4 * df['high'] - 2 * df['low'] + df['close']) / 3, n), name = 'KelChU_' + str(n))  
    KelChD = pd.Series(pd.rolling_mean((-2 * df['high'] + 4 * df['low'] + df['close']) / 3, n), name = 'KelChD_' + str(n))  
    df = df.join(KelChM)  
    df = df.join(KelChU)  
    df = df.join(KelChD)  
    return df

#Ultimate Oscillator  
def ULTOSC(df):  
    i = 0  
    TR_l = [0]  
    BP_l = [0]  
    while i < df.index[-1]:  
        TR = max(df.get_value(i + 1, 'high'), df.get_value(i, 'close')) - min(df.get_value(i + 1, 'low'), df.get_value(i, 'close'))  
        TR_l.append(TR)  
        BP = df.get_value(i + 1, 'close') - min(df.get_value(i + 1, 'low'), df.get_value(i, 'close'))  
        BP_l.append(BP)  
        i = i + 1  
    UltO = pd.Series((4 * pd.rolling_sum(pd.Series(BP_l), 7) / pd.rolling_sum(pd.Series(TR_l), 7)) + (2 * pd.rolling_sum(pd.Series(BP_l), 14) / pd.rolling_sum(pd.Series(TR_l), 14)) + (pd.rolling_sum(pd.Series(BP_l), 28) / pd.rolling_sum(pd.Series(TR_l), 28)), name = 'Ultimate_Osc')  
    df = df.join(UltO)  
    return df

#Donchian Channel  
def DONCH(df, n):  
    i = 0  
    DC_l = []  
    while i < n - 1:  
        DC_l.append(0)  
        i = i + 1  
    i = 0  
    while i + n - 1 < df.index[-1]:  
        DC = max(df['high'].ix[i:i + n - 1]) - min(df['low'].ix[i:i + n - 1])  
        DC_l.append(DC)  
        i = i + 1  
    DonCh = pd.Series(DC_l, name = 'Donchian_' + str(n))  
    DonCh = DonCh.shift(n - 1)  
    df = df.join(DonCh)  
    return df

#####################回测功能#########################
def Trade_testing(df,tp1,tp2,al=''):
    money=1000000.00  #总资金
    priceBuy=0.00    #最后一次买入价格
    priceSell=999999.00  #最后一次卖出价格
    security=0.00   #证券数量
    #securityName=""   #证券代码
    stamp_duty=0.001   #印花税 0.1%
    trading_Commission=0.0005    #交易佣金0.05%
    priceStopLoss=0.00   #止损价
    position=False   #持仓状态
    stop_loss_num=0   #止损次数
    stop_loss_max=50 #止损3次,就停止交易
    stop_loss_range=0.05   #止损幅度

    trade=True   #允许交易
    if (al.strip()==''):
        na='property'
    else:
        na=al 

    print('----开始回测-----')
    i = 0  
    ZB_l = []
    y=money
    while i < df.index[-1]+1:  
        if (df.get_value(i, tp1) >0 and position==False and trade==True) :  #买点
            priceBuy=df.get_value(i, 'close')
            x=int(money/(priceBuy*(1+trading_Commission))/100)
            security=x*100.00
            money=money-security*priceBuy*(1.00+trading_Commission)
            position=True
            priceStopLoss=priceBuy*(1-stop_loss_range)
            print('日期:',df.get_value(i, 'date'),'买入:',security,'股,价格:',priceBuy)
            
        if (df.get_value(i, tp2) >0 and position==True and trade==True) : #卖点
            priceSell=df.get_value(i, 'close')
            money=money+security*priceSell*(1.00-trading_Commission-stamp_duty)
            position=False
            print('日期:',df.get_value(i, 'date'),'卖出:',security,'股,价格:',priceSell,'获利:',(money-1000000.00)/10000,'%')
            security=0.00
            
        if (df.get_value(i, 'close')<=priceStopLoss and position==True and trade):  #止损
            #priceSell=df.get_value(i, 'close')
            priceSell=priceStopLoss-0.01
            money=money+security*priceSell*(1.00-trading_Commission-stamp_duty)
            position=False
            stop_loss_num=stop_loss_num+1
            print('日期:',df.get_value(i, 'date'),'止损:',security,'股,价格:',priceSell,'获利:',(money-1000000.00)/10000,'%')
            security=0.00
            if (stop_loss_num>=stop_loss_max):
                trade=False
                

        y= (money+security*df.get_value(i, 'close')-1000000.00)/10000              
        ZB_l.append(y)  
        i = i + 1          
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = na)  
    df = df.join(ZB)  
    print('总投入:1000000.00,最终获利幅度',y,'%')
    return df
   
###########################有问题的测试代码####################
#N周期线性回归线的斜率
def SLOPE(df,tp, n):  
    i = n-1  
    ZB_l = []
    lxx=0.0
    lxy=0.0
    while i< df.index[-1]:  
        j=n
        x=0.0
        y=0.0	
        while j>0:
            x=j+x
            y=df.get_value(j-1, tp)+y 
            j=j-1
        x=x/n
        y=y/n
        j=1
        while j<n:
            lxx=lxx+(j-x)*(j-x)
            lxy=lxy+(j-x)*( df.get_value(j-1, tp)-y)
            j=j+1
        slope=-lxy/lxx
        ZB_l.append(slope)  
        i = i + 1          
        
    ZB_s = pd.Series(ZB_l)  
    ZB = pd.Series(ZB_s, name = 'SLOPE_' + str(n))  
    df = df.join(ZB)   
    return df