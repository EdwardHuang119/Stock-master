# -*- coding: utf-8 -*-
#pytdx小白量化框架数据接口
##pip install pytdx
#买<零基础搭建量化投资系统>,送小白量化软件源代码。
#独狼荷蒲qq:2775205
#通通python量化群:524949939
#电话微信:18578755056
#最后修改日期:2021年3月21日
import datetime as dt
import pandas as pd
from pytdx.hq import TdxHq_API
from pytdx.exhq import TdxExHq_API, TDXParams
from pytdx.config.hosts import hq_hosts

global tdxapiex

def exhq():
    ex_api = TdxExHq_API(auto_retry=True, raise_exception=False)
    try:
        is_tdx_ex_connect = ex_api.connect('106.14.95.149', 7727, time_out=30)
    except Exception as e:
        print('time out to connect to pytdx')
        print(e)
    if is_tdx_ex_connect is not False:# 失败了返回False，成功了返回地址
        print('connect to pytdx extend api successful')
    else:
        ex_api=None
    return ex_api


global tdxapi,servers,hqhosts
global hqstop
hqstop=False
hqhosts=[]
tdxapi=None
global scode #股票代码
scode=''
global smarket #股票市场
smarket=0

servers2=['59.173.18.140',\
         '119.147.212.81',\
         '183.60.224.178',\
         '183.60.224.178',\
         'tdx.xmzq.com.cn',\
         '58.23.131.163',\
         '218.6.170.47',\
         '123.125.108.14',\
         '59.110.61.176',\
         '106.14.76.29',\
         '139.196.174.113',\
         '139.196.175.118',\
         '120.77.76.11',\
         '180.153.18.170']

servers=['180.153.18.171',\
         '218.6.170.55',\
         '58.67.221.146',\
         '103.24.178.242',\
         '114.80.63.35',\
         '180.153.39.51',\
         '123.125.108.23',\
         '123.125.108.24',\
         '114.80.63.12',\
         '61.147.174.2',\
         '36.152.49.226',\
         '218.98.6.162',\
         '218.201.105.52',\
         '202.108.253.130',\
         '180.153.18.170']

#tdx接口初始化
def TdxInit(ip='59.173.18.140',port=7709):
    global tdxapi
    tdxapi = TdxHq_API(heartbeat=True)
    result=tdxapi.connect(ip, port)
    if result==None:
        return None
    return tdxapi


#tdx接口初始化
def TdxInit2():
    global tdxapi,servers,hqhosts
    global hqstop
    tdxapi = TdxHq_API(heartbeat=True)
    for i in range(len(servers)):
        hq_hosts.insert(0,('新增',servers[i],7709))
    result=None
    hqhosts=hq_hosts
    #print(len(hq_hosts))
    i=0
    while result==False and i<len(hqhosts) and hqstop==False:
        result=tdxapi.connect(hqhosts[i][1], hqhosts[i][2])
        i+=1
        if i>10:
            break
    if result==None:
        return None
    return tdxapi

def tdx_ping_future(ip, port=7709, type_='stock'):
    apix = TdxExHq_API()
    __time1 = dt.datetime.now()
    try:
       with apix.connect(ip, port, time_out=0.7):
            res = apix.get_instrument_count()
            if res is not None:
                if res > 40000:
                    return dt.datetime.now() - __time1
                else:
                    #print('️Bad FUTUREIP REPSONSE {}'.format(ip))
                    return dt.timedelta(9, 9, 0)
            else:
                #print('️Bad FUTUREIP REPSONSE {}'.format(ip))
                return dt.timedelta(9, 9, 0)
    #
    except Exception as e:
        pass
        #print('BAD RESPONSE {}'.format(ip))
        return dt.timedelta(9, 9, 0)


def disconnect():
    global tdxapi
    tdxapi.disconnect()
    tdxapi=None
    return None


def get_market(code):
    c=code[0:1]
    y=0
    if c=='6' or c=='5':
        y=1
    return y

#获取股票代码表
def GetSecurityList(nMarket = 0):
    global tdxapi
    #nMarket = 0    # 0 - 深圳  1 - 上海
    nStart = 0
    
    m=tdxapi.get_security_count(nMarket)
    df=tdxapi.to_df(tdxapi.get_security_list(nMarket, nStart))
    df=pd.DataFrame(columns = ['code','name','pre_close']) 
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    while nStart<m:
        result = tdxapi.get_security_list(nMarket, nStart)
        df2=tdxapi.to_df(result)
        df=df.append( df2,ignore_index=True)            
        nStart=nStart+1000
    return df

#获取深圳股票代码表
def getSZ():
    base=GetSecurityList(0)
    base.to_csv('./data/sz.csv' , encoding= 'gbk')
    return base

#获取上海股票代码表
def getSH():
    base=GetSecurityList(1)
    base.to_csv('./data/sh.csv' , encoding= 'gbk')
    return base

#日线级别k线获取函数
def get_k_data(code='600030',ktype='D',start='1991-01-01',end='2018-10-15',\
               index=False,autype='qfq'):
    global tdxapi,scode,smarket
    scode=code
    df1 = tdxapi.get_k_data(code, start, end)
    df1=df1.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    df1.rename(columns={'vol':'volume'}, inplace = True)
    df1['code']=code
    df1['ktype']=ktype
    return df1


#获取除权除息数据
def get_xdxr_info(nMarket = 0,code='000001'):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    #nMarket = 0    # 0 - 深圳  1 - 上海
    result= tdxapi.get_xdxr_info(nMarket, code)
    df=tdxapi.to_df(result)
    df['code']=code
    df['market']=nMarket    
    return df


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
def get_security_bars(nCategory=4,nMarket = -1,code='000776',\
                    nStart=0, nCount=240):
    global tdxapi,scode,smarket
    scode=code
    if nMarket == -1:
        nMarket=get_market(code)
    smarket=nMarket        
    result =tdxapi.get_security_bars(nCategory, nMarket,code, nStart, nCount)
    df=tdxapi.to_df(result)
    #a=[x[0:10] for x in df.datetime]
    #df.insert(0,'date',a)
    df['date']=df['datetime']
    df['volume']=df['vol']
    df['code']=code
    df['market']=nMarket
    df['category']=nCategory
    return df

def get_all_data(nCategory=4,nMarket = 0,code='000776'):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    data=[]
    for i in range(10):
          data+=tdxapi.get_security_bars(nCategory, nMarket,code,(9-i)*800,800)
    df=tdxapi.to_df(data)
    df['date']=df['datetime']
    df['volume']=df['vol']
    df['code']=code
    df['market']=nMarket
    df['category']=nCategory    
    return df

def get_index_bars(nCategory=4,nMarket = 1,code='000001',\
                    nStart=0, nCount=240):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    result =tdxapi.get_index_bars(nCategory, nMarket,code, nStart, nCount)
    df=tdxapi.to_df(result)
    return df

#"查询分时行情"
def get_minute_time_data(nMarket = 0,code='000776'):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    #nMarket = 0    # 0 - 深圳  1 - 上海
    result= tdxapi.get_minute_time_data(nMarket, code)
    df=tdxapi.to_df(result)
    df['code']=code
    df['market']=nMarket
    return df


#"查询历史分时行情
def get_history_minute_time_data(nMarket = 0,code='000776',date=20190829):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    #nMarket = 0    # 0 - 深圳  1 - 上海
    result= tdxapi.get_history_minute_time_data(nMarket, code,date)
    df=tdxapi.to_df(result)
    df['code']=code
    df['market']=nMarket
    return df

#查询分笔数据
def get_transaction_data(nMarket = 0,code='000776',\
                    nStart=0, nCount=5000):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    nMarket=get_market(code)
    result= tdxapi.get_transaction_data(nMarket, code,nStart, nCount)
    df=tdxapi.to_df(result)
    df['code']=code
    df['market']=nMarket
    return df    
    
#查询历史分时成交
def get_history_transaction_data(nMarket = 0,code='000776',\
                    nStart=0, nCount=5000,date=20170209):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    nMarket=get_market(code)
    result= tdxapi.get_history_transaction_data(nMarket, code,nStart,\
                                                nCount,date)
    df=tdxapi.to_df(result)
    df['code']=code
    df['market']=nMarket    
    return df   

#查询公司信息目录
def get_company_info_category(nMarket = 0,code='000776'):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    #nMarket = 0    # 0 - 深圳  1 - 上海
    result= tdxapi.get_company_info_category(nMarket, code)
    df=tdxapi.to_df(result)
    df['code']=code
    df['market']=nMarket    
    return df

#查询公司信息目录
def get_F10(code='000776',item='股东研究'):
    global tdxapi,scode
    scode=code
    #nMarket = 0    # 0 - 深圳  1 - 上海
    nMarket=get_market(code)
    result= tdxapi.get_company_info_category(nMarket, code)
    df=tdxapi.to_df(result)
    df2=df[df.name==item]
    f=df2.iat[0,1]
    ls=df2.iat[0,2]
    le=df2.iat[0,3]
    result= tdxapi.get_company_info_content(nMarket,code,\
                                            f,ls,le)
    return result

#读取公司信息-最新提示
def get_company_info_content(nMarket = 0,code='000776',filename='000776.txt',
                             start=0, length=13477):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    nMarket=get_market(code)
    result= tdxapi.get_company_info_content(nMarket,code,\
                                            filename,start,length)
    return result


#读取财务信息
def get_finance_info(nMarket = 0,code='000776'):
    global tdxapi,scode,smarket
    scode=code
    smarket=nMarket
    nMarket=get_market(code)
    result= tdxapi.get_finance_info(nMarket, code)
    df=tdxapi.to_df(result)
    df['code']=code
    df['market']=nMarket    
    return df    


#日线级别k线获取函数
def get_k_data2(code='600030', start='2005-07-01', end='2019-02-27'):
    global tdxapi,scode
    scode=code
    df= tdxapi.get_k_data(code,start,end)
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='') 
    df.rename(columns={'vol':'volume'}, inplace = True)
    df['code']=code
    return df


#获取多个证券的盘口五档报价数据 
#stocks = api.get_security_quotes([(0, "000002"), (1, "600300")])
#stocks = api.get_security_quotes([(0, "000002")])
def get_security_quotes(code='000776'):
    global tdxapi,scode,smarket
    scode=code
    nMarket = get_market(code)
    smarket=nMarket    
    result= tdxapi.get_security_quotes(nMarket, code)
    return result    

def get_security_quotes2(market=0,code='000776'):
    global tdxapi,scode,smarket
    scode=code
    smarket=market
    result= tdxapi.get_security_quotes(market, code)
    return result    

def get_hq(codes=[ "000001","600000"]):
    global tdxapi
    mk=get_market(codes[0])
    result= tdxapi.get_security_quotes(mk, codes[0])
    df2=tdxapi.to_df(result)
    for  i in range(1,len(codes)):
        mk=get_market(codes[i])
        result= tdxapi.get_security_quotes(mk,codes[i])
        df=tdxapi.to_df(result)
        df2=df2.append( df,ignore_index=True)    
    df2.to_csv('./data/hq.csv' , encoding= 'gbk')
    return df2

def get_hq2(codes=[[0,"000001"],[1,"600000"]]):
    global tdxapi
    result= tdxapi.get_security_quotes(codes)
    df2=tdxapi.to_df(result)
    return df2

#获取全部深圳行情
def get_szhq():
    global tdxapi
    df1=getSZ()
    codes=list(df1.code)
    result= tdxapi.get_security_quotes(0, codes[0])
    df2=tdxapi.to_df(result)
    cs=[]
    for  i in range(1,len(codes)):
        cs.append((0,codes[i]))
        if i%100==0:
            result= tdxapi.get_security_quotes(cs)
            df=tdxapi.to_df(result)
            df2=df2.append( df,ignore_index=True)      
            cs=[]
    result= tdxapi.get_security_quotes(cs)
    df=tdxapi.to_df(result)
    df2=df2.append( df,ignore_index=True)              
    df2.to_csv('./data/shhq.csv' , encoding= 'gbk')
    return df2

#获取全部上海行情
def get_shhq():
    global tdxapi
    df1=getSH()
    codes=list(df1.code)
    result= tdxapi.get_security_quotes(1, codes[0])
    df2=tdxapi.to_df(result)
    cs=[]
    for  i in range(1,len(codes)):
        cs.append((1,codes[i]))
        if i%100==0:
            result= tdxapi.get_security_quotes(cs)
            df=tdxapi.to_df(result)
            df2=df2.append( df,ignore_index=True)      
            cs=[]
    result= tdxapi.get_security_quotes(cs)
    df=tdxapi.to_df(result)
    df2=df2.append( df,ignore_index=True)              
    df2.to_csv('./data/shhq.csv' , encoding= 'gbk')
    return df2

#获取全部深圳财务数据
def get_szcw():
    global tdxapi
    df1=getSZ()
    codes=list(df1.code)
    result= tdxapi.get_finance_info(0, '000001')
    df2=tdxapi.to_df(result)
    for  code in codes:
        result= tdxapi.get_finance_info(0,code)
        df=tdxapi.to_df(result)
        df2=df2.append( df,ignore_index=True)    
    df2.to_csv('./data/szcw.csv' , encoding= 'gbk')
    return df2

#获取全部上海财务数据
def get_shcw():
    global tdxapi
    df1=getSH()
    codes=list(df1.code)
    result= tdxapi.get_finance_info(1, '600000')
    df2=tdxapi.to_df(result)
    for  code in codes:
        result= tdxapi.get_finance_info(1,code)
        df=tdxapi.to_df(result)
        df2=df2.append( df,ignore_index=True)   
    df2.to_csv('./data/shcw.csv' , encoding= 'gbk')
    return df2

#'深圳股票代码表'
def szcode():
    #'深圳股票代码'
    sz=getSZ()
    sz['type']=''
    sz['kind']=''
    sz['market']=0
    sz['type2']=10
    for i in range(len(sz)):
        #print(i,sh['code'][i])
        x=int(sz['code'][i])
        if x<2000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='A股股票'
            sz.loc[i,'type2']=1
        elif x>=2000 and x<31000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='中小板'
            sz.loc[i,'type2']=2
        elif x>=31000 and x<80000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='权证'
            sz.loc[i,'type2']=8
        elif x>=80000 and x<100000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='配股'
            sz.loc[i,'type2']=1
        elif x>=100000 and x<150000:
            sz.loc[i,'type']='证券'    
            sz.loc[i,'kind']='债券'
            sz.loc[i,'type2']=6
        elif x>=150000 and x<200000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='基金'   
            sz.loc[i,'type2']=7
        elif x>=200000 and x<300000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='B股股票'
            sz.loc[i,'type2']=5
        elif x>=300000 and x<380000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='创业板'
            sz.loc[i,'type2']=3
        elif x>=390000 and x<400000:
            sz.loc[i,'type']='指数板块'
            sz.loc[i,'kind']='指数'         
            sz.loc[i,'type2']=0
        elif x>=400000 and x<500000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='三板'  
            sz.loc[i,'type2']=1            
        elif x>=500000 and x<600000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='基金'    
            sz.loc[i,'type2']=7
        elif x>=600000 and x<800000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='A股股票'  
            sz.loc[i,'type2']=1
        elif x>=800000 and x<900000:
            sz.loc[i,'type']='指数板块'
            sz.loc[i,'kind']='板块'       
            sz.loc[i,'type2']=0
        elif x>=900000 and x<999000:
            sz.loc[i,'type']='证券'
            sz.loc[i,'kind']='B股股票'  
            sz.loc[i,'type2']=5
        elif x>=999000 :
            sz.loc[i,'type']='指数板块'  
            sz.loc[i,'kind']='指数'  
            sz.loc[i,'type2']=0
    sz.to_csv('./data/sz.csv' , encoding= 'gbk')    
    return sz

#上海股票代码表
def shcode():
    #上海股票代码
    sh=getSH()
    sh['type']=''
    sh['kind']=''
    sh['market']=1
    sh['type2']=10
    for i in range(len(sh)):
        #print(i,sh['code'][i])
        x=int(sh['code'][i])
        if x<1000:
            sh.loc[i,'type']='指数板块'
            sh.loc[i,'kind']='指数'
            sh.loc[i,'type2']=0
        elif x>=1000 and x<30000:
            sh.loc[i,'type']='证券'
            sh.loc[i,'kind']='债券'
            sh.loc[i,'type2']=6
        elif x>=30000 and x<200000:
            sh.loc[i,'type']='证券'  
            sh.loc[i,'kind']='债券'  
            sh.loc[i,'type2']=6
        elif x>=200000 and x<500000:
            sh.loc[i,'type']='证券'              
            sh.loc[i,'kind']='债券'  
            sh.loc[i,'type2']=6
        elif x>=500000 and x<600000:
            sh.loc[i,'type']='证券'       
            sh.loc[i,'kind']='基金'
            sh.loc[i,'type2']=7
        elif x>=600000 and x<700000:
            sh.loc[i,'type']='证券'  
            sh.loc[i,'kind']='A股股票'  
            sh.loc[i,'type2']=1
        elif x>=700000 and x<750000:
            sh.loc[i,'type']='证券'  
            sh.loc[i,'kind']='新股申购'  
            sh.loc[i,'type2']=1
        elif x>=750000 and x<800000:
            sh.loc[i,'type']='其他'  
            sh.loc[i,'kind']='其他'  
            sh.loc[i,'type2']=9
        elif x>=800000 and x<900000:
            sh.loc[i,'type']='指数板块'              
            sh.loc[i,'kind']='板块'
            sh.loc[i,'type2']=0
        elif x>=900000 and x<999000:
            sh.loc[i,'type']='证券'  
            sh.loc[i,'kind']='B股股票'  
            sh.loc[i,'type2']=5
        elif x>=999000 :
            sh.loc[i,'type']='指数板块'  
            sh.loc[i,'kind']='指数'  
            sh.loc[i,'type2']=0
        #print(i,sh['code'][i], sh['type'][i])
    sh.to_csv('./data/sh.csv' , encoding= 'gbk')
    return sh


#获取深圳股票代码表
def get_szcode2(t=''):
    base=pd.read_csv('../../../Downloads/xb2e/data/sz.csv', encoding='gbk')
    base= base.drop('Unnamed: 0', axis=1)
    if t!='':
        base=base[base['type']==t]
        base=base.reset_index(drop=True)
    base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]
    return base

#获取上海股票代码表
def get_shcode2(t=''):
    base=pd.read_csv('../../../Downloads/xb2e/data/sh.csv', encoding='gbk')
    base= base.drop('Unnamed: 0', axis=1)
    if t!='':
        base=base[base['type']==t]    
        base=base.reset_index(drop=True)
    base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]
    return base


# 板块相关参数
BLOCK_DEFAULT = "block.dat"
BLOCK_SZ = "block_zs.dat"
BLOCK_FG = "block_fg.dat"
BLOCK_GN = "block_gn.dat"

#获取板块信息
def get_block(bk=BLOCK_DEFAULT):
    global tdxapi
    result= tdxapi.get_and_parse_block_info(bk)
    df=tdxapi.to_df(result)
    df.to_csv('./data/'+bk+'.csv' , encoding= 'gbk')
    return df

#获取本地板块信息
def get_block2(bk=BLOCK_DEFAULT):
    global tdxapi
    base=pd.read_csv('./data/'+bk+'.csv', encoding= 'gbk')
    base= base.drop('Unnamed: 0', axis=1)
    base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]    
    return base

def getblock(bk=''):
    df=get_block("block.dat")
    bk2=list(df['blockname'])
    bk3=set(bk2)
    bk2=list(bk3)
    if bk in bk2:
        df=df[df.blockname==bk]
        df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
        return df
    df=get_block("block_zs.dat")
    bk2=list(df['blockname'])
    bk3=set(bk2)
    bk2=list(bk3)
    if bk in bk2:
        df=df[df.blockname==bk]
        df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
        return df
    df=get_block("block_fg.dat")
    bk2=list(df['blockname'])
    bk3=set(bk2)
    bk2=list(bk3)
    if bk in bk2:
        df=df[df.blockname==bk]
        df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
        return df
    df=get_block("block_gn.dat")
    bk2=list(df['blockname'])
    bk3=set(bk2)
    bk2=list(bk3)
    df=df[df.blockname==bk]
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
    return df


#返回板块中的股票
def getblock2(bk=''):
    df=getblock(bk)
    if len(df) == 0:
        return []
    else:
        bks2=df['code']
        bks=list(bks2)
        return bks

#返回股票所属板块
def getblock3(code=''):
    df=get_block("block.dat")
    df2=get_block("block_zs.dat")
    df=df.append(df2)
    df2=get_block("block_fg.dat")
    df=df.append(df2)
    df2=get_block("block_gn.dat")
    df=df.append(df2)
    df=df[df.code==code]
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
    bk2=list(df['blockname'])
    bk3=set(bk2)
    bk2=list(bk3)
    return bk2


#返回通达信股票代码格式
def tdxcode(code):
    market=get_market(code)
    return (market,code)

#返回通达信板块代码格式
def tdxcodes(codes):
    bk=[]
    for code in codes:
        market=get_market(code)
        bk.append((market,code))
    return bk

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



def data_fq(fqtype='01'):
    '使用数据库数据进行复权'
    bfq_data=get_all_data(9,1, '600030')
    xdxr_data=get_xdxr_info(1, '600030')
    
    info = xdxr_data.query('category==1')
    bfq_data = bfq_data.assign(if_trade=1)

    if len(info) > 0:
        data = pd.concat([bfq_data, info.loc[bfq_data.index[0]:bfq_data.index[-1], ['category']]], axis=1)

        data['if_trade'].fillna(value=0, inplace=True)
        data = data.fillna(method='ffill')

        data = pd.concat([data, info.loc[bfq_data.index[0]:bfq_data.index[-1], ['fenhong', 'peigu', 'peigujia',
                                                                                'songzhuangu']]], axis=1)
    else:
        data = pd.concat([bfq_data, info.loc[:, ['category', 'fenhong', 'peigu', 'peigujia',
                                                 'songzhuangu']]], axis=1)
    data = data.fillna(0)
    data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu']
                        * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])

    if fqtype in ['01', 'qfq']:
        data['adj'] = (data['preclose'].shift(-1) / data['close']).fillna(1)[::-1].cumprod()
    else:
        data['adj'] = (data['close'] / data['preclose'].shift(-1)).cumprod().shift(1).fillna(1)

    for col in ['open', 'high', 'low', 'close', 'preclose']:
        data[col] = data[col] * data['adj']
    data['volume'] = data['volume'] / \
        data['adj'] if 'volume' in data.columns else data['vol']/data['adj']
    try:
        data['high_limit'] = data['high_limit'] * data['adj']
        data['low_limit'] = data['high_limit'] * data['adj']
    except:
        pass
    return data.query('if_trade==1 and open != 0').drop(['fenhong', 'peigu', 'peigujia', 'songzhuangu',
                                               'if_trade', 'category'], axis=1, errors='ignore')


def tdx_ping100():
    #
    data_future = [tdx_ping_future(x['ip'], x['port'], 'future') for x in future_ip_list]
    best_future_ip = future_ip_list[data_future.index(min(data_future))]
    print('\nbest_future_ip',best_future_ip)
    #
    print('')
    data_stock = [tdx_ping_stk(x['ip'], x['port'], 'stock') for x in stock_ip_list]
    best_stock_ip = stock_ip_list[data_stock.index(min(data_stock))]
    print('\nbest_stock_ip',best_stock_ip)
    #
    x=best_stock_ip
    tim=tdx_ping_stk(x['ip'], x['port'], 'stock') 
    x=best_future_ip
    tim2=tdx_ping_future(x['ip'], x['port'], 'future') 
    #
    print('')
    print('股票 stock best_ip',best_stock_ip,tim)
    print('期货 future best_ip',best_future_ip,tim2)
    #
    #best_stock_ip {'ip': '119.147.164.60', 'port': 7709} 0:00:00.258858
    #best_future_ip {'ip': '119.97.185.5', 'port': 7727, 'name': '扩展市场武汉主站1'} 0:00:00.055968
    #
    return best_stock_ip
    
#测试
if __name__ == '__main__':
    tdxapi=TdxInit(ip='183.60.224.178',port=7709)
    df=get_security_bars()
    print(df)
    print(df)
    df2=getblock2(bk='上证50')
    print(df2)
    df3=get_security_bars(nCategory=4,nMarket = 1,code='000016',nStart=0, nCount=240)
    print(df3)
    #pys=hhz.loadhzk2('data/pinyin.csv')
#    getSZ()
#    getSH()
#    tdxapi=TdxInit()
    #cd=get_szcode()
    #cd2=get_shcode()
    #print(cd)
#    cd=cd.append(cd2)
#    cd=cd.reset_index(level=None, drop=True ,col_level=0, col_fill='')
#    cd.to_csv('./data/codes.csv' , encoding= 'gbk')
#    cds={}
#    for i in range(len(cd)):
#        cds[(cd.market[i],cd.code[i])]=cd.name[i]
#    
#    print(cds)
#    df= get_hq2([[0,'000001'],[1,'600030']])
#    print(df)
#    df['zd']=df['price']-df['last_close']  #涨跌
#    df['zdf1']=df['zd']*100/df['last_close']  #涨跌幅
#    df=df.round(2)  #改变符点数小数点后2位
#    df['zdf']=df['zdf1'].astype(str)+'%'
#    df['code2']=['0'*(6-len(x)) + x for x in df.code.astype(str)]
#    df['name']=''
#    for i in range(len(df)):
#        df.loc[i,'name']=cds[(df.loc[i,'market'],df.loc[i,'code2'])]
#
#    df.to_csv('./data/hq.csv' , encoding= 'gbk')
#    aa=get_block(BLOCK_GN)
#    #print(aa)
#    bb=list(aa['blockname'])
#    bb1=set(bb)
#    bb2=list(bb1)
#    print(bb2)
#    bfq_data=get_all_data(9,1, '600030')
#    bfq_data.to_csv('./data/cq1.csv' , encoding= 'gbk')
#    print(bfq_data)
#    xdxr_data=get_xdxr_info(1, '600030')
#    print(xdxr_data)
    result= tdxapi.get_finance_info(0, '000001')
    print(result['gudingzichan'])
#    aa=data_fq()
#    print(aa)
#    aa.to_csv('./data/cq2.csv' , encoding= 'gbk')
#    print(aa.columns)
#    print(get_all_data())
    
#    df=df=get_szhq()
#    print(df.columns)

#    sh=shcode()
#    sz=szcode()
#    print(sh)
#    print(sz)
#    
#    print('深圳股票代码\n')
#    df=get_k_data()
#    print(df)
#    #print(df.columns)
#    sz=getSZ()
#    print(sz)
    
#    sz=get_shcode('A股股票')
#    
#    #sh=sh[sh.type=='A股股票']
#    print(sz)

    #df=get_transaction_data()
#    df=get_xdxr_info(1,'600030')
#    df=get_company_info_category()
#    df=get_index_bars()
#    print(df)  
#    df=TdxExHq_API.get_instrument_quote(0)
#    print(df)
#    df2=get_xdxr_info()
#    print(df2)
#    print('查询公司信息目录')
#    df=get_company_info_category()
#    print(df.name)
#    t=get_F10('600030','公司概况')
#    print(t)
#    txt=get_company_info_content(nMarket = 0,code='000776',filename='000776.txt',\
#                             start=60463, length=16935)
#    print(txt)
#    ex_api=exhq()
#    a=ex_api.get_history_minute_time_data(1,'600030',date='2019-12-16')
#    b=ex_api.get_markets()
#    c=ex_api.to_df(b)
#    print(c)
#    aa=ex_api.get_instrument_info(0, 100)
#    bb=ex_api.to_df(aa)
#    print(bb)
