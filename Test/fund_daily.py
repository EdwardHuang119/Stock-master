#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Test.TushareProApi import *
import pandas as pd

show = True
show_func = print if show else lambda a: a

marker = 'E'
status= 'L'


def fund_analys_per(fund_portfolio,fund_code,end_date_1,end_date_2):
# 先要确定比对周期，之后从旧周期和新周期之间做比对。通过筛选切片确定有没有，如果有则开始和本周期的比对。
#     end_date_1 = '20201231'
#     end_date_2 = '20200930'
    symbol_1 = fund_portfolio.loc[(fund_portfolio['end_date']==end_date_1) & (fund_portfolio['ts_code']==fund_code)]['symbol'].tolist()
    symbol_2 = fund_portfolio.loc[(fund_portfolio['end_date']==end_date_2) & (fund_portfolio['ts_code']==fund_code)]['symbol'].tolist()
    symbol_new_buy = list(set(symbol_1).difference(set(symbol_2)))
    symbol_new_sell = list(set(symbol_2).difference(set(symbol_1)))
    symbol_analys = list(set(symbol_1).intersection(set(symbol_2)))
    symbol_union = list(set(symbol_1).union(set(symbol_2)))
    # show_func(symbol_1)
    # show_func(symbol_2)
    # show_func(symbol_new_buy)
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
            mkv = float(fund_portfolio.loc[
                (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                        fund_portfolio['end_date'] == end_date_1), 'mkv'])
            mkv_d_value = mkv
            amount = float(fund_portfolio.loc[
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
            mkv_ex = float(fund_portfolio.loc[
                          (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                                  fund_portfolio['end_date'] == end_date_2), 'mkv'])
            mkv_d_value = mkv-mkv_ex
            amount = 0
            amount_ex = float(fund_portfolio.loc[
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
            # print(symbol_union[i])
            amount = float(fund_portfolio.loc[
                (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                        fund_portfolio['end_date'] == end_date_1), 'amount'])
            amount_ex = float(fund_portfolio.loc[
                (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                        fund_portfolio['end_date'] == end_date_2), 'amount'])
            if amount-amount_ex > 0:
                operater = '增持'
            elif amount-amount_ex < 0:
                operater = '减仓'
            elif amount-amount_ex == 0:
                operater = '持有'
            mkv = float(fund_portfolio.loc[
                (fund_portfolio['ts_code'] == fund_code) & (fund_portfolio['symbol'] == symbol_union[i]) & (
                        fund_portfolio['end_date'] == end_date_1), 'mkv'])
            mkv_ex = float(fund_portfolio.loc[
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
        i=i+1
    print('基金%s，在截止在%s之前的操作数据已经完成分析' % (fund_code, end_date_1))
    return fund_portfolio_analys

def fund_analys_list(fund_portfolio,fund_code_list,end_date_1,end_date_2):
    fund_portfolio_analys = pd.DataFrame()
    for i in range(len(fund_code_list)):
        fund_portfolio_analys_per = fund_analys_per(fund_portfolio,fund_code_list[i],end_date_1,end_date_2)
        fund_portfolio_analys = pd.concat([fund_portfolio_analys, fund_portfolio_analys_per], ignore_index=True)
        print('已经完成第%s个基金操作分析，共有个%s'%(i+1,len(fund_code_list)))
        # print('基金%s，在截止在%s之前的操作数据已经完成分析' % (fund_code, end_date_1))
        i=i+1
    return fund_portfolio_analys

def hk_code(code):
    code = str(code)[1:]
    return code

# def Getfund_basic():
#     fund_basic = fund_basic(marker='')
#     return fund_basic

# def fund_portfolio(fund_code,end_date_ex,end_date_af):



if __name__ == "__main__":
    fund_basic = fund_basic(market='')
    # show_func(fund_basic)
    Tocsv(fund_basic,'','fund_basic')
    # '''
    # 全部基金的合集
    fund_code = fund_basic.loc[(fund_basic['status']=='L') & (fund_basic['market']=='E')]['ts_code'].tolist()
    # 单个基金
    # fund_code = '162416.SZ'
    # fund_code = ['320007.OF','000527.OF','540008.OF','001156.OF']
    fund_portfolio = fund_portfolio(fund_code)
    # Tocsv(fund_portfolio,'','fund_portfolio_all')
    # fund_portfolio = Read_csv('fund_portfolio_all','')
    fund_portfolio = fund_portfolio[
        (fund_portfolio['end_date'] == '20200630') | (fund_portfolio['end_date'] == '20200331')]
    fund_portfolio = fund_portfolio.drop_duplicates(subset=['ts_code', 'end_date', 'symbol'], keep='last',
                                                    inplace=False)
    # 下载的数据有重复，原因未知，需要做一次去除重复
    fund_portfolio = fund_portfolio.fillna(0)
    # 需要对空值进行填充
    show_func(fund_portfolio)
    
    Tocsv(fund_portfolio,'','fund_protfolio_2020seas_2')
    # fund_portfolio_analys = fund_analys_per(fund_portfolio,'162416.SZ','20201231','20200930')
    fund_portfolio_analys = fund_analys_list(fund_portfolio,fund_code,'20200630','20200331')
    # show_func(fund_portfolio_analys)
    Tocsv(fund_portfolio_analys,'','fund_protfolio_analys_2020_S2')
    # '''
    '''
    china_stock_basic = GetAlltscode('','','','')
    china_stock_basic = china_stock_basic[['ts_code','name']]
    hk_basic = hk_basic()
    hk_basic=hk_basic[['ts_code','name']]
    hk_basic['ts_code'] = hk_basic['ts_code'].apply(hk_code)
    # 港股改为4位代码
    Total_stock_name =pd.concat([china_stock_basic,hk_basic],ignore_index=True)
    Total_stock_name.columns=['symbol','stock_name']
    # Tocsv(Total_stock_name,'','Total_stock_name')
    # 测试效果
    fund_name = fund_basic[['ts_code','name']]
    # show_func(fund_name)
    fund_oper_analys = Read_csv('fund_protfolio_analys_All','')
    fund_oper_analys.loc[fund_oper_analys['operater']== '新进','mkv_d_value']= fund_oper_analys['mkv']
    fund_oper_analys = pd.merge(fund_oper_analys,fund_name,on=['ts_code'])
    fund_oper_analys = pd.merge(fund_oper_analys,Total_stock_name,on=['symbol'])
    fund_oper_analys = fund_oper_analys[['ts_code', 'name','end_date', 'symbol', 'stock_name','operater', 'mkv', 'mkv_d_value',
       'amount', 'amount_d_value', 'stk_mkv_ratio', 'stk_mkv_ratio_d_value',
       'stk_float_ratio', 'stk_float_ratio_d_value']]
    # 补基金公司名称和股票名称，然后调整一下列的分布。
    # Tocsv(fund_oper_analys,'','fund_oper_analys_2')
    # fund_oper_analys=fund_oper_analys.sort_values(by=['ts_code'])
    # 测试效果
    # 开始分析

    # fund_oper_analys_test_1 = fund_oper_analys.groupby(['symbol','stock_name','operater'])['operater'].count()
    # fund_oper_analys_test_1.columns = ['symbol','stock_name','operater','operator_count']
    fund_oper_analys_test = fund_oper_analys.groupby(['symbol', 'stock_name', 'operater']).agg({'operater':np.count_nonzero,'mkv':np.sum,'mkv_d_value':np.sum,'amount':np.sum})
    # fund_oper_analys_test_2 = fund_oper_analys.groupby(['symbol','stock_name','operater']).sum()
    # show_func(fund_oper_analys_test_2)
    # fund_oper_analys_test = pd.merge(fund_oper_analys_test_2,fund_oper_analys_test_1,on=['symbol','stock_name','operater'])
    show_func(fund_oper_analys_test)
    # 测试效果
    Tocsv(fund_oper_analys_test, '', 'fund_oper_test_3')
    '''


