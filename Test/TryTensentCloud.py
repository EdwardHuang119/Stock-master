#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import MySQLdb
import os
from configparser import ConfigParser
from sqlalchemy import create_engine
from string import Template

# 读取配置文件处理
configname = 'config.conf'
fatherpath = os.path.abspath(os.path.dirname(os.getcwd()))
configpath = fatherpath+'/confing'+'//'+configname
# print(configpath)
cf = ConfigParser()
cf.read(configpath)
# print(cf.sections())
dbchoese = "tencentcdb"
# dbchoese = 'localdb'
host = cf.get(dbchoese,"host")
port = int(cf.get(dbchoese,"port"))
user = cf.get(dbchoese,"user")
passwd = cf.get(dbchoese,"passwd")
dba = cf.get(dbchoese,"db")
hostandport = cf.get(dbchoese,'hostandport')

# print(host)


def connect_db():
    """Connect database and return db and cursor"""
    db = pymysql.connect(host=host,port=port,user=user,
                         passwd=passwd,db=dba)
    cursor = db.cursor()
    return (db,cursor)

def connect_db_engine():
    # scheme = 'mysql+pymysql://user:pass@host:port/dev_shopping?charset=utf8'
    # engine = create_engine(scheme)
    engine = create_engine(str(r"mysql+mysqldb://%s:" + '%s' + "@%s/%s?charset=utf8") % (user, passwd, hostandport, dba))
    return (engine)

if __name__ == "__main__":
    '''
    db,cursor = connect_db()
    sql_insert = "INSERT INTO stock_china_daily (`ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount`) VALUES ('000880.SZ', '2020-05-15 00:00:00', '7.74', '7.82','7.71','7.74','7.73','0.01','0.1294','18431.87','14297.047')"
    cursor.execute(sql_insert)
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s " % data)
    cursor.close()
    db.commit()
    db.close()
    '''
    engine = connect_db_engine()
    query_sql = """
          INSERT INTO `stock_china_daily` (`ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount`)
select
	`ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount` from stock_china_daily_temp;
          """
    # query_sql = Template(query_sql)
    # connection = engine.connect()
    # result = connection.execute("select version()")
    result = engine.execute(query_sql)
    # for r in result:
    #     print(r)
    # connection.close()
    engine.dispose()
    print('done')




