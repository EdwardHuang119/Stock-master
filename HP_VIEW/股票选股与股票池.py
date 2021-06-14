# -*- coding: utf-8 -*-
#通过基本面选股，建立股票池
import pickle
import tushare as ts
#import HP_data as ts  #如果有xbdata数据,离线学习用这句替换上一句.

#（1）获取最新股票数据
df=ts.get_today_all()
df1=df.copy()  #建立一个备份

#（2）删除业绩较差的ST股票
df1['a']=[('ST' in x )for x in df1.name.astype(str)]  #先给ST股票做标记a
df1=df1.set_index('a')  #将a设置为索引 
df1=df1.drop(index=[True]) #删除ST股票
df1=df1.reset_index(drop=True) #重建默认索引


#（3）选取市盈率前100名股票,作为股票池zxg
n=100  #选择前n个数据
df2=df1.sort_values(by=['per'],ascending=True).head(n)
zxg=list(df2.code)  #把选出股票代码转为列表
print('\n基本面选股结果zxg ：',zxg)

#（4）把选出的股票代码，保存到自选股板块文件“zxg.dat”文件中。
f = open('zxg.dat', 'wb')  
pt=pickle.dumps(zxg,0)
f.write(pt)
f.close()  

#（5）获取zxg.dat文件,并还原为股票池数据zxg2
f = open('zxg.dat', 'rb')  
zxg2=pickle.load(f)
f.close()  
print('\n获取股票池数据zxg2：',zxg2)