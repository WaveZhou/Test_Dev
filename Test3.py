# _*_ coding: utf-8 _*_
import re,datetime


# str2 = 'XY0886_久铭7号私募证券投资基金_2022-03-01估值表.xls'
#
# #re.search(r'([A-Za-z0-9]+)_久铭(\w+)私募[^\d]+(\d+)', file_name).groups()
#
#
# #str = '估值表日报-STV732-静久康铭2号私募证券投资基金-4-20220223.xlsx'
# code, name,date= re.search(r'([A-Za-z0-9]+)_(\w+)私募\w+_(\d+-\d+-\d+)',str2).groups()
# date = "".join(str(date).split('-'))
# date = datetime.datetime.strptime(date,'%Y%m%d')
# print(code,name,date)
# print(type(date))
# x = 5
# def fun():
#     a = 3
#     global x
#     x+=a
#     return x
# print(fun())
# print(x)
date = '2020/03/29'
str=''
if '/' in date:
    res = date.split('/')
    str = str.join(res)
    print(str)
    print('true')
# dict_list = [{},{}]
# print(len(dict_list))