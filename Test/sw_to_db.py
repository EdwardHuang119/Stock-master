#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from Test.TushareProApi import *
from Test.TryTensentCloud import connect_db
from Test.TryTensentCloud import connect_db_engine
import datetime

show = True
show_func = print if show else lambda a: a
engine = connect_db_engine()

def sw_date_list(start_date,end_date):
    sql = "select cal_date from trade_cal where is_open = 1 and `exchange`='SSE' and cal_date between '%s' and '%s'" % (start_date, end_date)
    date_list = pd.read_sql(sql,engine)
    date_list['cal_date'] = date_list['cal_date'].apply(lambda x: x.strftime('%Y%m%d'))
    date_list=date_list['cal_date'].tolist()
    return date_list

def sw_date_get(start_date,end_date):
    # 从日期下手
    # start_date=time_temp.strftime('%Y%m%d')
    # end_date = time_temp.strftime('%Y%m%d')
    date_list = sw_date_list(start_date,end_date)
    if date_list:
        sw_date = pd.DataFrame()
        for i in range(len(date_list)):
            sw_date_per = index_sw_daily_trade(trade_date = date_list[i])
            sw_date = pd.concat([sw_date,sw_date_per],ignore_index= True)
            print('%s的数据已经获取'%(date_list[i]))
            time.sleep(2)
            i = i+1
        '''
        index_class = index_classify('')
        index_code_list = index_class['index_code'].tolist()
        # show_func(index_code_list)
        # 循环获取行业数据
            for i in range(len(index_code_list)):
            # 首先获取数据信息
            sw_date_per = index_sw_daily(ts_code=index_code_list[i], start_date=start_date, end_date=end_date)
            # 返回的数据日期是倒序的，改为升序
            # sw_date_per = sw_date_per.sort_values(by=['trade_date'], ascending=True)
            sw_date = pd.concat([sw_date,sw_date_per],ignore_index= True)
            time.sleep(0.4)
            i = i+1
        '''
        print('共获取数据',sw_date.shape[0],'条')
    else:
        print('没有要下载的数据')
        sw_date = pd.DataFrame()
    # show_func(sw_date)
    return sw_date


def sw_date_insert(data):
    try:
        data.to_sql('stock_temp', con=engine, if_exists='replace', index=False)
    except Exception as e:
        print(e)
    try:
        query_sql = """
   INSERT INTO `stockindex_china_sw` (`ts_code`, `trade_date`, `name`,`open`, `low`, `high`, `close`, `change`, `pct_change`, `vol`, `amount`,`pe`,`pb`)
 select `ts_code`, `trade_date`, `name`,`open`, `low`, `high`, `close`, `change`, `pct_change`, `vol`, `amount`,`pe`,`pb` from stock_temp;
                                          """
        query_sql2 = """
                delete from stock_temp
            """
        engine.execute(query_sql)
        print('数据已经导入到正式表')
        engine.execute(query_sql2)
        print('临时表数据已经删除')
    except Exception as ae:
        print(ae)
    engine.dispose()
    return print('已经导入')

def start_date_get():
    result = engine.execute("select max(trade_date) from stockindex_china_sw ")
    for row in result:
        start_date = row['max(trade_date)'] + datetime.timedelta(days=1)
    return start_date

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    start_date = start_date_get()
    time_temp = datetime.datetime.now()
    end_date = time_temp.strftime('%Y-%m-%d')
    # end_date = '2021-05-28'
    data = sw_date_get(start_date,end_date)
    if data.empty:
        pass
    else:
        # show_func(data)
        sw_date_insert(data)
        endtime = datetime.datetime.now()
        print('从', starttime, '开始，到', endtime, '结束，耗时为', endtime - starttime)

