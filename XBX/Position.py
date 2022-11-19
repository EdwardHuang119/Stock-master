#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

择时策略中使用到的计算持仓的函数
"""
import pandas as pd
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


# 由交易信号产生实际持仓
def position_at_close(df):
    """
    根据signal产生实际持仓。考虑涨跌停不能买入卖出的情况。
    所有的交易都是发生在产生信号的K线的结束时
    :param df:
    :return:
    """
    # ===由signal计算出实际的每天持有仓位
    # 在产生signal的k线结束的时候，进行买入
    df['signal'].fillna(method='ffill', inplace=True)
    df['signal'].fillna(value=0, inplace=True)  # 将初始行数的signal补全为0
    df['pos'] = df['signal'].shift()
    df['pos'].fillna(value=0, inplace=True)  # 将初始行数的pos补全为0

    # ===对涨跌停无法买卖做出相关处理。
    # 找出收盘价无法买入的K线
    cannot_buy_condition = df['收盘价'] >= df['涨停价']
    # 将找出上一周期无法买入的K线、并且signal为1时，的'pos'设置为空值
    df.loc[cannot_buy_condition.shift() & (df['signal'].shift() == 1), 'pos'] = None  # 2010-12-22

    # 找出收盘价无法卖出的K线
    cannot_sell_condition = df['收盘价'] <= df['跌停价']
    # 将找出上一周期无法卖出的K线、并且signal为0时的'pos'设置为空值
    df.loc[cannot_sell_condition.shift() & (df['signal'].shift() == 0), 'pos'] = None

    # pos为空的时，不能买卖，只能和前一周期保持一致。
    df['pos'].fillna(method='ffill', inplace=True)

    # ===如果是分钟级别的数据，还需要对t+1交易制度进行处理，在之后案例中进行演示

    # ===删除无关中间变量
    df.drop(['signal'], axis=1, inplace=True)

    return df
