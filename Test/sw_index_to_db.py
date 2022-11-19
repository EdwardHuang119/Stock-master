#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from Test.TushareProApi import *
from Test.TryTensentCloud import connect_db
from Test.TryTensentCloud import connect_db_engine
import datetime

show = True
show_func = print if show else lambda a: a
engine = connect_db_engine()


if __name__ == "__main__":
    starttime = datetime.datetime.now()
    # start_date = start_date_get()
    time_temp = datetime.datetime.now()
    end_date = time_temp.strftime('%Y-%m-%d')
    data = index_classify("")
    show_func(data)
    # Tocsv(data,"","SW_index_check")
    try:
        data.to_sql('stock_temp', con=engine, if_exists='replace', index=False)
    except Exception as e:
        print(e)

        # INSERT
        # INTO
        # `sw_index`(`index_code`, `industry_name`, `level`, `industry_code`, `is_pub`, `parent_code`)
        # select
        # `index_code`, `industry_name`, `level`, `industry_code`, `is_pub`, `parent_code`
        # from stock_temp