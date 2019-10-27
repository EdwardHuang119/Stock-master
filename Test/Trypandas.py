# -*- coding: utf-8 -*-
from abupy import ABuSymbolPd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

tsla_df=ABuSymbolPd.make_kl_df('usTSLA',n_folds=2)
# tsla_df.tail()
# tsla_df[['close','volume']].plot(subplots=True,style=['r','g'],grid=True)
# plt.show()
# print(tsla_df.info())
# print(tsla_df.describe())

# print(tsla_df.loc['2016-11-01':'2017-04-02'])
# print(tsla_df.loc['2016-11-01':'2017-04-02','close':'open'])
# print(tsla_df[['close','low','p_change']][33:95])
# print(tsla_df.tail())

# [((np.abs(tsla_df.netChangeRatio)>8）&(tsla_df.volume>2.5*tsla_df.volume.mean())]

# print(tsla_df[['close','low','p_change']][(np.abs(tsla_df.p_change)>8)&(tsla_df.volume>2.5*tsla_df.volume.mean())])
# print(tsla_df[['close','low','p_change']][(tsla_df.p_change)>8&(tsla_df.volume>2.5*tsla_df.volume.mean())])
print(tsla_df.sort_index(by='p_change',ascending=True)[:5])