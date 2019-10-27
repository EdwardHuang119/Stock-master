# -*- coding: utf-8 -*-
import baostock as bs
import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import tushare as ts
from sqlalchemy import create_engine, event,MetaData,Table,select,insert,update

engine = create_engine('mysql+pymysql://root:4C6V&g96X@cdb-91rtu6jl.gz.tencentcdb.com:10045/Stock_test?charset=utf8')
conn = engine.connect()
metadata = MetaData(engine)

lg = bs.login(user_id="anonymous", password="123456")

# 获取股票的基本记录
# rs = bs.query_stock_basic(code="sh.600000")
rs = bs.query_stock_basic()
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)
result.to_sql('stock_basic_tmp',con=engine,if_exists='append',index=False)
print(type(result))
# print(result)


#鉴于code返回的是一个SZ.00001的形式，所以将这一列单独提取，形成list。转换拆分之后再导入回去
code_data = result.pop('code')
# pop会切割一列出来。原来的result会改变的。
code_datalist = np.array(code_data)
code_datalist = code_datalist.tolist()
# print(code_datalist)
# print(len(code_datalist),type(len(code_datalist)))
code_no=[]
for x in range(len(code_datalist)):
    code_no_item = code_datalist[x][3:]
    code_localtion_item = code_datalist[x][:2]
    code =[code_no_item,code_localtion_item]
    code_no.append(code)
code_no_df = DataFrame(data=code_no,columns=['code','mark'])
# 把分割一列并且刚刚生成的数据拼接成最终的结果，如下:
Stock_basic = pd.concat([code_no_df,result],axis=1)
# Stock_basic = pd.DataFrame(Stock_basic)
# print(type(Stock_basic))
# print(Stock_basic['code_name'].str.len().sort_values(),type(Stock_basic['code_name'].str.len()))
# 补足退市日期为默认值，保证导入数据库正常
Stock_basic['outDate'].replace('','1900-01-01',inplace=True)
# Stock_basic.to_csv(r'C:\Users\Edward & Bella\Desktop\WorkStaf\量化\112.csv',encoding='utf_8_sig')
print(Stock_basic)


# print(Stock_basic['outDate'].sort_values()=='')


# 导入数据库中
# Stock_basic.to_sql('stock_basic',con=engine,index=False,if_exists='append')

bs.logout()

