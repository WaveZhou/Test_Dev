# _*_ coding: utf-8 _*_
import pymysql.cursors, os, openpyxl, datetime
import pandas as pd

base_dir = r'D:\Users\Administrator\AppData\Local\Programs\PycharmWorkSpace\Test\testException\origin'

df = pd.read_excel(os.path.join(base_dir, '210000420.xlsx'))
#str = '905-客户-期权客户对账单2018.xls'
# str = '融资融券对帐单2018.xls'
# res = str.split('.')[0][:-4]
# print(res)
#ata = df.iloc[0,0]
# for i in range(21):
#     data = df.iloc[0, i]
#     print(data)
#     print('读取指定行数据：\n{0}'.format(data))
data = df.iloc[2,1]
# print(data)
#帐单日期::: 2018年2月13日 -- 2018年12月31日
print('读取指定行数据：\n{0}'.format(data))
start_date_origin_str = str(data).split('--')[0].strip()
import datetime
start_date_str = datetime.datetime.strptime(start_date_origin_str,'%Y年%m月%d日').strftime('%Y-%m-%d')
print(start_date_str)
end_date_origin_str = str(data).split('--')[1].strip()
end_date_origin = datetime.datetime.strptime(end_date_origin_str,'%Y年%m月%d日').strftime('%Y-%m-%d')


# print(type(data))
# res_str_date = datetime.datetime.strftime(data,'%Y-%m-%d')
# print(res_str_date)
# print(type(res_str_date))
#begin_date = str(data).split(":")[1].split('--')[0].strip()#两个杠，英文的冒号
# date_obj = datetime.datetime.strptime(begin_date,"%Y年%m月%d日").date()
# str_date = date_obj.strftime('%Y-%m-%d')
# print(type(str_date))
# print(str_date)
# # print()
# print(date_obj)
# end_date = str(data).split("：")[1].split('-')[1]
# print(begin_date)

# print(end_date)
# for i in range(21):
#     if i < 15:
#         data = df.iloc[1, i]
#         print(data)
#         print('读取指定行数据：\n{0}'.format(data))
#         continue
#     else:
#         data = df.iloc[1, i]
#         print(data)
#         print('读取指定行数据：\n{0}'.format(data))
# str(data).split('-')[0].strip()
# res = ''.join(filter(str.isdigit,data))
# print(type(data))
# # str_date = str(data).split('.')[0]
#
# #print(type(str_date))
# print('读取指定行数据：\n{0}'.format(data))

# with open(os.path.join(base_dir,'06005-期权客户对账单0537536302 (139).xlsx'), "r") as f:  # 打开文件
#     data = f.read()  # 读取文件
#     print(data)
