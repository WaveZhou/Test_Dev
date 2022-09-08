# _*_ coding: utf-8 _*_
import pymysql.cursors, os, openpyxl, datetime
import pandas as pd

from testException.utils.MysqlProxy import MysqlProxy

base_dir = r'D:\Users\Administrator\AppData\Local\Programs\PycharmWorkSpace\Test_Dev\testException\origin'

# df = pd.read_excel(os.path.join(base_dir, '210000420.xlsx'))
# df = pd.read_excel(os.path.join(base_dir,'机构信息表.xlsx'))
#
# data_code = df.iloc[0,0]
# data_ins = df.iloc[0,1]
# data_full = df.iloc[0,2]
store_list = list()
# temp = 0
# for i in range(40):
#     data_code = df.iloc[i,temp]
#     data_ins = df.iloc[i,temp+1]
#     data_full = df.iloc[i,temp+2]
#     temp = 0
#     store_list.append([data_code,data_ins,data_full])
# print(data_code,data_ins,data_full)
# mp = MysqlProxy()
# sql = 'INSERT INTO `institution_information`(`Ins_code`,`Ins_sim_name`,`Ins_full_name`) VALUES (%s,%s,%s)'
# mp.multiple_modify(sql,tuple(store_list))


df = pd.read_excel(os.path.join(base_dir, '产品科目体系信息(1).xlsx'))

Map_Collection = dict()
Map_Collection['否'] = None
Map_Collection['是'] = None
Map_Collection['久铭'] = 'JM'
Map_Collection['静久'] = 'JJ'
Map_Collection['无托管'] = 'JM'
Map_Collection['非托管'] = 'JM'
Map_Collection['招商证券'] = '021'
Map_Collection['国泰君安'] = '004'
Map_Collection['国君证券'] = '004'
Map_Collection['国信证券'] = '018'
Map_Collection['海通证券'] = '020'
Map_Collection['兴业证券'] = '022'
Map_Collection['华泰证券'] = '009'
Map_Collection['广发证券'] = '040'
Map_Collection['中信证券'] = '007'
Map_Collection['中泰证券'] = '008'
Map_Collection['安信证券'] = '003'
# Pro_full_name = df.iloc[0,0]
# Pro_sim_name = df.iloc[0,1]
# Pro_manage_code = Map_Collection[df.iloc[0,2]]
# Pro_code = df.iloc[0,3]
# Pro_trusteeship_code = df.iloc[0,4]
# if Pro_trusteeship_code == '无托管':
#     Pro_trusteeship_code = None
# Pro_mom_code = Map_Collection[df.iloc[0,5]]
#
# print(Pro_full_name,Pro_sim_name,Pro_manage_code,Pro_code,Pro_trusteeship_code,Pro_mom_code)
#
# Pro_full_name = df.iloc[1,0]
# Pro_sim_name = df.iloc[1,1]
# Pro_manage_code = Map_Collection[df.iloc[1,2]]
# Pro_code = df.iloc[1,3]
# Pro_trusteeship_code = df.iloc[1,4]
# if Pro_trusteeship_code == '无托管':
#     Pro_trusteeship_code = None
# Pro_mom_code = Map_Collection[df.iloc[1,5]]
# collection_2 = dict()
# collection_2['是'] = 1
# collection_2['否'] = 0
# store_list = list()
# # 更新pro_essential_factor产品基本信息表
# res_row = df.index
# int_tuple = res_row.T.shape
# for i in range(int_tuple[0]):
#     Pro_full_name = df.iloc[i, 0]
#     Pro_sim_name = df.iloc[i, 1]
#     Pro_manage_code = Map_Collection[df.iloc[i, 2]]
#     Pro_code = df.iloc[i, 3]
#     Pro_trusteeship_code = Map_Collection[df.iloc[i, 4]]
#     if Pro_trusteeship_code == '久铭':
#         Pro_trusteeship_code = 'JM'
#     Pro_mom_code = Map_Collection[df.iloc[i, 5]]
#     Liquidation = collection_2[df.iloc[i,6]]
#     store_list.append([Pro_code,Pro_sim_name,Pro_full_name,Pro_mom_code,Pro_trusteeship_code,Pro_manage_code,Liquidation])
# print(Pro_code,Pro_sim_name,Pro_full_name,Pro_mom_code,Pro_trusteeship_code,Pro_manage_code,Liquidation)
# mp = MysqlProxy()
# sql = 'INSERT INTO `pro_essential_factor`(`Pro_code`,`Pro_sim_name`,`Pro_full_name`,`Pro_mom_code`,`Pro_trusteeship_code`,`Pro_manage_code`,`Liquidation`) VALUES (%s,%s,%s,%s,%s,%s,%s)'
# mp.multiple_modify(sql,tuple(store_list))
#
# print(Pro_full_name,Pro_sim_name,Pro_manage_code,Pro_code,Pro_trusteeship_code,Pro_mom_code,Liquidation)


# 更新jm_subject_system久铭科目体系表
map_Subject = dict()
map_Subject['固定型科目'] = '01'
map_Subject['券商型科目'] = '02'
map_Subject['券商账户号型科目'] = '03'
map_Subject['证券代码型科目'] = '04'
map_Subject['自营产品型科目'] = '05'
map_Subject['机构证券代码型科目'] = '06'
for i in range(df.index.T.shape[0]):
    subject_code = df.iloc[i, 0]
    subject_name = df.iloc[i, 1]
    subject_level = df.iloc[i, 2]
    subject_type = map_Subject[df.iloc[i, 3]]
    is_leaf_subject = df.iloc[i, 4]
    store_list.append([subject_code, subject_name, subject_level, subject_type, is_leaf_subject])

mp = MysqlProxy()
sql = 'INSERT INTO `jm_subject_system`(`Subject_code`,`Subject_name`,`Subject_level`,`Subject_type`,`Is_leaf_subject`) VALUES (%s,%s,%s,%s,%s)'
mp.multiple_modify(sql, tuple(store_list))

# str = '905-客户-期权客户对账单2018.xls'
# str = '融资融券对帐单2018.xls'
# res = str.split('.')[0][:-4]
# print(res)
# ata = df.iloc[0,0]
# for i in range(21):
#     data = df.iloc[0, i]
#     print(data)
#     print('读取指定行数据：\n{0}'.format(data))
# data = df.iloc[2,1]
# print(data)
# 帐单日期::: 2018年2月13日 -- 2018年12月31日
# print('读取指定行数据：\n{0}'.format(data))
# start_date_origin_str = str(data).split('--')[0].strip()
# import datetime
# start_date_str = datetime.datetime.strptime(start_date_origin_str,'%Y年%m月%d日').strftime('%Y-%m-%d')
# print(start_date_str)
# end_date_origin_str = str(data).split('--')[1].strip()
# end_date_origin = datetime.datetime.strptime(end_date_origin_str,'%Y年%m月%d日').strftime('%Y-%m-%d')


# print(type(data))
# res_str_date = datetime.datetime.strftime(data,'%Y-%m-%d')
# print(res_str_date)
# print(type(res_str_date))
# begin_date = str(data).split(":")[1].split('--')[0].strip()#两个杠，英文的冒号
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
