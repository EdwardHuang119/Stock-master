#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

择时策略中使用到的signal函数
"""
import pandas as pd
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


# =====移动平均线策略

# 简单移动平均线策略
def simple_moving_average_signal(df, para=[20, 120]):
    """
    简单的移动平均线策略。只能做多。
    当短期均线上穿长期均线的时候，做多，当短期均线下穿长期均线的时候，平仓
    :param df:
    :param para: ma_short, ma_long
    :return: 最终输出的df中，新增字段：signal，记录发出的交易信号
    """

    # ===策略参数
    ma_short = para[0]  # 短期均线。ma代表：moving_average
    ma_long = para[1]  # 长期均线

    # ===计算均线。所有的指标，都要使用复权价格进行计算。
    df['ma_short'] = df['收盘价_复权'].rolling(ma_short, min_periods=1).mean()
    df['ma_long'] = df['收盘价_复权'].rolling(ma_long, min_periods=1).mean()

    # ===找出做多信号
    condition1 = df['ma_short'] > df['ma_long']  # 短期均线 > 长期均线
    condition2 = df['ma_short'].shift(1) <= df['ma_long'].shift(1)  # 上一周期的短期均线 <= 长期均线
    df.loc[condition1 & condition2, 'signal'] = 1  # 将产生做多信号的那根K线的signal设置为1，1代表做多

    # ===找出做多平仓信号
    condition1 = df['ma_short'] < df['ma_long']  # 短期均线 < 长期均线
    condition2 = df['ma_short'].shift(1) >= df['ma_long'].shift(1)  # 上一周期的短期均线 >= 长期均线
    df.loc[condition1 & condition2, 'signal'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # ===删除无关中间变量
    df.drop(['ma_short', 'ma_long'], axis=1, inplace=True)

    return df


# 简单移动平均线策略参数
def simple_moving_average_para_list(ma_short=range(10, 200, 10), ma_long=range(10, 300, 10)):
    """
    产生简单移动平均线策略的参数范围
    :param ma_short:
    :param ma_long:
    :return:
    """
    para_list = []
    for short in ma_short:
        for long in ma_long:
            if short >= long:
                continue
            else:
                para_list.append([short, long])

    return para_list


def signal_gftd(df, para: list = None):
    """
    广发TD策略V2，只能做多不能做空，形成卖出形态会转换成平多仓
    :param df:  原始数据
    :param para:  参数，[n1, n2, n3]
    :return:
    """

    # 辅助函数，先跳过两个函数的内容
    def is_buy_count(i, pre_close) -> bool:
        """
        判断是否计数为买入形态，需要A，B，C三个条件同时满足才行
        :param i: 当前循环的index
        :param pre_close: 上一次计数的收盘价，第一次为None，会忽略C条件
        :return: bool
        """
        # A. 收盘价大于或等于之前第 2 根 K 线最高价;
        a = df.at[i, '收盘价_复权'] >= df.at[i - 2, '最高价_复权']
        # B. 最高价大于之前第 1 根 K 线的最高价;
        b = df.at[i, '最高价_复权'] > df.at[i - 1, '最高价_复权']
        # C. 收盘价大于之前第 1 个计数的收盘价。
        c = (df.at[i, '收盘价_复权'] > pre_close) if pre_close is not None else True
        return a and b and c

    def is_sell_count(i, pre_close) -> bool:
        """
        判断是否计数为卖出形态，需要A，B，C三个条件同时满足才行
        :param i: 当前循环的index
        :param pre_close: 上一次计数的收盘价，第一次为None，会忽略C条件
        :return: bool
        """
        # A. 收盘价小于或等于之前第 2 根 K 线最低价;
        a = df.at[i, '收盘价_复权'] <= df.at[i - 2, '最低价_复权']
        # B. 最低价小于之前第 1 根 K 线的最低价;
        b = df.at[i, '最低价_复权'] < df.at[i - 1, '最低价_复权']
        # C. 收盘价小于之前第 1 个计数的收盘价。
        c = (df.at[i, '收盘价_复权'] < pre_close) if pre_close is not None else True
        return a and b and c

    # ===参数
    if para is None:
        para = [4, 4, 4]  # 默认为4，4，4

    n1, n2, n3 = para

    # ===寻找启动点
    # 计算ud
    df['ud'] = 0  # 首先设置为0
    # 根据收盘价比较设置1或者-1
    df.loc[df['收盘价_复权'] > df.shift(n1)['收盘价_复权'], 'ud'] = 1
    df.loc[df['收盘价_复权'] < df.shift(n1)['收盘价_复权'], 'ud'] = -1

    # 对最近n2个ud进行求和
    df['udc'] = df['ud'].rolling(n2).sum()

    # 找出所有形成买入或者卖出的启动点，并且赋值为1或者-1
    # -1代表买入启动点，1代表卖出启动点
    df.loc[df['udc'].abs() == n2, 'checkpoint'] = df['udc'] / n2

    # 找出所有启动点的索引值，即checkpoint那一列非空的所有行
    check_point_index = df[df['checkpoint'].notnull()].index

    # ===生成买入或者卖出信号
    # [主循环] 从前往后，针对启动点的索引值进行循环
    for index in check_point_index:
        # 我们实际使用1代表买入，和启动点（checkpoint）正好相反，
        # 取负数就能计算得到可能使用的信号值，这里卖出信号是-1，之后会有处理
        signal = -df.at[index, 'checkpoint']

        # 缓存信号形成过程中的最高价和最低价，用于计算止损价格
        min_price = df.loc[index - n2: index, '最低价_复权'].min()
        max_price = df.loc[index - n2: index, '最高价_复权'].max()

        pre_count_close = None  # 之前第1个计数的收盘价，默认为空
        cum_count = 0  # 满足计数形态的累计值，默认清零
        stop_lose_price = 0  # 止损价格

        # [子循环] 从启动点（checkpoint）下一根k线开始往后，搜索满足buy count和sell count的形态
        for index2 in df.loc[index + 1:].index:
            close = df.at[index2, '最低价_复权']  # 当前收盘价
            min_price = min(min_price, close)  # 计算信号开始形成到这一步的最低价
            max_price = max(max_price, close)  # 计算信号开始形成到这一步的最高价

            # ==如果当前是启动点，并且当前k线满足buy count的形态
            # 1. 累计加一
            # 2. 缓存当前收盘价
            # 3. 记录止损价格（这一步并不会放到df中）
            if signal == 1 and is_buy_count(index2, pre_count_close):
                # 买入启动点
                cum_count += 1
                pre_count_close = close  # 更新前一个计数收盘价
                stop_lose_price = min_price
            elif signal == -1 and is_sell_count(index2, pre_count_close):
                # 卖出启动点
                cum_count += 1
                pre_count_close = close  # 更新前一个计数收盘价
                stop_lose_price = max_price

            # ==如果遇到新的启动点，重新开始计数
            #   退出子循环，继续主循环的下一个启动点处理
            if df.at[index2, 'checkpoint'] > 0 or df.at[index2, 'checkpoint'] < 0:
                break

            # ==如果累计计数达到n3，发出交易信号
            #   退出子循环，继续主循环的下一个启动点处理
            if cum_count == n3:
                # 设置当前信号
                df.loc[index2, 'signal'] = max(signal, 0)  # 如果是-1就赋值为0，这个信号函数不包含做空
                df.loc[index2, 'stop_lose_price'] = stop_lose_price  # 设置产生信号的时候的止损价格
                break

    # ===新增了signal（信号）列和对应的stop_lose_price（止损价）列
    # ===处理止损信号
    df['stop_lose_price'].fillna(method='ffill', inplace=True)  # 设置当前信号下所有行的止损价格
    df['cur_sig'] = df['signal']
    df['cur_sig'].fillna(method='ffill')
    stop_on_long_condition = (df['cur_sig'] == 1) & (df['收盘价_复权'] < df['stop_lose_price'])
    stop_on_short_condition = (df['cur_sig'] == 0) & (df['收盘价_复权'] > df['stop_lose_price'])
    df.loc[stop_on_long_condition | stop_on_short_condition, 'signal'] = 0  # 设置止损平仓信号

    # ===信号去重复
    temp = df[df['signal'].notnull()][['signal']]
    temp = temp[temp['signal'] != temp['signal'].shift(1)]
    df['signal'] = temp['signal']

    # ===去除不要的列
    df.drop(['ud', 'udc', 'checkpoint', 'stop_lose_price', 'cur_sig'], axis=1, inplace=True)

    # ===由signal计算出实际的每天持有仓位
    # signal的计算运用了收盘价，是每根K线收盘之后产生的信号，到第二根开盘的时候才买入，仓位才会改变。
    df['pos'] = df['signal'].shift()
    df['pos'].fillna(method='ffill', inplace=True)
    df['pos'].fillna(value=0, inplace=True)  # 将初始行数的position补全为0
    return df
