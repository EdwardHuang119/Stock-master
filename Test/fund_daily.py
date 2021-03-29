#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Test.TushareProApi import *
import pandas as pd

show = True
show_func = print if show else lambda a: a

marker = 'E'
# 字典项为E为场内，O为场外
status= 'L'
# 字典想为上市

fund_basic = fund_basic(market='')
# fund_code = fund_basic.loc[(fund_basic['status']=='L') & (fund_basic['market']=='E')]['ts_code'].tolist()
fund_code = '502056.SH'
fund_portfolio = fund_portfolio(fund_code)
fund_portfolio=fund_portfolio.drop_duplicates(inplace=False)
# fund_portfolio['mkv'] = fund_portfolio['mkv'].astype(int)
# 下载的数据有重复，原因未知，需要做一次去除重复

# Tocsv(fund_portfolio,'','fund_protfolio_test_4')
# show_func(fund_portfolio)



# 先要确定比对周期，之后从旧周期和新周期之间做比对。通过筛选切片确定有没有，如果有则开始和本周期的比对。
end_date_1 = '20201231'
end_date_2 = '20200930'
symbol_1 = fund_portfolio.loc[(fund_portfolio['end_date']==end_date_1) & (fund_portfolio['ts_code']==fund_code)]['symbol'].tolist()
symbol_2 = fund_portfolio.loc[(fund_portfolio['end_date']==end_date_2) & (fund_portfolio['ts_code']==fund_code)]['symbol'].tolist()
symbol_new_buy = list(set(symbol_1).difference(set(symbol_2)))
symbol_new_sell = list(set(symbol_2).difference(set(symbol_1)))
symbol_analys = list(set(symbol_1).intersection(set(symbol_2)))
symbol_union = list(set(symbol_1).union(set(symbol_2)))


show_func(symbol_1)
show_func(symbol_2)
show_func(symbol_new_buy)
# show_func(symbol_new_sell)
# show_func(symbol_analys)
# show_func(symbol_union)

colum = ['ts_code','end_date','symbol','operater','mkv','mkv_d_value','amount','amount_d_value','stk_mkv_ratio','stk_mkv_ratio_d_value','stk_float_ratio','stk_float_ratio_d_value']
fund_portfolio_analys = pd.DataFrame(columns=colum)
for i in range(len(symbol_union)):
    ts_code= fund_code
    symbol = symbol_union[i]
    if symbol_union[i] in symbol_new_buy:
        operater = '新进'
        mkv = int(fund_portfolio.loc[
            (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                    fund_portfolio['end_date'] == end_date_1), 'mkv'])
        mkv_d_value = 0
        amount = int(fund_portfolio.loc[
            (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                    fund_portfolio['end_date'] == end_date_1), 'amount'])
        amount_d_value = amount
        stk_mkv_ratio = float(fund_portfolio.loc[
            (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                    fund_portfolio['end_date'] == end_date_1), 'stk_mkv_ratio'])
        stk_mkv_ratio_d_value =stk_mkv_ratio
        stk_float_ratio = float(fund_portfolio.loc[
            (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                    fund_portfolio['end_date'] == end_date_1), 'stk_float_ratio'])
        stk_float_ratio_d_value = stk_float_ratio
        # show_func(mkv,type(mkv))
    elif symbol_union[i] in symbol_new_sell:
        operater = '抛售'
        mkv = 0
        mkv_ex = int(fund_portfolio.loc[
                      (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                              fund_portfolio['end_date'] == end_date_2), 'mkv'])
        mkv_d_value = mkv-mkv_ex
        amount = 0
        amount_ex = int(fund_portfolio.loc[
            (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                    fund_portfolio['end_date'] == end_date_2), 'amount'])
        amount_d_value = amount - amount_ex
        stk_mkv_ratio = 0
        stk_mkv_ratio_ex = float(fund_portfolio.loc[
            (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                    fund_portfolio['end_date'] == end_date_2), 'stk_mkv_ratio'])
        stk_mkv_ratio_d_value =stk_mkv_ratio-stk_mkv_ratio_ex
        stk_float_ratio = 0
        stk_float_ratio_ex = float(fund_portfolio.loc[
            (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                    fund_portfolio['end_date'] == end_date_2), 'stk_float_ratio'])
        stk_float_ratio_d_value = stk_float_ratio-stk_float_ratio_ex
        # show_func(mkv,type(mkv))
    elif symbol_union[i] in symbol_analys:
        amount = int(fund_portfolio.loc[
            (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                    fund_portfolio['end_date'] == end_date_1), 'amount'])
        amount_ex = int(fund_portfolio.loc[
            (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                    fund_portfolio['end_date'] == end_date_2), 'amount'])
        if amount-amount_ex > 0:
            operater = '增持'
        elif amount-amount_ex < 0:
            operater = '减仓'
        elif amount-amount_ex == 0:
            operater = '持有'
        mkv = int(fund_portfolio.loc[
            (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                    fund_portfolio['end_date'] == end_date_1), 'mkv'])
        mkv_ex = int(fund_portfolio.loc[
                      (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                              fund_portfolio['end_date'] == end_date_2), 'mkv'])
        mkv_d_value = mkv-mkv_ex
        amount_d_value = amount -amount_ex
        stk_mkv_ratio = float(fund_portfolio.loc[
            (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                    fund_portfolio['end_date'] == end_date_1), 'stk_mkv_ratio'])
        stk_mkv_ratio_ex = float(fund_portfolio.loc[
            (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                    fund_portfolio['end_date'] == end_date_2), 'stk_mkv_ratio'])
        stk_mkv_ratio_d_value =stk_mkv_ratio-stk_mkv_ratio_ex
        stk_float_ratio = float(fund_portfolio.loc[
            (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                    fund_portfolio['end_date'] == end_date_1), 'stk_float_ratio'])
        stk_float_ratio_ex = float(fund_portfolio.loc[
            (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                    fund_portfolio['end_date'] == end_date_2), 'stk_float_ratio'])
        stk_float_ratio_d_value = stk_float_ratio-stk_float_ratio_ex
        # show_func(mkv, type(mkv))
    fund_portfolio_analys = fund_portfolio_analys.append(pd.DataFrame({'ts_code':[ts_code],'end_date':[end_date_1],'symbol':[symbol],'operater':[operater],'mkv':[mkv],'mkv_d_value':[mkv_d_value],'amount':[amount],'amount_d_value':[amount_d_value],'stk_mkv_ratio':[stk_mkv_ratio],'stk_mkv_ratio_d_value':[stk_mkv_ratio_d_value],'stk_float_ratio':[stk_float_ratio],'stk_float_ratio_d_value':[stk_float_ratio_d_value]}),ignore_index=True)
# fund_portfolio_analys['symbol'] = pd.Series[symbol_union]
# fund_portfolio_analys = fund_portfolio_analys.columns = ['ts_code','end_date','symbol','operater','mkv','amount','amount_d_value']
show_func(fund_portfolio_analys)
Tocsv(fund_portfolio_analys,'','fund_protfolio_analys_test')