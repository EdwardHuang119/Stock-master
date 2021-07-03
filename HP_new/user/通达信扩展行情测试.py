'''
tdx扩展行情接口API
https://rainx.gitbooks.io/pytdx/content/pytdx_exhq.html

'''
#首先需要引入
from pytdx.exhq import TdxExHq_API

#然后，创建对象
api = TdxExHq_API()

#连接行情服务器
api.connect('106.14.95.149', 7727, time_out=30)

#获取市场代码
df=api.to_df(api.get_markets())

#输出信息
print(df)

df2=api.get_history_minute_time_data(31, "00020", 20170811)
df3=api.to_df(df2)
print(df3)

#断开连接
api.disconnect()


