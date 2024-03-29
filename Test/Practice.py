# -*- coding: utf-8 -*-


import Test.TushareProApi
from Test.TushareProApi import GetdatlyfromCname
from Test.TushareProApi import Getconcept_detail
from Test.TushareProApi import Getdailyfromconcept
from Test.TushareProApi import moneyflowlist
# import Test.QyptTableView
# from Test.QyptTableView import Dataframdatashow
from Test.TushareProApi import trade_cal
from Test.TushareProApi import trade_cal_list
from Test.TushareProApi import hk_hold,index_classify,index_member
import sys
from Test.TushareProApi import Getdailyfromtscode
from Test.TushareProApi import Tocsv
from Test.TryTensentCloud import connect_db
from Test.TryTensentCloud import connect_db_engine
import pandas as pd
import datetime
import time
from datetime import date
from dateutil.relativedelta import relativedelta

def index_get():
    level = ['l1', 'l2', 'l3']
    index = pd.DataFrame()
    for i in range(len(level)):
        index_per = index_classify(level[i])
        index = pd.concat([index, index_per], ignore_index=True)
        i = i + 1
    return index

def index_menber_get():
    index = index_get()
    index_member_list = index['index_code'].values.tolist()
    index_member_1 =pd.DataFrame()
    for i in range(len(index_member_list)):
        index_member_per = index_member(index_member_list[i],'')
        index_member_1 = pd.concat([index_member_1,index_member_per],ignore_index=True)
        i=i+1
    return index_member_1

show = True
show_func = print if show else lambda a: a

# Chinadaily = Getdailyfromtscode('','20200508','20200508')


if __name__ == "__main__":
    end_date = date.today()
    dateTime_p = datetime.datetime.now()
    str_p = datetime.datetime.strftime(dateTime_p, '%Y%m%d')
    # show_func(str(end_date),type(str(end_date)))
    show_func(str_p,type(str_p))

    
    '''
    index_member = index_menber_get()
    index = index_get()
    index_member['in_date']= pd.to_datetime(index_member['in_date'],format='%Y%m%d')
    # index_member = index_member['out_date'] !='None'
    show_func(index_member)
    # show_func(index)
    '''
    '''
    engine = connect_db_engine()
    try:
        index_member.to_sql('index_member_temp', con=engine, if_exists='replace', index=False)
    except Exception as e:
        print(e)
    engine.dispose()
    '''



    '''
    # 港股通数据存储
    starttime = datetime.datetime.now()
    start_date = '20200602'
    end_date = '20200621'
    period = trade_cal_list(start_date, end_date, '')
    HK_hold_DataFrame = pd.DataFrame()
    for i in range(len(period)):
        HK_hold_list_per = hk_hold(period[i], '', '')
        HK_hold_DataFrame = pd.concat([HK_hold_DataFrame, HK_hold_list_per],ignore_index=True)
        print('%s的数据已经完全获取' % (period[i]))
        i = i + 1
        time.sleep(0.2)
    # hk_hold = hk_hold('','20141117','20200621')
    # trade_cal['cal_date'] = pd.to_datetime(trade_cal['cal_date'], format='%Y%m%d')
    HK_hold_DataFrame['trade_date'] = pd.to_datetime( HK_hold_DataFrame['trade_date'], format='%Y%m%d')
    show_func(HK_hold_DataFrame.shape[0])
    show_func(HK_hold_DataFrame)
    engine = connect_db_engine()
    try:
        HK_hold_DataFrame.to_sql('stock_temp', con=engine, if_exists='replace', index=False)
        print('%s到%s的数据已经导入到临时表中,共导入了%s条' %(start_date,end_date,HK_hold_DataFrame.shape[0]))
    except Exception as e:
        print(e)
    try:
        query_sql = """
        INSERT INTO `stock_hk_hold` (`trade_date`, `ts_code`, `name`, `vol`, `ratio`, `exchange`)
        SELECT
        `trade_date`, `ts_code`, `name`, `vol`, `ratio`, `exchange` FROM stock_temp;
                             """
        query_sql2 = """
                       delete from stock_temp
                   """
        engine.execute(query_sql)
        print('数据已经导入到正是表')
        engine.execute(query_sql2)
        print('临时表数据已经删除')
    except Exception as ae:
        print(ae)
    engine.dispose()
    endtime = datetime.datetime.now()
    print('从', starttime, '开始，到', endtime, '结束，耗时为', endtime - starttime, '。共导入数据', HK_hold_DataFrame.shape[0], '条。')
    # 港股数据存储结束
    '''
    '''
    # 尝试从数据库获取数据转dataframe
    engine = connect_db_engine()
    sql = """select * from stock_china_daily where trade_date >= '2020-01-01'"""
    chinadaily = pd.read_sql_query(sql, engine)
    show_func(chinadaily.head())
    show_func(chinadaily.shape[0])
    engine.dispose()
    # 尝试从数据库获取数据转dataframe，结束
    '''
    '''
    # 存交易日历
    engine = connect_db_engine()
    trade_cal_sse = trade_cal('20200101','20201231','')
    trade_cal_hk = trade_cal('20200101','20201231','XHKG')
    trade_cal = pd.concat([trade_cal_sse,trade_cal_hk],ignore_index=True)
    trade_cal['cal_date'] = pd.to_datetime(trade_cal['cal_date'],format='%Y%m%d')
    try:
        trade_cal.to_sql('stock_china_daily_temp', con=engine, if_exists='replace', index=False)
    except Exception as e:
        print(e)
    show_func(trade_cal)
    engine.dispose()
    # 存交易日历结束
    '''
    '''
    # 练习怎么从数据库获取数据信息
    engine = connect_db_engine()
    result = engine.execute("select max(trade_date) from stock_china_daily ")
    for row in result:
        # print(row['max(trade_date)'],type(row['max(trade_date)']),row['max(trade_date)']+datetime.timedelta(days=1))
        startdate =row['max(trade_date)']+datetime.timedelta(days=1)
        startdate = startdate.strftime('%Y%m%d')
    time_temp =datetime.datetime.now()
    enddate = time_temp.strftime('%Y%m%d')
    if startdate == enddate:
        print('截止到%s的数据已经获取完整'%(enddate))
    else:
        print('开始获取%s到%f的数据'%(startdate,enddate))
    # print(startdate,enddate)
    engine.dispose()
    '''
    '''
    # 练习一些怎么获取把东西导入到数据库里面。通过To_sql命令来实现，效果是明显提速了。
    Chinadaily = Getdailyfromtscode('','20200316','20200319')
    # Chinadaily = Chinadaily.head()
    # Chinadaily['trade_date'] = pd.to_datetime(Chinadaily['trade_date'],format='%Y%m%d')
    show_func(Chinadaily.shape[0])
    engine = connect_db_engine()
    try:
        Chinadaily.to_sql('stock_china_daily_temp', con=engine, if_exists='replace', index=False)
    except Exception as e:
        print(e)
    print('数据已经导入临时表，共导入数据%s条' % (str(Chinadaily.shape[0])))
    try:
        query_sql = """
                  INSERT INTO `stock_china_daily` (`ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount`)
        select
        	`ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount` from stock_china_daily_temp;
                  """
        query_sql2 = """
            delete from stock_china_daily_temp
        """
        engine.execute(query_sql)
        print('数据已经导入到正是表')
        engine.execute(query_sql2)
        print('临时表数据已经删除')
    except Exception as ae:
        print(ae)
    engine.dispose()
    '''
'''
    for i in range(Chinadaily.shape[0]):
        try:
            c_len = Chinadaily.shape[0]
            resu0 = list(Chinadaily.ix[c_len-1-i])
            print(resu0)
        except Exception as aa:
            print(aa)
            print('No DATA Code: ' + str(i))
            continue

        insert_sql = "INSERT INTO stock_china_daily (`ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount`) VALUES ('%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s')" % (str(resu0[0]),str(resu0[1]),float(resu0[2]),float(resu0[3]),float(resu0[4]),float(resu0[5]),float(resu0[6]),float(resu0[7]),float(resu0[8]),float(resu0[9]),float(resu0[10]))
            print(insert_sql)
        except Exception as ab:
            print(ab)
            continue
连接数据库
    db,cursor = connect_db()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s " % data)
    
    engine = connect_db_engine()
    try:
        Chinadaily.to_sql('stock_china_daily', con=engine, if_exists='replace', index=False)
    except Exception as e:
        print(e)
'''
    # db.close()





# daily = GetdatlyfromCname('宋城演A', '20190101', '20191002')
# conceptlist = Getdailyfromconcept('TS355', 20191009, 20191010)

# Dataframdatashow(conceptlist)
# Dataframdatashow(Getconcept_detail('TS328',''))
# Dataframdatashow(moneyflowlist(stock_list,'','20190601','20191018'))
# Dataframdatashow(moneyflowlist(stock_list,'','20190701','20191018'))
'''
# 交易日历的集合
A =trade_cal('20200101','20200215')
# show_func(type(A),A)
B =A.loc[A['is_open'] ==1]['cal_date'].tolist()
# B =B['cal_date'].tolist()
show_func(type(B),B)
'''
