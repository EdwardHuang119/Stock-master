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
#最后修改日期:2018年9月26日
#主程序：HP_main.py
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
import pandas as pd  
import numpy  as np
import HP_VIEW.HP_global as g

"""
Series 类

这个是下面以DataFrame为输入的基础函数
return pd.Series format
"""
def EMA(Series, N):
    return pd.Series.ewm(Series, span=N, min_periods=N - 1, adjust=True).mean()

def MA(Series, N):
    return pd.Series.rolling(Series, N).mean()

def SMA(Series, N, M=1):
    ret = []
    i = 1
    length = len(Series)
    # 跳过X中前面几个 nan 值
    while i < length:
        if np.isnan(Series.iloc[i]):
            i += 1
        else:
            break
    preY = Series.iloc[i]  # Y'
    ret.append(preY)
    while i < length:
        Y = (M * Series.iloc[i] + (N - M) * preY) / float(N)
        ret.append(Y)
        preY = Y
        i += 1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

def DIFF(Series, N=1):
    return pd.Series(Series).diff(N)

def HHV(Series, N):
    return pd.Series(Series).rolling(N).max()

def LLV(Series, N):
    return pd.Series(Series).rolling(N).min()

def SUMX(Series, N):
    if N<=0:
        N=len(Series)
    sum=pd.Series.rolling(Series, N).sum()
    return pd.Series(sum,name='sums')

def ABS(Series):
    return abs(Series)

def MAX(A, B):
    var = IF(A > B, A, B)
    return pd.Series( var,name='maxs')

def MIN(A, B):
    var = IF(A < B, A, B)
    return var

def SINGLE_CROSS(A, B):
    if A.iloc[-2] < B.iloc[-2] and A.iloc[-1] > B.iloc[-1]:
        return True
    else:
        return False

def CROSS(A, B):
    var = np.where(A<B, 1, 0)
    return (pd.Series(var, index=A.index).diff()<0).apply(int)

def COUNT(COND, N):
    return pd.Series(np.where(COND,1,0),index=COND.index).rolling(N).sum()

def IF(COND, V1, V2):
    var = np.where(COND, V1, V2)
    return pd.Series(var, index=V1.index)

def REF(Series, N):
    var = Series.diff(N)
    var = Series - var
    return var

def LAST(COND, N1, N2):
    N2 = 1 if N2 == 0 else N2
    assert N2 > 0
    assert N1 > N2
    return COND.iloc[-N1:-N2].all()

def STD(Series, N):
    return pd.Series.rolling(Series, N).std()

def AVEDEV(Series, N):
    return Series.rolling(N).apply(lambda x: (np.abs(x - x.mean())).mean(), raw=True)

def DMA(ser_,para_):#DMA函数(para<1)
    ser_,para_,dma_=list(ser_),list(para_),[ser_[0],]
    for i in range(1,len(ser_)):
        dma_.append(para_[i]*ser_[i]+(1-para_[i])*dma_[-1])
    return dma_

##########################################
#def MACD(Series, FAST, SLOW, MID):
#    EMAFAST = EMA(Series, FAST)
#    EMASLOW = EMA(Series, SLOW)
#    DIFF = EMAFAST - EMASLOW
#    DEA = EMA(DIFF, MID)
#    MACD = (DIFF - DEA) * 2
#    DICT = {'DIFF': DIFF, 'DEA': DEA, 'MACD': MACD}
#    VAR = pd.DataFrame(DICT)
#    return VAR
#
#
#def BBIBOLL(Series, N1, N2, N3, N4, N, M):  # 多空布林线
#
#    bbiboll = BBI(Series, N1, N2, N3, N4)
#    UPER = bbiboll + M * STD(bbiboll, N)
#    DOWN = bbiboll - M * STD(bbiboll, N)
#    DICT = {'BBIBOLL': bbiboll, 'UPER': UPER, 'DOWN': DOWN}
#    VAR = pd.DataFrame(DICT)
#    return VAR
#
#
#def BBI(Series, N1, N2, N3, N4):
#    '多空指标'
#
#    bbi = (MA(Series, N1) + MA(Series, N2) +
#           MA(Series, N3) + MA(Series, N4)) / 4
#    DICT = {'BBI': bbi}
#    VAR = pd.DataFrame(DICT)
#    return VAR



def Para_cs(ser_,peri_):
    ser_,peri_=list(ser_),list(peri_)
    cs_=[]
    s_t=[]
    for i in range(len(ser_)):
        if i==0:sum_temp=0
        else:sum_temp=abs(ser_[i]-ser_[i-1])
        peri_temp=peri_[i]*2+1
        s_t.append(sum_temp)
        if i<peri_[i]:cs_.append(abs(ser_[i]-ser_[0])/sum(s_t[1:i+1])*(0.8-2/peri_temp)+2/peri_temp)
        else:cs_.append(abs(ser_[i]-ser_[i-peri_[i]])/sum(s_t[i-peri_[i]+1:i+1])*(0.8-2/peri_temp)+2/peri_temp)
    return list(map(lambda x:x*x,cs_))


def BACK_(ser_,p1_,p2_,p3_,p4_):
    ser_,p1,p2,p3,p4,back_=list(ser_),list(p1_),list(p2_),list(p3_),list(p4_),[]
    for i in range(len(ser_)):
        val_= [ser_[i],p1[i],p2[i],p3[i],p4[i]]   
        val_.sort()
        back_.append(val_[val_.index(ser_[i])-1]) if val_.index(ser_[i])>0 else back_.append(ser_[i])
    return back_
def BACK(ser_,p1,p2,p3,p4):#下方最近周期数
    ser_=list(ser_)
    back_=[]
    for i in range(len(ser_)):
        val_= [ser_[i],p1,p2,p3,p4]   
        val_.sort()
        back_.append(val_[val_.index(ser_[i])-1]) if val_.index(ser_[i])>0 else back_.append(ser_[i])
    return back_


def RESIS_(ser_,p1_,p2_,p3_,p4_):
    ser_,p1,p2,p3,p4,resis_=list(ser_),list(p1_),list(p2_),list(p3_),list(p4_),[]
    for i in range(len(ser_)):
        val_= [ser_[i],p1[i],p2[i],p3[i],p4[i]]   
        val_.sort(reverse=True)
        resis_.append(val_[val_.index(ser_[i])-1]) if val_.index(ser_[i])>0 else resis_.append(10000)
    return resis_
def MTR(high,low,close):
    a,b,c = high - low,np.abs(close.shift(1) - high),np.abs(close.shift(1) - low)
    mtr = a.where(a>b, b)
    mtr =  mtr.where(mtr>c, c)
    return mtr 

def LLVBARS(price,window):
    return price.rolling(window).apply(lambda x:window-np.argmin(x)-1)
def HHVBARS(price,window):
    return price.rolling(window).apply(lambda x:window-np.argmax(x)-1)

def AND_(cond1_,cond2_):
    cond1_,cond2_,cond_=list(cond1_),list(cond2_),[]
    for i in range(len(cond1_)):
        if cond1_==True and cond2_==True:cond_.append(True)
        else :cond_.append(False)
    return cond_
def OR_(cond1_,cond2_):
    cond1_,cond2_,cond_=list(cond1_),list(cond2_),[]
    for i in range(len(cond1_)):
        if cond1_==False and cond2_==False:cond_.append(False)
        else :cond_.append(True)
    return cond_

def REF_(ser_,peri_):
    ser_,peri_,ref_=list(ser_),list(peri_),[]
    for i in range(len(ser_)):
        if i<peri_[i]:ref_.append(np.nan)
        else:ref_.append(ser_[i-peri_[i]])
    return ref_

def REF(ser_,p):
    ser_,ref_=list(ser_),[]
    for i in range(p):
        ref_.append(np.nan)
    for i in range(len(ser_)-p):
        ref_.append(ser_[i])
    return ref_

def SUM_(ser_,peri_):
    ser_,peri_,sum_=list(ser_),list(peri_),[ser_[0],]
    for i in range(1,len(ser_)):
        if i+1<peri_[i]:sum_.append(sum(ser_[:i+1]))
        else:sum_.append(sum(seri_[i+1-per_[i]:i+1]))
    return sum_

def SUM(ser_,p):
    ser_,sum_=list(ser_),[ser_[0],]
    for i in range(1,len(ser_)):
        if i<p:sum_.append(sum(ser_[:i+1]))
        else:sum_.append(sum(ser_[i+1-p:i+1]))
    return sum_

def MA_(ser_,peri_):
    ser_,peri_,ma_=list(ser_),list(peri_),[ser_[0],]
    for i in range(1,len(ser_)):
        if i+1<peri_[i]:ma_.append(sum(ser_[:i+1])/(i+1))
        else:ma_.append(sum(ser_[i+1-peri_[i]:i+1])/peri_[i])
    return ma_

def CROSS_(ser_a,ser_b):
    ser_a,ser_b,sig_=list(ser_a),list(ser_b),[0,]
    for i in range(1,len(ser_a)):
        sig_.append(1) if ser_a[i]>ser_b[i] and ser_a[i-1]<=ser_b[i-1] else sig_.append(0)
    return sig_

def BARSLAST_AB(ser_a,ser_b):
    ser_a,ser_b,sig_,bars_,lenth=list(ser_a),list(ser_b),[0,],[],len(ser_a)
    for i in range(1,lenth):
        sig_.append(1) if ser_a[i]>ser_b[i] and ser_a[i-1]<=ser_b[i-1] else sig_.append(0)
    first_=sig_.index(1)
    for i in range(first_):
        bars_.append(np.nan)
    for i in range(first_,lenth):
        if sig_[i]==1:
            count_=0
            bars_.append(0)
        else:
            count_+=1
            bars_.append(count_)
    return bars_   

def BARSLAST_COND(ser_cond):
    ser_cond,sig_,bars_,lenth=list(ser_cond),[0,],[],len(ser_cond)
    for i in range(1,lenth):
        sig_.append(1) if ser_cond[i]==True and ser_cond[i-1]==False else sig_.append(0)
    first_=sig_.index(1)
    for i in range(first_):
        bars_.append(np.nan)
    for i in range(first_,lenth):
        if sig_[i]==1:
            count_=0
            bars_.append(0)
        else:
            count_+=1
            bars_.append(count_)
    return bars_ 

def COUNT_(cond_,peri_):
    cond_,peri_,count_=list(cond_),list(peri_),[]
    for i in range(len(cond_)):
        if i<peri_[i]:
            count_.append(np.nan)
            break
        count_t=0
        for j in range(peri_[i]):
            if cond_[-j-1]==True:
                count_t+=1
        count_.append(count_t)
    return count_    


ZIG_STATE_START = 0
ZIG_STATE_RISE = 1
ZIG_STATE_FALL = 2
def zig(k,x=0.055):
    '''
    #之字转向
    CLOSE=mydf['close']
    zz=zig(CLOSE,x=0.055) 
    mydf = mydf.join(pd.Series(zz,name='zz'))  #增加 J到 mydf中1
    mydf.zz.plot.line()
    CLOSE.plot.line()
    '''
    d = k.index
    peer_i = 0
    candidate_i = None
    scan_i = 0
    peers = [0]
    z = np.zeros(len(k))
    state = ZIG_STATE_START
    while True:
        scan_i += 1
        if scan_i == len(k) - 1:
            # 扫描到尾部
            if candidate_i is None:
                peer_i = scan_i
                peers.append(peer_i)
            else:
                if state == ZIG_STATE_RISE:
                    if k[scan_i] >= k[candidate_i]:
                        peer_i = scan_i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = scan_i
                        peers.append(peer_i)
                elif state == ZIG_STATE_FALL:
                    if k[scan_i] <= k[candidate_i]:
                        peer_i = scan_i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = scan_i
                        peers.append(peer_i)
            break
 
        if state == ZIG_STATE_START:
            if k[scan_i] >= k[peer_i] * (1 + x):
                candidate_i = scan_i
                state = ZIG_STATE_RISE
            elif k[scan_i] <= k[peer_i] * (1 - x):
                candidate_i = scan_i
                state = ZIG_STATE_FALL
        elif state == ZIG_STATE_RISE:
            if k[scan_i] >= k[candidate_i]:
                candidate_i = scan_i
            elif k[scan_i] <= k[candidate_i]*(1-x):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_FALL
                candidate_i = scan_i
        elif state == ZIG_STATE_FALL:
            if k[scan_i] <= k[candidate_i]:
                candidate_i = scan_i
            elif k[scan_i] >= k[candidate_i]*(1+x):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_RISE
                candidate_i = scan_i
    
    #线性插值， 计算出zig的值            
    for i in range(len(peers) - 1):
        peer_start_i = peers[i]
        peer_end_i = peers[i+1]
        start_value = k[peer_start_i]
        end_value = k[peer_end_i]
        a = (end_value - start_value)/(peer_end_i - peer_start_i)# 斜率
        for j in range(peer_end_i - peer_start_i +1):
            z[j + peer_start_i] = start_value + a*j
    
    return z
    
#####################################################
#常用股票公式，需要预先处理股票数据
'''
#首先要对数据预处理
#df = hp.get_k_data('600080',ktype='D')
mydf=df.copy()
CLOSE=mydf['close']
LOW=mydf['low']
HIGH=mydf['high']
OPEN=mydf['open']
VOL=mydf['volume']
C=mydf['close']
L=mydf['low']
H=mydf['high']
O=mydf['open']
V=mydf['volume']

'''
def KDJ(N=9, M1=3, M2=3):
    """
    KDJ 随机指标
    """
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = EMA(RSV, (M1 * 2 - 1))
    D = EMA(K, (M2 * 2 - 1))
    J = K * 3 - D * 2

    return K, D, J


def DMI(M1=14, M2=6):
    """
    DMI 趋向指标
    """
    TR = SUM(MAX(MAX(HIGH - LOW, ABS(HIGH - REF(CLOSE, 1))), ABS(LOW - REF(CLOSE, 1))), M1)
    HD = HIGH - REF(HIGH, 1)
    LD = REF(LOW, 1) - LOW

    DMP = SUM(IF((HD > 0) & (HD > LD), HD, 0), M1)
    DMM = SUM(IF((LD > 0) & (LD > HD), LD, 0), M1)
    DI1 = DMP * 100 / TR
    DI2 = DMM * 100 / TR
    ADX = MA(ABS(DI2 - DI1) / (DI1 + DI2) * 100, M2)
    ADXR = (ADX + REF(ADX, M2)) / 2

    return DI1, DI2, ADX, ADXR


def MACD(SHORT=12, LONG=26, M=9):
    """
    MACD 指数平滑移动平均线
    """
    DIFF = EMA(CLOSE, SHORT) - EMA(CLOSE, LONG)
    DEA = EMA(DIFF, M)
    MACD = (DIFF - DEA) * 2

    return DIFF,DEA,MACD


def RSI(N1=6, N2=12, N3=24):
    """
    RSI 相对强弱指标
    """
    LC = REF(CLOSE, 1)
    RSI1 = SMA(MAX(CLOSE - LC, 0), N1, 1) / SMA(ABS(CLOSE - LC), N1, 1) * 100
    RSI2 = SMA(MAX(CLOSE - LC, 0), N2, 1) / SMA(ABS(CLOSE - LC), N2, 1) * 100
    RSI3 = SMA(MAX(CLOSE - LC, 0), N3, 1) / SMA(ABS(CLOSE - LC), N3, 1) * 100

    return RSI1, RSI2, RSI3


def BOLL(N=20, P=2):
    """
    BOLL 布林带
    """
    MID = MA(CLOSE, N)
    UPPER = MID + STD(CLOSE, N) * P
    LOWER = MID - STD(CLOSE, N) * P

    return UPPER, MID, LOWER


def WR(N=10, N1=6):
    """
    W&R 威廉指标
    """
    WR1 = (HHV(HIGH, N) - CLOSE) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    WR2 = (HHV(HIGH, N1) - CLOSE) / (HHV(HIGH, N1) - LLV(LOW, N1)) * 100

    return WR1, WR2


def BIAS(L1=5, L4=3, L5=10):
    """
    BIAS 乖离率
    """
    BIAS = (CLOSE - MA(CLOSE, L1)) / MA(CLOSE, L1) * 100
    BIAS2 = (CLOSE - MA(CLOSE, L4)) / MA(CLOSE, L4) * 100
    BIAS3 = (CLOSE - MA(CLOSE, L5)) / MA(CLOSE, L5) * 100
    return BIAS, BIAS2, BIAS3


def ASI(M1=26, M2=10):
    """
    ASI 震动升降指标
    """
    LC = REF(CLOSE, 1)
    AA = ABS(HIGH - LC)
    BB = ABS(LOW - LC)
    CC = ABS(HIGH - REF(LOW, 1))
    DD = ABS(LC - REF(OPEN, 1))
    R = IF((AA > BB) & (AA > CC), AA + BB / 2 + DD / 4, IF((BB > CC) & (BB > AA), BB + AA / 2 + DD / 4, CC + DD / 4))
    X = (CLOSE - LC + (CLOSE - OPEN) / 2 + LC - REF(OPEN, 1))
    SI = X * 16 / R * MAX(AA, BB)
    ASI = SUM(SI, M1)
    ASIT = MA(ASI, M2)
    return ASI, ASIT


def VR(M1=26):
    """
    VR容量比率
    """
    LC = REF(CLOSE, 1)
    VR = SUM(IF(CLOSE > LC, VOL, 0), M1) / SUM(IF(CLOSE <= LC, VOL, 0), M1) * 100
    return VR


def ARBR(M1=26):
    """
    ARBR人气意愿指标
    """
    AR = SUM(HIGH - OPEN, M1) / SUM(OPEN - LOW, M1) * 100
    BR = SUM(MAX(0, HIGH - REF(CLOSE, 1)), M1) / SUM(MAX(0, REF(CLOSE, 1) - LOW), M1) * 100
    return AR, BR


def DPO(M1=20, M2=10, M3=6):
    DPO = CLOSE - REF(MA(CLOSE, M1), M2)
    MADPO = MA(DPO, M3)
    return DPO, MADPO


def TRIX(M1=12, M2=20):
    TR = EMA(EMA(EMA(CLOSE, M1), M1), M1)
    TRIX = (TR - REF(TR, 1)) / REF(TR, 1) * 100
    TRMA = MA(TRIX, M2)
    return TRIX, TRMA
   



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