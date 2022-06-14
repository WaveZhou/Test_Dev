# _*_ coding: utf-8 _*_
import re
# # import shutil,os
# # origin = 'D:\\Test\\origin\\demo1.txt'
# # target = 'D:\\Test\\target'
# #
# # shutil.move(origin,target)
# # os.makedirs(origin,exist_ok=True)
# mo = r'[\u4e00-\u9fa5]*'#第一个位置出现的为中文字符串才匹配
# s = '我哈哈d235grg更改'
# result = re.search(mo,s)
# print(result)
from zipfile import ZipFile

from Check_Bill_Test.utils.BatchDecompression import BatchDecompression

bd = BatchDecompression(r'./yasuo/',r'./yasuo/',['盯市'])
bd.batchExt()
#name.encode('cp437').decode('gbk')
# def support_gbk(zip_file: ZipFile):
#     name_to_info = zip_file.NameToInfo
#     # copy map first
#     for name, info in name_to_info.copy().items():
#         real_name = name
#         if real_name != name:
#             info.filename = real_name
#             del name_to_info[name]
#             name_to_info[real_name] = info
#     return zip_file
#
#
# with support_gbk(ZipFile(r'./yasuo/久铭对账单20220331.zip')) as zfp:
#     zfp.extractall(r'./yasuo/')

