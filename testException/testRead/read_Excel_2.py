# _*_ coding: utf-8 _*_
import pymysql.cursors, os, openpyxl, datetime
import pandas as pd
import re
from testException.utils.MysqlProxy import MysqlProxy
# 把招商托管估值表中五个字段的值导入进数据库
base_dir = r'D:\Users\Administrator\AppData\Local\Programs\PycharmWorkSpace\Test_Dev\testException\origin'
#file_name = '20220824_(XY6305)久铭专享23号私募证券投资基金_证券投资基金估值表.xls'
#file_name = 'SW8251_久铭6号私募证券投资基金_2022-08-26估值表.xls'
file_name = '估值表日报-STV732-静久康铭2号私募证券投资基金-4-20220901.xls'

#datestr,pro_code,pro_name = re.search(r'(\d+)_\W([A-Za-z0-9]+)\W(\w+)私募', file_name).groups()
#2022-08-29_SL0795_久铭稳健22号私募证券投资基金估值表.xlsx [国信]
#20220826_(XY6307)久铭专享21号私募证券投资基金_证券投资基金估值表.xls
# pro_code,pro_name,date_str = re.search(r'([A-Za-z0-9]+)_(\w+)证券\w+_\w+_(\d+)', file_name).groups()
# print(datestr,pro_code,pro_name)
# datestr, product_id, pro_name = re.search(r'(\d+)_\W([A-Za-z0-9]+)\W(\w+)私募',
#                                           file_name).groups()
#date_str,product = re.search(r'(\d+)_\w+_(\w+)私募',file_name).groups()
#product_id, product, date_tuoguan = re.search(r'([A-Za-z0-9]+)(\w+)私募[^\d]+(\d+-\d+-\d+)', file_name).groups()
pro_code, pro_name, date_str = re.search(r'\w-([A-Za-z0-9]+)-(\w+)私募.+-(\d{8})',file_name).groups()
print(pro_code,date_str)
#print(date_str,product)



data_frame = pd.read_excel(os.path.join(base_dir,file_name))


PRODUCT_CODE_NAME_MAP = {'SN0910':'久铭1号'}
# product_id, product, date_str = re.search(r'([A-Za-z0-9]+)(\w+)私募[^\d]+(\d+)', file_name).groups()
# product_code, product_name = product_id, PRODUCT_CODE_NAME_MAP[product_id]


resss = data_frame.index
int_tuple = resss.T.shape
print(int_tuple[0])
list_key_words = ['单位净值','实收资本','资产净值','资产合计','负债合计']
for row in range(int_tuple[0]):
    if data_frame.iloc[row,0] in list_key_words:
        if data_frame.iloc[row,0] != '单位净值':
            print(data_frame.iloc[row,9])
        else:
            print(data_frame.iloc[row,1])