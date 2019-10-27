#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import os
from configparser import ConfigParser


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

# print(host)


def connect_db():
    """Connect database and return db and cursor"""
    db = pymysql.connect(host=host,port=port,user=user,
                         passwd=passwd,db=dba)
    cursor = db.cursor()
    return (db,cursor)

db,cursor = connect_db()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print("Database version : %s " % data)
db.close()


# def connect_db():
#     """Connect database and return db and cursor"""
#     db = pymysql.connect(host="cdb-91rtu6jl.gz.tencentcdb.com",port=10045,user='root',
#                          passwd='3621@(!jj',db="Stock_test")
#     cursor = db.cursor()
#     return (db,cursor)
#
# db,cursor = connect_db()
# cursor.execute("SELECT VERSION()")
# data = cursor.fetchone()
# print("Database version : %s " % data)
# db.close()