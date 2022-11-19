#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
邢不行-股票量化入门训练营
邢不行微信：xbx9585
Day2：如何获取股票的实时价格
"""
import pandas as pd
import time
from urllib.request import urlopen  # python自带爬虫库
import urllib.request


# # =====直接通过网址获取数据
# import sys
# import requests
# url = 'https://27.push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.600000&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=0&end=20500101&lmt=120'
# r = requests.get(url).json()['data']['klines']
# l = [i.split(',') for i in r]
# df = pd.DataFrame(l)
# df = df[[0, 1, 2, 3, 4, 5, 6]]
# df.columns = ['交易日期', '开盘价', '收盘价', '最高价', '最低价', '成交量', '成交额']
# print(df)
# sys.exit()
# # 由于新浪网站接口一月份更新后无法直接从网页抓取，可以通过东财网址进行查看，具体可以看目录里的神奇的网址图文攻略


def requestForNew(url, max_try_num=10, sleep_time=5):
    headers = {
        'Referer': 'http://finance.sina.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62'
    }
    request = urllib.request.Request(url, headers=headers)
    for i in range(max_try_num):
        response = urlopen(request)
        if response.code == 200:
            return response.read().decode('gbk')
        else:
            print("链接失败", response)
            time.sleep(sleep_time)

# =============================以上代码不需要修改==============================================


# =====构建网址
# 正常股票：sh600000 sz000002，退市股票：sh600002 sz000003、停牌股票：sz300124，除权股票：sh600276，上市新股：sz002952
stock_code_list = ['sh600352', 'sz000001', 'sh600356','sh600882','sz300740','sh603185','sz300037','sz002624','sz002352','sz000756'] #在后面添加,' '即可，注意一定要用英文符号
url = "https://hq.sinajs.cn/list=" + ",".join(stock_code_list)



# =============================以下代码不需要修改==============================================

# =====抓取数据
# 需要电脑联网
content = requestForNew(url)
# print(content)
# exit()

# =====将数据转换成DataFrame
data_line = content.strip().split('\n')  # 去掉文本前后的空格、回车等。每行是一个股票的数据
data_line = [i.replace('var hq_str_', '').split(',') for i in data_line]
df = pd.DataFrame(data_line, dtype='float')
print(df)

# =====对DataFrame进行整理
df[0] = df[0].str.split('="')
df['stock_code'] = df[0].str[0].str.strip()
df['stock_name'] = df[0].str[-1].str.strip()
df['candle_end_time'] = pd.to_datetime(df[30] + ' ' + df[31])  # 股票市场的K线，是普遍以当跟K线结束时间来命名的

rename_dict = {1: 'open', 2: 'pre_close', 3: 'close', 4: 'high', 5: 'low', 6: 'buy1', 7: 'sell1',
               8: 'amount', 9: 'volume', 32: 'status'}  # 自己去对比数据，会有新的返现
df.rename(columns=rename_dict, inplace=True)
df['status'] = df['status'].str.strip('";')
df = df[['stock_code', 'stock_name', 'candle_end_time', 'open', 'high', 'low', 'close', 'pre_close', 'amount', 'volume',
         'buy1', 'sell1', 'status']]
print(df)

# =====保存数据
df.to_csv('xingbuxing_stock_data_20220911.csv', index=False)

# =====打卡作业
# 任意选取10只股票，获取其最新数据，将数据保存到csv文件，发送到课程群。发送“day2作业打卡”并@助教


# =====打卡福利
# 赠送一份完整股票历史数据
