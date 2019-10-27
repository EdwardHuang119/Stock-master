#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, event,MetaData,Table,select,insert,update
# from sqlalchemy import *
import pymysql

engine = create_engine('mysql+pymysql://root:4C6V&g96X@cdb-91rtu6jl.gz.tencentcdb.com:10045/Stock_test?charset=utf8')
conn = engine.connect()
metadata = MetaData(engine)

def serch():
    table = Table('stock_basic', metadata, autoload=True)
    s = select([table])
    conn.execute(s)

def insert():
    table =Table('stock_basic',metadata,autoload=True)

c=serch()
print(c)




