import os, shutil
import re

from testException.BatchDecompression import BatchDecompression


# class Auto_Increment:
#     def __init__(self):
#         self.num = 0
#         self.target_file = None
#         self.target_pre_file = None
#     def get_add_one(self):
#         self.num += 1
#         return self.num
#
#     def set_target_file(self, file: str):
#         self.target_file = file
#
#     def set_target_pre_file(self,file : str):
#         self.target_pre_file = file
#
# def rename_to_new_dir(origin_path, target_path, re_file_name, signal, flag):
#     """
#     源目录下的文件拷贝或剪切到目标目录，并更换目标目录的文件名
#     :param origin_path: 源目录（精确到文件）
#     :param target_path: 目标目录（只到目录）
#     :param re_file_name: 新文件名名
#     :param signal: 信号，1. 为拷贝， 2. 为剪切
#     :param flag:目标目录文件已存在 增量为True,替换为False
#     :return:None
#     """
#     # old_path = os.path.join(settings['origin_path'], institution, file_name)
#     # new_path_parent = os.path.join(settings['not_matched'], date_str, dir_name)
#     if not os.path.exists(target_path):
#         os.makedirs(target_path, exist_ok=True),
#     new_path = os.path.join(target_path, re_file_name)
#     ai = Auto_Increment()
#     count = 0
#
#     if flag:
#         map_dict = dict()
#         while os.path.exists(new_path):
#             new_path = os.path.join(target_path, re_file_name.split('.')[0] + '(' + str(ai.get_add_one()) + ').' +re_file_name.split('.')[1])
#             map_dict[count] = new_path.split('\\')[-1]
#             count += 1
#
#         target_file = new_path.split('\\')[-1]
#         ai.set_target_file(str(target_file))
#         if count >= 2:
#             ai.set_target_pre_file(str(map_dict[count-2]))
#     else:
#         if os.path.exists(new_path):
#             os.remove(new_path)
#     if signal == 1:
#         shutil.copy(origin_path, new_path)
#     elif signal == 2:
#         os.rename(origin_path, new_path)
#     return ai


orgin_path = r'D:\Users\Administrator\AppData\Local\Programs\PycharmWorkSpace\Test\testException\origin'
target_path = r'D:\Users\Administrator\AppData\Local\Programs\PycharmWorkSpace\Test\testException\target'
# new_path = os.path.join(orgin_path,'已处理_8001001277帐单(盯市)20220325.TXT')
# old_path = os.path.join(orgin_path,'8001001277帐单(盯市)20220325.TXT')

# bd = BatchDecompression(orgin_path,orgin_path,['盯市'])
with open(os.path.join(orgin_path,'10310909账单(盯市).txt'),'r') as f:
    res_content = f.read()
    #print(res_content)
    #print(type(res_content))
    #regix = re.compile('对帐日期: (\d{4}[-/]?\d{2}[-/]?\d{2})')
    res = re.search(r'日期:.+(\d{4}[-/]?\d{2}[-/]?\d{2})',res_content).group(0)
    print(res.split(':')[1].strip())
    # res_list = res.split(':')
    # res_date = res_list[1].strip()
    # start_date = res_date.split('-')[0].strip()
    # end_date = res_date.split('-')[1].strip()
    # print(res_date)
    # print(start_date)
    # print(end_date)
    # for e in res_list:
    #     print(e)
    # print(type(res))
    # match_list = regix.findall(res_content, re.M)
    # for item in match_list:
    #     print(item)
#bd.batchExt()
# ai = rename_to_new_dir(os.path.join(target_path, '未处理_8001001277帐单(盯市)20220325.TXT'), target_path,
#                         '已处理_8001001277帐单(盯市)20220325.TXT', 2, False)
# print(ai.num)
# print(ai.target_file)
# print(ai.target_pre_file)
# rename_to_new_dir()
# os.rename(old_path,new_path)
# bd = BatchDecompression(orgin_path,target_path,['盯市'])
# bd.batchExt()
