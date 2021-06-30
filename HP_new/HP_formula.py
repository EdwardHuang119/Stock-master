# -*- coding: utf-8 -*-
"""
#仿通达新大智慧公式基础库  Ver1.00
#版本：Ver1.01
#设计人：独狼荷蒲
#电话:18578755056
#QQ：2775205
#百度：荷蒲指标
#开始设计日期: 2018-07-08
#公众号:独狼股票分析
#使用者请同意最后<版权声明>
#最后修改日期:2021年04月22日
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
import os
import math
import datetime as dt
import pandas as pd  
import numpy  as np

class HSeries(pd.Series):
    def __init__(self,**kw):
       super.__init__(**kw)


#列表扩展
def Listexpand(List,n):
    Lista=[]
    for x in List:
        for i in range(n):
            Lista.append(x)
    return Lista

#列表扩展
def Seriesexpand(Series,n):
    Lista=[]
    for x in list(Series):
        for i in range(n):
            Lista.append(x)
    return pd.Series(Lista)
     


def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]


# DATE=Date(date)
def Date(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        d=(100+int(s[2:4]))*10000+int(s[5:7])*100+int(s[8:10])
        ret.append(d)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

# YEAR=Year(date)
def Year(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        d=int(s[0:4])
        ret.append(d)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

# MONTH =Month(date)
def Month(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        d=int(s[5:7])
        ret.append(d)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

def Week(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        t1=dt.datetime.strptime(s[0:10],"%Y-%m-%d")
        w2=dt.date.weekday(t1)
        ret.append(w2)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)    

    
# DAY=Day(date)
def Day(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        d=int(s[8:10])
        ret.append(d)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

# TIME=Time(date)    
def Time(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        t=int(s[-5:-3])*100+int(s[-2:])
        ret.append(t)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

# HOUR =  Hour(date):
def Hour(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        t=int(s[-5:-3])*100+int(s[-2:])
        ret.append(t)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

# MINUTE=Minute(date)
def MINUTE(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        t=int(s[-5:-3])*100+int(s[-2:])
        ret.append(t)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

def FROMOPEN():
    d1=time.strftime("%Y-%m-%d",time.localtime(time.time()))+' 09:30:01.001'
    d3=dt.datetime.strptime(todayopen,"%Y-%m-%d %H:%M:%S.%f")
    d2 = dt.datetime.now()
    return int((d2-d3).seconds/60)

##########################
#杂函数
#判断是否是英文句子
def isenglish(ss):
    result=True
    for c in ss.lower():
        if c in "abcdefghijklmnopqrstuvwxyz,.' !?":
            continue 
        result=False
        break
    return result

def CODE(code):
    code=code.strip()
    if isenglish(code)==True or len(code)==0:
        ret_=0
    else:
        ret_=int(code)
    return ret_


def get_names():
    names={}
    codes=[]
    names2=[]
    if (os.path.isfile('./names.csv'))==True:
        base=pd.read_csv('./names.csv' , encoding= 'gbk')
        codes2=list(base.code)
        names2=list(base.name)
        i=0
        for code in codes2:
            codes.append(code[1:])
            names.update({code[1:]:names2[i]})
            i+=1
    return names,codes

def STKNAME(code):
    names,codes=get_names()
    if code in codes:
        ret_=names[code]
    else:
        ret_=''
    return ret_
    
# 算农历日期
g_lunar_month_day = [
	0x00752, 0x00ea5, 0x0ab2a, 0x0064b, 0x00a9b, 0x09aa6, 0x0056a, 0x00b59, 0x04baa, 0x00752, # 1901 ~ 1910 
	0x0cda5, 0x00b25, 0x00a4b, 0x0ba4b, 0x002ad, 0x0056b, 0x045b5, 0x00da9, 0x0fe92, 0x00e92, # 1911 ~ 1920 
	0x00d25, 0x0ad2d, 0x00a56, 0x002b6, 0x09ad5, 0x006d4, 0x00ea9, 0x04f4a, 0x00e92, 0x0c6a6, # 1921 ~ 1930 
	0x0052b, 0x00a57, 0x0b956, 0x00b5a, 0x006d4, 0x07761, 0x00749, 0x0fb13, 0x00a93, 0x0052b, # 1931 ~ 1940 
	0x0d51b, 0x00aad, 0x0056a, 0x09da5, 0x00ba4, 0x00b49, 0x04d4b, 0x00a95, 0x0eaad, 0x00536, # 1941 ~ 1950 
	0x00aad, 0x0baca, 0x005b2, 0x00da5, 0x07ea2, 0x00d4a, 0x10595, 0x00a97, 0x00556, 0x0c575, # 1951 ~ 1960 
	0x00ad5, 0x006d2, 0x08755, 0x00ea5, 0x0064a, 0x0664f, 0x00a9b, 0x0eada, 0x0056a, 0x00b69, # 1961 ~ 1970 
	0x0abb2, 0x00b52, 0x00b25, 0x08b2b, 0x00a4b, 0x10aab, 0x002ad, 0x0056d, 0x0d5a9, 0x00da9, # 1971 ~ 1980 
	0x00d92, 0x08e95, 0x00d25, 0x14e4d, 0x00a56, 0x002b6, 0x0c2f5, 0x006d5, 0x00ea9, 0x0af52, # 1981 ~ 1990 
	0x00e92, 0x00d26, 0x0652e, 0x00a57, 0x10ad6, 0x0035a, 0x006d5, 0x0ab69, 0x00749, 0x00693, # 1991 ~ 2000 
	0x08a9b, 0x0052b, 0x00a5b, 0x04aae, 0x0056a, 0x0edd5, 0x00ba4, 0x00b49, 0x0ad53, 0x00a95, # 2001 ~ 2010 
	0x0052d, 0x0855d, 0x00ab5, 0x12baa, 0x005d2, 0x00da5, 0x0de8a, 0x00d4a, 0x00c95, 0x08a9e, # 2011 ~ 2020 
	0x00556, 0x00ab5, 0x04ada, 0x006d2, 0x0c765, 0x00725, 0x0064b, 0x0a657, 0x00cab, 0x0055a, # 2021 ~ 2030 
	0x0656e, 0x00b69, 0x16f52, 0x00b52, 0x00b25, 0x0dd0b, 0x00a4b, 0x004ab, 0x0a2bb, 0x005ad, # 2031 ~ 2040 
	0x00b6a, 0x04daa, 0x00d92, 0x0eea5, 0x00d25, 0x00a55, 0x0ba4d, 0x004b6, 0x005b5, 0x076d2, # 2041 ~ 2050 
	0x00ec9, 0x10f92, 0x00e92, 0x00d26, 0x0d516, 0x00a57, 0x00556, 0x09365, 0x00755, 0x00749, # 2051 ~ 2060 
	0x0674b, 0x00693, 0x0eaab, 0x0052b, 0x00a5b, 0x0aaba, 0x0056a, 0x00b65, 0x08baa, 0x00b4a, # 2061 ~ 2070 
	0x10d95, 0x00a95, 0x0052d, 0x0c56d, 0x00ab5, 0x005aa, 0x085d5, 0x00da5, 0x00d4a, 0x06e4d, # 2071 ~ 2080 
	0x00c96, 0x0ecce, 0x00556, 0x00ab5, 0x0bad2, 0x006d2, 0x00ea5, 0x0872a, 0x0068b, 0x10697, # 2081 ~ 2090 
	0x004ab, 0x0055b, 0x0d556, 0x00b6a, 0x00752, 0x08b95, 0x00b45, 0x00a8b, 0x04a4f, ]
 
 
#农历数据 每个元素的存储格式如下： 
#    12~7         6~5    4~0  
#  离元旦多少天  春节月  春节日  
#####################################################################################
g_lunar_year_day = [
	0x18d3, 0x1348, 0x0e3d, 0x1750, 0x1144, 0x0c39, 0x15cd, 0x1042, 0x0ab6, 0x144a, # 1901 ~ 1910 
	0x0ebe, 0x1852, 0x1246, 0x0cba, 0x164e, 0x10c3, 0x0b37, 0x14cb, 0x0fc1, 0x1954, # 1911 ~ 1920 
	0x1348, 0x0dbc, 0x1750, 0x11c5, 0x0bb8, 0x15cd, 0x1042, 0x0b37, 0x144a, 0x0ebe, # 1921 ~ 1930 
	0x17d1, 0x1246, 0x0cba, 0x164e, 0x1144, 0x0bb8, 0x14cb, 0x0f3f, 0x18d3, 0x1348, # 1931 ~ 1940 
	0x0d3b, 0x16cf, 0x11c5, 0x0c39, 0x15cd, 0x1042, 0x0ab6, 0x144a, 0x0e3d, 0x17d1, # 1941 ~ 1950 
	0x1246, 0x0d3b, 0x164e, 0x10c3, 0x0bb8, 0x154c, 0x0f3f, 0x1852, 0x1348, 0x0dbc, # 1951 ~ 1960 
	0x16cf, 0x11c5, 0x0c39, 0x15cd, 0x1042, 0x0a35, 0x13c9, 0x0ebe, 0x17d1, 0x1246, # 1961 ~ 1970 
	0x0d3b, 0x16cf, 0x10c3, 0x0b37, 0x14cb, 0x0f3f, 0x1852, 0x12c7, 0x0dbc, 0x1750, # 1971 ~ 1980 
	0x11c5, 0x0c39, 0x15cd, 0x1042, 0x1954, 0x13c9, 0x0e3d, 0x17d1, 0x1246, 0x0d3b, # 1981 ~ 1990 
	0x16cf, 0x1144, 0x0b37, 0x144a, 0x0f3f, 0x18d3, 0x12c7, 0x0dbc, 0x1750, 0x11c5, # 1991 ~ 2000 
	0x0bb8, 0x154c, 0x0fc1, 0x0ab6, 0x13c9, 0x0e3d, 0x1852, 0x12c7, 0x0cba, 0x164e, # 2001 ~ 2010 
	0x10c3, 0x0b37, 0x144a, 0x0f3f, 0x18d3, 0x1348, 0x0dbc, 0x1750, 0x11c5, 0x0c39, # 2011 ~ 2020 
	0x154c, 0x0fc1, 0x0ab6, 0x144a, 0x0e3d, 0x17d1, 0x1246, 0x0cba, 0x15cd, 0x10c3, # 2021 ~ 2030 
	0x0b37, 0x14cb, 0x0f3f, 0x18d3, 0x1348, 0x0dbc, 0x16cf, 0x1144, 0x0bb8, 0x154c, # 2031 ~ 2040 
	0x0fc1, 0x0ab6, 0x144a, 0x0ebe, 0x17d1, 0x1246, 0x0cba, 0x164e, 0x1042, 0x0b37, # 2041 ~ 2050 
	0x14cb, 0x0fc1, 0x18d3, 0x1348, 0x0dbc, 0x16cf, 0x1144, 0x0a38, 0x154c, 0x1042, # 2051 ~ 2060 
	0x0a35, 0x13c9, 0x0e3d, 0x17d1, 0x11c5, 0x0cba, 0x164e, 0x10c3, 0x0b37, 0x14cb, # 2061 ~ 2070 
	0x0f3f, 0x18d3, 0x12c7, 0x0d3b, 0x16cf, 0x11c5, 0x0bb8, 0x154c, 0x1042, 0x0ab6, # 2071 ~ 2080 
	0x13c9, 0x0e3d, 0x17d1, 0x1246, 0x0cba, 0x164e, 0x10c3, 0x0bb8, 0x144a, 0x0ebe, # 2081 ~ 2090 
	0x1852, 0x12c7, 0x0d3b, 0x16cf, 0x11c5, 0x0c39, 0x154c, 0x0fc1, 0x0a35, 0x13c9, # 2091 ~ 2100 
	]
 
START_YEAR = 1901
month_DAY_BIT = 12
month_NUM_BIT = 13 
#　todo：正月初一 == 春节   腊月二十九/三十 == 除夕
yuefeng = ["正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "冬月", "腊月"]
riqi = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "廿十",
    "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
 
xingqi = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
xingqi2 = ["星期日","星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
tiangan   = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
dizhi     = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
shengxiao = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
 
# 节气名称组
jieqi = [
    "小寒", "大寒",  # 1月        
    "立春", "雨水",  # 2月
    "惊蛰", "春分",  # 3月
    "清明", "谷雨",  # 4月
    "立夏", "小满",  # 5月
    "芒种", "夏至",  # 6月
    "小暑", "大暑",  # 7月
    "立秋", "处暑",  # 8月
    "白露", "秋分",  # 9月
    "寒露", "霜降",  # 10月
    "立冬", "小雪",  # 11月
    "大雪", "冬至"]  # 12月

# 节气日期
jieqi2 = [
    5, 20,  # 1月        
    3,18,  # 2月
    5, 20,  # 3月
    4, 20,  # 4月
    5, 21,  # 5月
    5, 21,  # 6月
    7, 22,  # 7月
    7, 23,  # 8月
    7, 23,  # 9月
    8, 23,  # 10月
    7, 22,  # 11月
    7, 22]  # 12月


 ## 特殊年份特殊节气进行纠正
def rectify_year(year,m,day):
    day2=day
    cday=''
    m=m-1
    jq1=2*m
    jq2=2*m+1
    
    day=jieqi[jq1]
 
    if day2==jieqi2[jq1]:
        cday=jieqi[jq1]
    if day2==jieqi2[jq2]:
        cday=jieqi[jq2]
    return cday
 
def change_year(num):
    dx = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
    tmp_str = ""
    for i in str(num):
        tmp_str += dx[int(i)]
    return tmp_str
 
def week_str(tm):
    return xingqi[tm.weekday()]
 
def lunar_day(day):
    return riqi[(day - 1) % 30]
 
def lunar_day1(month, day):
    if day == 1:
        return lunar_month(month)
    else:
        return riqi[day - 1]
 
def lunar_month(month):
    leap = (month>>4)&0xf
    m = month&0xf
    month = yuefeng[(m - 1) % 12]
    if leap == m:
        month = "闰" + month
    return month
 
def lunar_year(year):
    return tiangan[(year - 4) % 10] + dizhi[(year - 4) % 12] + '[' + shengxiao[(year - 4) % 12] + ']'
 
# 返回：
# a b c
# 闰几月，该闰月多少天 传入月份多少天
def lunar_month_days(lunar_year, lunar_month):
    if (lunar_year < START_YEAR):
        return 30
 
    leap_month, leap_day, month_day = 0, 0, 0 # 闰几月，该月多少天 传入月份多少天
 
    tmp = g_lunar_month_day[lunar_year - START_YEAR]
 
    if tmp & (1<<(lunar_month-1)):
        month_day = 30
    else:
        month_day = 29
 
    # 闰月
    leap_month = (tmp >> month_NUM_BIT) & 0xf
    if leap_month:
        if (tmp & (1<<month_DAY_BIT)):
            leap_day = 30
        else:
            leap_day = 29
 
    return (leap_month, leap_day, month_day)
# 返回的月份中，高4bit为闰月月份，低4bit为其它正常月份
def get_ludar_date(tm):
    year, month, day = tm.year, 1, 1
    code_data = g_lunar_year_day[year - START_YEAR]
    days_tmp = (code_data >> 7) & 0x3f
    chunjie_d = (code_data >> 0) & 0x1f
    chunjie_m = (code_data >> 5) & 0x3
    span_days = (tm - dt.datetime(year, chunjie_m, chunjie_d)).days
    #print("span_day: ", days_tmp, span_days, chunjie_m, chunjie_d)
 
    # 日期在该年农历之后
    if (span_days >= 0):
        (leap_month, foo, tmp) = lunar_month_days(year, month)
        while span_days >= tmp:
            span_days -= tmp
            if (month == leap_month):
                (leap_month, tmp, foo) = lunar_month_days(year, month) # 注：tmp变为闰月日数
                if (span_days < tmp): # 指定日期在闰月中
                    month = (leap_month<<4) | month
                    break
                span_days -= tmp
            month += 1 # 此处累加得到当前是第几个月
            (leap_month, foo, tmp) = lunar_month_days(year, month)
        day += span_days
        return year, month, day
    # 倒算日历
    else:
        month = 12
        year -= 1
        (leap_month, foo, tmp) = lunar_month_days(year, month)
        while abs(span_days) >= tmp:
            span_days += tmp
            month -= 1
            if (month == leap_month):
                (leap_month, tmp, foo) = lunar_month_days(year, month)
                if (abs(span_days) < tmp): # 指定日期在闰月中
                    month = (leap_month<<4) | month
                    break
                span_days += tmp
            (leap_month, foo, tmp) = lunar_month_days(year, month)
        day += (tmp + span_days) # 从月份总数中倒扣 得到天数
        return year, month, day

def CWEEK(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        t1=dt.datetime.strptime(s[0:10],"%Y-%m-%d")
        w2=dt.date.weekday(t1)
        ret.append(xingqi2(w2))
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)    


def LYEAR(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        y=int(s[0:4])
        m=int(s[5:7])
        d=int(s[8:10])
        tmp = dt.datetime(y, m, d)
        y2,m2,d2=get_ludar_date(tmp)
        ret.append(y2)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

def LMONTH(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        y=int(s[0:4])
        m=int(s[5:7])
        d=int(s[8:10])
        tmp = dt.datetime(y, m, d)
        y2,m2,d2=get_ludar_date(tmp)
        ret.append(m2)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

def LDAY(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        y=int(s[0:4])
        m=int(s[5:7])
        d=int(s[8:10])
        tmp = dt.datetime(y, m, d)
        y2,m2,d2=get_ludar_date(tmp)
        ret.append(d2)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

def CYEAR(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        y=int(s[0:4])
        m=int(s[5:7])
        d=int(s[8:10])
        tmp = dt.datetime(y, m, d)
        y2,m2,d2=get_ludar_date(tmp)
        y3=lunar_year(y2)
        ret.append(y3)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

def CYEARX(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        y=int(s[0:4])
        m=int(s[5:7])
        d=int(s[8:10])
        tmp = dt.datetime(y, m, d)
        y2,m2,d2=get_ludar_date(tmp)
        y3=lunar_year(y2)
        ret.append(y3)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)


def CMONTH(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        y=int(s[0:4])
        m=int(s[5:7])
        d=int(s[8:10])
        tmp = dt.datetime(y, m, d)
        y2,m2,d2=get_ludar_date(tmp)
        m3=lunar_month(m2)
        ret.append(m3)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)

def CDAY(Series):
    length = len(Series)
    ret=[]
    i=1
    while i < length:
        s=Series.iloc[i]
        y=int(s[0:4])
        m=int(s[5:7])
        d=int(s[8:10])
        tmp = dt.datetime(y, m, d)
        y2,m2,d2=get_ludar_date(tmp)
        d3= lunar_day(d2)
        ret.append(d3)
        i+=1
    return pd.Series(ret, index=Series.tail(len(ret)).index)



"""
Series 类

这个是下面以DataFrame为输入的基础函数
return pd.Series format
"""

def REVERSE(Series):
    return -Series
    

def EMA2(Series, N):
    return pd.Series.ewm(Series, span=N, min_periods=N - 1, adjust=True).mean()

def EMA(Series, N):
    var=pd.Series.ewm(Series, span=N, min_periods=N - 1, adjust=True).mean()
    if N>0:
        var[0]=0
        #y=0
        a=2.00000000/(N+1)
        for i in range(1,N):
            y=pd.Series.ewm(Series, span=i, min_periods=i - 1, adjust=True).mean()
            y1=a*Series[i]+(1-a)*y[i-1]
            var[i]=y1
    return var


def MA(Series, N):
    return pd.Series.rolling(Series, N).mean()

def MA2(Series, N):
    var=pd.Series.rolling(Series, N).mean()
    if N>0:
        y=0
        for i in range(N):
            y=y+Series[i]
            var[i]=y/(i+1)
    return var

# SMA(X,N,M):X的N日移动平均,M为权重,如Y=(X*M+Y'*(N-M))/N
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

# WMA(X,N):X的N日加权移动平均.算法:Yn=(1*X1+2*X2+...+n*Xn)/(1+2+...+n)
def WMA(Series, N):
    ret = []
    i = 0
    length = len(Series)
    # 跳过X中前面几个 nan 值
    while i < length:
        if np.isnan(Series.iloc[i]):
            i += 1
        else:
            break
    j=1
    while j<N and i<length:
        preY = Series.iloc[i]  # Y'
        ret.append( np.NAN)
        i+=1
        j=j+1
    while i < length:
        j=0
        y=0.0
        y2=0
        while j<(N):
            y = y+Series.iloc[i-N+j]*(j+1)
            j=j+1
            y2= y2+j
            
        i=i+1
        y3= y/ float(y2)
        ret.append(y3)
    return pd.Series(ret, index=Series.tail(len(ret)).index)

def DIFF(Series, N=1):
    return pd.Series(Series).diff(N)

def HHV(Series, N=0):
    if N==0:
        return Series.cummax()
    else:
        return pd.Series(Series).rolling(N).max()

def LLV(Series, N=0):
    if N==0:
        return Series.cummin()
    else:
        return pd.Series(Series).rolling(N).min()

def LLV2(Series, N):
    if isinstance(N, int):  # N为整型
        return pd.Series(Series).rolling(N).min()
    elif isinstance(N, (list, pd.Series)):  # N为序列或列表
        df = pd.DataFrame({'Series': Series, 'N': N})
        res = []
        for idx, row in df.iterrows():
            if not np.isnan(row[1]):
                N = int(row[1])
                r = df['Series'].rolling(N).min()
                rs = r.iloc[idx]
            else:
                rs = np.nan
            res.append(rs)
        return res


def HHV2(Series, N):
    if isinstance(N, int):  # N为整型
        return pd.Series(Series).rolling(N).max()
    elif isinstance(N, (list, pd.Series)):  # N为序列或列表
        df = pd.DataFrame({'Series': Series, 'N': N})
        res = []
        for idx, row in df.iterrows():
            if not np.isnan(row[1]):
                N = int(row[1])
                r = df['Series'].rolling(N).max()
                rs = r.iloc[idx]
            else:
                rs = np.nan
            res.append(rs)
        return res

def SUMX(Series, N=0):
    if N<=0:
        N=len(Series)
    sum_=pd.Series.rolling(Series, N).sum()
    return pd.Series(sum_,name='sums')

def SUM(ser_,p):
    ser_,sum_=list(ser_),[ser_[0],]
    for i in range(1,len(ser_)):
        if i<p:sum_.append(sum(ser_[:i+1]))
        else:sum_.append(sum(ser_[i+1-p:i+1]))
    return pd.Series(sum_,name='sums')

def ABS(Series):  #绝对值 
    return abs(Series)

def MAX(A, B):
    var = IF(A > B, A, B)
    return pd.Series( var,name='maxs')

def MIN(A, B):
    var = IF(A < B, A, B)
    return var

def SQRT(A):   #平方根 
    A2=np.array(A)
    var = np.sqrt(A2)
    return (pd.Series(var, index=A.index))


def SQUARE(A):   #平方根 
    A2=np.array(A)
    var = np.square(A2)
    return (pd.Series(var, index=A.index))

def CEILING(A):   #返回沿A数值增大方向最接近的整数。
    A2=np.array(A)
    var = np.ceil(A2)
    return (pd.Series(var, index=A.index))

def FLOOR(A):   #返回沿A数值减少方向最接近的整数。
    A2=np.array(A)
    var = np.floor(A2)
    return (pd.Series(var, index=A.index))

def INTPART(A):   #返回沿A数值减少方向最接近的整数。
    A2=np.array(A)
    var = np.floor(A2)
    return (pd.Series(var, index=A.index))

def INT(A):   #返回沿A数值四舍五入
    A2=np.array(A)
    var = np.rint(A2)
    return (pd.Series(var, index=A.index))

def LN(A):   #自然对数
    A2=np.array(A)
    var = np.log(A2)
    return (pd.Series(var, index=A.index))


def LOG(A):    #10为底的对数
    A2=np.array(A)
    var = np.log10(A2)
    return (pd.Series(var, index=A.index))

def LOG2(A):   #2为底的对数
    A2=np.array(A)
    var = np.log2(A2)
    return (pd.Series(var, index=A.index))

def EXP(A):   #指数值 
    A2=np.array(A)
    var = np.exp(A2)
    return (pd.Series(var, index=A.index))

def POW(A,x):   #A的x次幂
    A2=np.array(A)
    var = A2**x
    return (pd.Series(var, index=A.index))

def POW2(x):
    if isinstance(x, int or float):  # N为整型
        return 10**x
    elif isinstance(x, (list, pd.Series)):  # N为序列或列表
        x_array = np.array(list(x))
        res = 10 ** x_array
        return pd.Series(res)

def SIGN(A):   #符号值 1（+），0，-1（-）  
    A2=np.array(A)
    var = np.sign(A2)
    return (pd.Series(var, index=A.index))


def MOD(A, B):  #元素级的模运算
    var = np.mod(np.array(A) ,np.array(B))
    return  (pd.Series(var, index=A.index))

def COS(A):   
    A2=np.array(A)
    var = np.cos(A2)
    return (pd.Series(var, index=A.index))


def SIN(A):   
    A2=np.array(A)
    var = np.sin(A2)
    return (pd.Series(var, index=A.index))



def TAN(A):   
    A2=np.array(A)
    var = np.tan(A2)
    return (pd.Series(var, index=A.index))


def ACOS(A):   
    A2=np.array(A)
    var = np.arccos(A2)
    return (pd.Series(var, index=A.index))

def ASIN(A):   
    A2=np.array(A)
    var = np.arcsin(A2)
    return (pd.Series(var, index=A.index))

def ATAN(A):   
    A2=np.array(A)
    var = np.arctan(A2)
    return (pd.Series(var, index=A.index))

def SINGLE_CROSS(A, B):
    if A.iloc[-2] < B.iloc[-2] and A.iloc[-1] > B.iloc[-1]:
        return True
    else:
        return False

def CROSS(A, B):
    A2=np.array(A)
    var = np.where(A2<B, 1, 0)
    return (pd.Series(var, index=A.index).diff()<0).apply(int)

def CROSSX(A, B):
    B2=np.array(B)
    var = np.where(A<B2, 1, 0)
    return (pd.Series(var, index=B.index).diff()<0).apply(int)


def BETWEEN(A, B, C):
    A2=np.array(A)
    var = np.where(A2>=B, 1, 0)
    var2 = np.where(A2<=C, 1, 0)
    v1=pd.Series(var, index=A.index)
    v2=pd.Series(var2, index=A.index)
    v3=v1*v2
    return v3


def COUNT(COND, N):
    if N==0:
        return pd.Series(np.where(COND,1,0),index=COND.index).cumsum()
    else:
        return pd.Series(np.where(COND,1,0),index=COND.index).rolling(N).sum()


def COUNT2(COND, N):
    var=pd.Series(np.where(COND,1,0),index=COND.index).rolling(N).sum()
    if N>0:
        y=0
        for i in range(N):
            print(COND.iloc[i])
            if  COND.iloc[i]:
                y=y+1
            var[i]=y
    return var

def IF(COND, V1, V2):
    var = np.where(COND, V1, V2)
    return pd.Series(var)

def IFF(COND, V1, V2):
    var = np.where(COND, V1, V2)
    return pd.Series(var)

def IFN(COND, V1, V2):
    var = np.where(COND, V2, V1)
    return pd.Series(var)



def REF(Series, N,sign=0):
    #sign=1表示保留数据,并延长序列
    if sign==1:
        for i in range(N):
            Series=Series.append(pd.Series([0],index=[len(Series)+1]))
    return Series.shift(N)

def REFX(Series, N):
    return Series.shift(-N)

#变参REFA()
def REFA(Series, Series2):
    if 'int' in str(type(Series2)):
        return REF(Series, Series2)
    s1,lenth1=list(Series),len(Series)
    if 'list' in str(type(Series2)):
        s2,lenth2=Series2,len(Series2)
    else:
        s2,lenth2=list(Series2),len(Series2)
    bars_=[]
    if lenth1!=lenth2:
        return Series
    for i in range(lenth1):
        if s1[i-int(s2[i])]==np.nan:
            bars_.append(np.nan)
        elif (i-int(s2[i])>=0 and (i-int(s2[i]))<lenth1):
            bars_.append(s1[i-int(s2[i])])
        else:
            bars_.append(np.nan)
    return pd.Series(bars_ )    


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
    if (np.isnan(para_).any()):
        newdf=pd.DataFrame(para_)
        newdf=newdf.fillna(axis=0,value=0.00000001)
        para_=newdf[0]
    ser_,para_,dma_=list(ser_),list(para_),[ser_[0],]
    for i in range(1,len(ser_)):
        dma_.append(para_[i]*ser_[i]+(1-para_[i])*dma_[-1])
    return pd.Series(dma_)

def LLVBARS(price,window):
    return price.rolling(window).apply(lambda x:window-np.argmin(x)-1,raw=True)

def HHVBARS(price,window):
    return price.rolling(window).apply(lambda x:window-np.argmax(x)-1,raw=True)

def BARSLAST(ser_cond):
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
    return pd.Series(bars_ )

def DRAWNULL():
    return np.nan

def BARSCOUNT(ser_cond):
    ser_cond=list(ser_cond)
    lenth=len(ser_cond)
    bars_=[]
    y=0
    sign=False
    for i in range(0,lenth):
        if math.isnan(float(ser_cond[i])) and sign==False:
            bars_.append(0)
        else:
            y=y+1
            bars_.append(y)
    return pd.Series(bars_ )

def BARSSINCE(ser_cond):
    ser_cond=list(ser_cond)
    lenth=len(ser_cond)
    bars_=[]
    y=0
    sign=False
    for i in range(0,lenth):
        if math.isnan(float(ser_cond[i])) and sign==False:
            bars_.append(0)
        else:
            if ser_cond[i]>0  and sign==False:
                sign=True
            if sign==True:
                y=y+1
            bars_.append(y)
    return pd.Series(bars_ )

def NOT(A):
    A2=np.array(A)
    var = np.where(A2>0, 0, 1)
    return (pd.Series(var, index=A.index).diff()<0).apply(int)

def FILTER(A, N):
    A2=np.array(A)
    var = np.where(A2>0, 1, 0)
    k=N
    sign=False
    for i in range(len(var)):
        if sign==True and k>0:
            var[i]=0
            k=k-1
        if k<=0:
            sign=False
        if var[i]>0:
            sign=True
            k=N
    return (pd.Series(var, index=A.index).diff()<0).apply(int)

def BACKSET(A, N):
    A2=np.array(A)
    var = np.where(A2>0, 1, 0)
    for i in range(len(var)):
        if var[i]>0:
            for j in range(min(i,N)):
                var[i-j]=0
                
    return (pd.Series(var, index=A.index).diff()<0).apply(int)

def TFILTER(A,B, N):
    A2=np.array(A)
    var = np.where(A2>0, 1, 0)
    B2=np.array(B)
    var2 = np.where(B2>0, 1, 0)    
    sign=False
    for i in range(len(var)):
        if N==1 or N==0:
            if sign==False and var[i]>0:
                var[i]=1
                sign=True
        else:
            if  var[i]>0:
                var[i]=1
                sign=True
                
        if N==2 or N==0:
            if sign==True and var2[i]>0:
                var[i]=2
                sign=False
        else:
            if  var2[i]>0:
                var[i]=2
                sign=False
    return (pd.Series(var, index=A.index).diff()<0).apply(int)

#线性回归斜率
def SLOPE(Series, N):
    #SLOPE(X,N)为X的N周期线性回归线的斜率
    xx=list(Series)
    res=np.ones(len(xx))*np.nan
    for i in range(N,len(xx)):
        slp=np.polyfit(range(N),xx[i+1-N:i+1],1)
        res[i]=slp[0]
    return pd.Series(res)

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
    #d = k.index
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
"""
之字转向。
用法:
ZIG(K,N,ABS),当价格变化量超过N%时转向,K表示0:开盘价,1:最高价,2:最低价,3:收盘价,4:低点采用最低价、高点采用最高价。若ABS为0或省略，则表示相对ZIG转向，否则为绝对ZIG转向。
例如：ZIG(3,5)表示收盘价的5%的ZIG转向;
ZIG(3,0.5,1)表示收盘价的0.5元绝对ZIG转向
"""
def ZIG(k,x=5.5):
    '''
    #之字转向
    CLOSE=mydf['close']
    zz=zig(CLOSE,x=0.055) 
    mydf = mydf.join(pd.Series(zz,name='zz'))  #增加 J到 mydf中1
    mydf.zz.plot.line()
    CLOSE.plot.line()
    '''
    #d = k.index
    k=list(k)
    x=x/100
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
    
    return pd.Series(z)
#######################################################
global x_all,y_all,x_train,x_test,y_train,y_test
x_all = []     #输入数据
y_all = []     #输出数据
x_train=None
x_test=None
y_train=None
y_test=None

def sk_init(df='',x=[],y=['label'],test_size=0.10):
    global x_all,y_all,x_train,x_test,y_train,y_test
    df=df.fillna(value=0.00)
    ## 不设置学习字段，自动获取数字型数据字段
    if len(x)==0:
        x=[]
        x2=df.columns
        for s in x2:
            s2=str(type(df[s].iloc[0]))
            if 'int' in s2:
                x.append(s)
            if 'float' in s2:
                x.append(s)

    #装配神经网络学习数据
    for i in range(len(df)-1):

        # 输入数字数据
        features = []
        for col in x:
            features.append(df[col].iloc[i]) 
        
        x_all.append(features)

        # 输出学习参考数据为下一周期结果
        y_all.append(df['label'].iloc[i+1])
    
    #划分学习数据和验证数据
    l=len(x_all)
    l2=int(l*(1-test_size))
    x_train,x_test,y_train,y_test = x_all[:l2:],x_all[l2:],y_all[:l2],y_all[l2:]

    return x_train,x_test,y_train,y_test
 
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
   

def CYC(P1=5, P2=13, P3=34):
    VAR1 = (CLOSE+OPEN)/200
    VAR2 = (3*HIGH+LOW+OPEN+2*CLOSE)/7
    VAR3 = SUM((CLOSE+OPEN) * VOL /2, P1)/VAR1/100
    VAR4 = SUM((CLOSE+OPEN) * VOL /2, P2)/VAR1/100
    VAR5 = SUM((CLOSE+OPEN) * VOL /2, P3)/VAR1/100
    CYC5 = DMA(VAR2, VOL/VAR3)
    CYC13 = DMA(VAR2, VOL/VAR4)
    CYC34 = DMA(VAR2, VOL/VAR5)
    return CYC5, CYC13, CYC34

def WINNER():
    WWW_999=IF(LOW>CLOSE,0,IF(HIGH<CLOSE,1,(CLOSE-LOW+0.01)/(HIGH-LOW+0.01)))
    winner=DMA(WWW_999,VOL/hgs.CAPITAL)*100
    return winner

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