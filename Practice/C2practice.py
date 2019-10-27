#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
from collections import OrderedDict
from functools import reduce


def sample_211():
    """
    量化语言-Python
    :return:
    """
    price_str = '30.14, 29.58, 26.36, 32.56, 32.82'
    print('type(price_str):', type(price_str))

    if not isinstance(price_str, str):
        # not代表逻辑‘非’， 如果不是字符串，转换为字符串
        price_str = str(price_str)
    if isinstance(price_str, int) and price_str > 0:
        # and 代表逻辑‘与’，如果是int类型且是正数
        price_str += 1
    elif isinstance(price_str, float) or float(price_str[:4]) < 0:
        # or 代表逻辑‘或’，如果是float或者小于0
        price_str += 1.0
    else:
        try:
            raise TypeError('price_str is str type!')
        except TypeError:
            print('raise, try except')

def sample_212(show=True):
    show_func = print if show else lambda a: a
    price_str = '30.14, 29.58, 26.36, 32.56, 32.82'
    price_str = price_str.replace(' ', '')
    price_array = price_str.split(',')
    show_func(price_array)
    price_array.append('32.82')
    show_func(price_array)
    show_func(set(price_array))
    '''''''''
    # 如下这个方法不行，如下方法是准备先判断一下price_arrey的长度，然后循环找，找到了就去掉一个。但是因为会导致len（price_array）变成变长导致超过边界
    for i in range(0,len(price_array)):
        if str(price_array[i]) == '32.82':
            print(i,price_array[i])
            del price_array[i]
        # print(i,price_array[i])
            i = i+1
    show_func(price_array)
    '''''''''

    date_array = []
    date_base = 20170118
    # 这里用for只是为了计数，无用的变量python建议使用'_'声明
    for _ in range(0, len(price_array)):
        date_array.append(str(date_base))
        # 本节只是简单示例，不考虑日期的进位
        date_base += 1
    show_func(date_array)


    date_base = 20170118
    date_array = [str(date_base + ind) for ind, _ in enumerate(price_array)]
    # enumerrate这个函数就是这么用的，会把一个list拆成一个从0开始的序号和本身的元素的一个新的list
    show_func(date_array)

    stock_tuple_list = [(date, price) for date, price in zip(date_array, price_array)]
    # tuple访问使用索引
    show_func('20170119日价格：{}'.format(stock_tuple_list[1][1]))
    # show_func()
    show_func(stock_tuple_list)

    stock_tuple_list = [(date, price) for date, price in zip(date_array, price_array)]
    # tuple访问使用索引
    show_func('20170119日价格：{}'.format(stock_tuple_list[1][1]))
    show_func(stock_tuple_list)

    stock_namedtuple = namedtuple('stock', ('date', 'price'))
    stock_namedtuple_list = [stock_namedtuple(date, price) for date, price in zip(date_array, price_array)]
    # namedtuple访问使用price
    show_func('20170119日价格：{}'.format(stock_namedtuple_list[1].price))
    show_func(stock_namedtuple_list)
    # show_func(stock_namedtuple_list[0],stock_namedtuple_list[0][1],stock_namedtuple_list[0][0])

    # 字典推导式：{key: value for in}
    stock_dict = {date: price for date, price in zip(date_array, price_array)}
    show_func('20170119日价格：{}'.format(stock_dict['20170119']))
    show_func(stock_dict)

    show_func(stock_dict.keys())

    stock_dict = OrderedDict((date, price) for date, price in zip(date_array, price_array))
    show_func(stock_dict.keys())
    return stock_dict

def sample_221():
    """
    2.2.1 函数的使用和定义
    :return:
    """
    stock_dict = sample_212(show=False)
    print(stock_dict)
    # print(stock_dict.values(),type(stock_dict.values()))
    print('min(stock_dict):', min(stock_dict))
    # print(stock_dict.keys(),type(stock_dict.keys()),stock_dict.values(),type(stock_dict.values()))
    # newturble = (zip(stock_dict.values(),stock_dict.keys()))
    # 如果想给字典求得最大值/最小值/排序后，能同时得到键值对，就需要使用zip()把键值反转过来，形成(值，键) 元组序列，然后再求最大值/最小值/排序。
    # zip()的返回值是一个只能访问一次的迭代器。
    # print(newturble,type(newturble))
    print('min(zip(stock_dict.values(), stock_dict.keys())):', min(zip(stock_dict.values(), stock_dict.keys())),type(min(zip(stock_dict.values(), stock_dict.keys()))))
    # print(min(newturble))

    def find_second_max(dict_array):
        # 对传入的dict sorted排序
        stock_prices_sorted = sorted(zip(dict_array.values(), dict_array.keys()))
        # 第二大的也就是倒数第二个
        return stock_prices_sorted[-2]

    # 系统函数callable验证是否为一个可call的函数
    if callable(find_second_max):
        print('find_second_max(stock_dict):', find_second_max(stock_dict))

def sample_222():
    """
    2.2.2 lambda函数
    :return:
    """
    stock_dict = sample_212(show=False)

    find_second_max_lambda = lambda dict_array: sorted(zip(dict_array.values(), dict_array.keys()))[-2]
    print('find_second_max_lambda(stock_dict):', find_second_max_lambda(stock_dict))

    def find_max_and_min(dict_array):
        # 对传入的dict sorted排序R
        stock_prices_sorted = sorted(zip(dict_array.values(), dict_array.keys()))
        return stock_prices_sorted[0], stock_prices_sorted[-1]

    print('find_max_and_min(stock_dict):', find_max_and_min(stock_dict))

def sample_223(show=True):
    """
    2.2.3 高阶函数
    :return:
    """
    stock_dict = sample_212(show=False)
    show_func = print if show else lambda a: a

    # 将字符串的的价格通过列表推导式显示转换为float类型
    # 由于stock_dict是OrderedDict所以才可以直接
    # 使用stock_dict.values()获取有序日期的收盘价格
    price_float_array = [float(price_str) for price_str in stock_dict.values()]
    # 通过将时间平移形成两个错开的收盘价序列，通过zip打包成为一个新的序列，
    # 通过[:-1]:从第0个到倒数第二个，[1:]：从第一个到最后一个 错开形成相邻
    # 组成的序列每个元素为相邻的两个收盘价格
    pp_array = [(price1, price2) for price1, price2 in zip(price_float_array[:-1], price_float_array[1:])]
    show_func(pp_array)
    # list for python3
    change_array = list(map(lambda pp: reduce(lambda a, b: round((b - a) / a, 3), pp), pp_array))
    # list insert插入数据，将第一天的涨跌幅设置为0
    change_array.insert(0, 0)
    show_func(change_array)

if __name__ == "__main__":
    # sample_212()
    # sample_221()
    # sample_222()
    sample_223()