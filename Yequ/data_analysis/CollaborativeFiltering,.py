#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 小雨对编号为638的用户格外关注，很想下次可以“投其所好”地为他推荐他会喜欢的书籍。
# 她决定利用这两天学到的基于用户的协同过滤算法，完成这一任务。
# 和课程中的思路类似，具体步骤如下：
# 1. 读取文件；
# 2. 构建数据透视表，并指定参与计算的最小数据量为5；
# 3. 计算用户间的相关系数；
# 4. 找出与编号638的用户最相似的用户；
# 5. 挑选可推荐书籍，推荐规则为：推荐和「用户638」最相似用户评分在8分以上，且「用户638」未看过的书籍；
# 6. 通过访问Index对象的.values属性，输出可推荐书籍的序列号。

import pandas as pd
# 1. 读取文件；
data = pd.read_csv("/Users/Mac/PycharmProjects/Stock-master/Yequ/data_analysis/practisedata/BookRates.csv")
# 2. 构建数据透视表，并指定参与计算的最小数据量为5；
id_socrt = data.pivot_table(index="ISBN",columns="user_id",values='rating')
corrMatrix = id_socrt.corr(method="pearson", min_periods=5)
# 4. 找出与编号638的用户最相似的用户；
userCorr = corrMatrix[638].drop(index=638)
# userCorr = corrMatrix[corrMatrix["user_id"]=="638"]
mostCorruser = userCorr.idxmax()
# 5. 挑选可推荐书籍，推荐规则为：推荐和「用户638」最相似用户评分在8分以上，且「用户638」未看过的书籍；
TargetBook = id_socrt[mostCorruser]
TargetBook=TargetBook[TargetBook.values>8]
user638readed = id_socrt[638].dropna()
Targebookname = TargetBook.index
Readedbookname = user638readed.index
# 6. 通过访问Index对象的.values属性，输出可推荐书籍的序列号。
TargeBookList = TargetBook[~Targebookname.isin(Readedbookname)]
print(TargeBookList.index.values)