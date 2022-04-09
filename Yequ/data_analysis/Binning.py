#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 本章节学习和使用数据分箱子的做法

# 题目要求
# 欧欧是品牌旗舰店SW的销售主管，临近年末，她想要通过构造RFM模型，观察用户标记分层的结果，有针对性地精细化运营，冲刺业绩。
#
# 构造的第一步，定义三个标准：
# R代表最近一次购买距今多少天
# F代表购买了多少次
# M代表购买总金额
# 请利用所学内容，帮助欧欧完成RFM模型的构造并可视化结果。
# 具体要求如下：
# 1. 导入模块，读取文件"/Users/RFM/RFM.xlsx"
# 2. R值获取：
# (1) 按"买家昵称"分组，选出"付款日期"的最大值并还原索引
# (2) 将截止时间2020年10月1日转换成时间类型
# (3) 计算截止日期与"付款日期"这列值的差，用.dt取到数据，再用.days属性将天数提取出来，得到R
# 3. F值获取:
# (1) 按"买家昵称"分组，再按照"付款日期"计数并还原索引
# (2) 重命名所有columns的名称为"买家昵称","F"
# 4. M值获取：
# (1) 按"买家昵称"分组，再按照"实付金额"求和并还原索引
# (2) 重命名所有columns的名称为"买家昵称","M"
# 5. 两两联合：分别联合"R"、"F"、"M"三列所在的DataFrame
# 6. 使用qcut()函数：
# 将"R"这列的数据分箱，均分为2组，区间标记命名为1-0分
# 将"F"这列的数据按照0、1、16分箱，，区间标记命名为0-1分
# 将"M"这列的数据分箱，均分为2组，区间标记命名为0-1分
# 7. 将数据分箱之后的三列使用astype()函数转化为字符串格式并用"+"把字符串拼接在一起，组成一个新的列
# 8. 定义一个函数，将"111", "110"这样的值，转化为对应的用户分层，对应关系如图：
# 9. 对新生成的列，使用apply()函数，调用定义的函数，再按照"人群类型"进行分类
# 10. 使用count()函数进行聚合，得到最终结果并打印输出
# 11. 导入matplotlib.pyplot模块并设置中文字体"Arial Unicode MS"
# 12. 使用plt.bar()函数，以最终结果的index为横坐标, 最终结果的values为纵坐标进行展示，调整子图布局，显示图像

# 导入pandas模块
import pandas as pd
# 读取文件，赋值给df
df = pd.read_excel("/Users/Mac/PycharmProjects/Stock-master/Yequ/data_analysis/practisedata/RFM.xlsx")

# R值获取：每个用户最后一次购买时间距今多少天
# TODO 使用groupby()函数，按"买家昵称"分组，再选取"付款日期"的最大值，赋值给r
r = df["付款日期"].groupby(df["买家昵称"]).max()

# TODO 使用reset_index()函数还原r的索引再次赋值给r
r =r.reset_index()
# TODO 使用to_datetime()函数，将截止时间2020年10月1日转换成时间类型，赋值给endTime
endTime = pd.to_datetime("2020-10-1")
# TODO 计算endTime和"付款日期"这一列的值的差，
# 用.dt取到数据，再用.days属性将天数提取出来，赋值给r["R"]
r["R"] = (endTime-r["付款日期"]).dt.days

# F值获取:每个用户累计购买频次
# TODO 使用groupby()函数，按"买家昵称"分组，再按照"付款日期"计数，赋值给f
f =df["付款日期"].groupby(df["买家昵称"]).count()
# TODO 使用reset_index()函数还原f的索引再次赋值给f
f = f.reset_index()
# TODO 修改f所有列索引名称为"买家昵称","F"
f.columns = ["买家昵称","F"]



# M值获取:每个用户总金额
# TODO 使用groupby()函数，按"买家昵称"分组，再按照"实付金额"求和，赋值给m
m = df["实付金额"].groupby(df["买家昵称"]).sum()
# 使用reset_index()函数还原m的索引再次赋值给m
m = m.reset_index()
# TODO 重命名m中所有columns的名称为"买家昵称","M"
m.columns = ["买家昵称","M"]

# TODO 使用pd.merge()函数联合r和f，赋值给rf
rf = pd.merge(r,f)
# TODO 使用pd.merge()函数联合rf和m，赋值给rfm
rfm = pd.merge(rf,m)

# TODO 对rfm使用qcut()函数，将"R"这列的数据分箱，均分为2组，区间标记命名为1-0分，赋值给"R-SCORE"这列
rfm["R-SCORE"] = pd.qcut(rfm["R"],q=2,labels=[1,0])
rfm["R-SCORE"] = pd.qcut(rfm["R"],q=2,labels=[1,0])
# TODO 对rfm使用cut()函数，将"F"这列的数据按0、1、16分箱，区间标记命名为0-1分，赋值给"F-SCORE"这列
rfm["F-SCORE"] = pd.cut(rfm["F"],[0,1,16],labels = [0,1])
# TODO 对rfm使用qcut()函数，将"M"这列的数据分箱，均分为2组，区间标记命名为0-1分，赋值给"M-SCORE"这列
rfm["M-SCORE"] = pd.qcut(rfm["M"],q=2,labels= [0,1])

# 对rfm中"R-SCORE"、"F-SCORE"、"M-SCORE"这三列，使用astype()函数转化为字符串格式
# 用"+"把字符串拼接在一起，组成一个新的列"mark"
rfm["mark"] = rfm["R-SCORE"].astype(str) + rfm["F-SCORE"].astype(str) + rfm["M-SCORE"].astype(str)

# 定义一个函数rfmType，将"111", "110"这样的值，转化为对应的用户分层
def rfmType(x):
    if x == "111":
        return "高价值用户"
    elif x == "101":
        return "重点发展用户"
    elif x == "011":
        return "重点唤回用户"
    elif x == "001":
        return "重点潜力用户"
    elif x == "110":
        return "一般潜力用户"
    elif x == "100":
        return "一般发展用户"
    elif x == "010":
        return "一般维系用户"
    else:
        return "低价值用户"

# 对rfm中"mark"这列，使用apply()函数，调用rfmType函数，赋值给"人群类型"
rfm["人群类型"] = rfm["mark"].apply(rfmType)

# 使用groupby()函数，对rfm["人群类型"]按照"人群类型"进行分类
# 然后使用count()函数进行聚合，赋值给变量df_type
df_type = rfm["人群类型"].groupby(rfm["人群类型"]).count()

# 输出df_type
print(df_type)

# 导入matplotlib.pyplot模块
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams["font.sans-serif"] = "Arial Unicode MS"
# TODO 使用plt.bar()函数，以df_type.index为横坐标, df_type.values为纵坐标，对df_type进行展示
plt.bar(df_type.index,df_type.values)

# 使用plt.tight_layout()函数来调整子图布局
plt.tight_layout()
# 使用plt.show()函数显示图像
plt.show()