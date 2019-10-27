# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import random

# 创建一个空dataframe,并且把列的数据名称加上（成功）
# list = [1,2,3]
# data1 = pd.DataFrame(columns=['姓名'])
# # print(type(data1))
# for x in list:
#     data1[x]=None
# data1['Total']=None
# print(data1)

# 建立一个测试用CSV,并中文保存
# people = ['小A','大名','猪头','七七','天才']
# Version = ["11月",'12月','1月']
# data = pd.read_csv(r"C:\Users\Edward & Bella\Desktop\WorkStaf\pandas\55555.csv",encoding="GBK")
# print(data)
# data2 = data.groupby(["人员","有效问题数"]).sum()
# # data2 = pd.to_datetime(data2('提交日期'),format=(%Y%m%d %H:%m:%s))
# print(data2)

# 尝试行列彼此相加
data={'state':['Ohio','Ohio','Ohio','Nevada','Nevada'],'year':[2000,2001,2002,2001,2002],'pop':[1.5,1.7,3.6,2.4,2.9]}
Test1=pd.DataFrame(data)
print(Test1)



