import os,datetime
#subject = '0011000048久铭专享6号20220217.txt'
# '上海久铭投资管理有限公司－久铭1号私募证券投资基金_661026000005_股票期权对账单(人民币)_20220217.xls上海久铭投资管理有限公司－久铭1号私募证券投资基金_661026000005_股票期权对账单(人民币)_20220217.xls'
# '上海久铭投资管理有限公司－久铭专享16号私募证券投资基金-融资融券账户对账单-8009243503_2022-03-03.xlsx'
# orgin_path = r'D:\Users\Administrator\AppData\Local\Programs\PycharmWorkSpace\Test\testException\origin\未匹配_Statement_106560--HKD--EQ_20211220.xlsx'
# res = os.sep
# data_dir = os.sep.join(['hello', 'world'])
# res = orgin_path.split('\\')[-1]
# if not res.startswith('已处理'):
#     print('突然')
# time = datetime.datetime.now()
# print(time)

str = '未匹配_Statement_106560--HKD--EQ_20211220.xlsx'
from Check_Bill_Test.utils.Transform_FileName import Transform_FileName
tf = Transform_FileName()
res = tf.get_date(str)
print(res)