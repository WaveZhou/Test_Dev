# _*_ coding: utf-8 _*_
from Check_Bill_Test.Institution.impl.DongBei import DongBei


class A:
    def __init__(self):
        print('hh')

    def speak(self):
        print('woqu')
class B(A):
    def run(self):
        print('paoqilao')
# origin_dir = 'D:\估值专用邮箱数据\邮件账户分类缓存\收件日20220228 当天'
# tf = Transform_FileName()
# count = 0
# # for item in os.listdir(origin_dir):
# #     if os.path.isdir(os.path.join(origin_dir,item)):
# #         if tf.get_date(item) != '':
# #             for obj in os.listdir(os.path.join(origin_dir,item)):
# #                 if obj in os.listdir(origin_dir):
# #                     for file in os.listdir(os.path.join(origin_dir,item,obj)):
# #                         print(file)
# #                         count = count + 1
# #                         #shutil.move(os.path.join(origin_dir,item,obj,file),os.path.join(origin_dir,obj))
# #                         #print(obj)
# #                     #print(obj)
# # print(count)
# str = '21800108'
# res = str[0:4]
# print(res)
# xy = XingYe()
# xy.load_file_content_for_date('兴业','普通')
# DongBei
institution_impl = locals()['DongBei']('东北', '普通')
print(institution_impl)
# str = '国投安信期货账户'
# belong = str[0:2]
# type = str[-4:-2]
# print(belong)
# print(type)
# b = locals()['B']()
# b.speak()
# name_dict = {'zhangsan':'张三','lisi':'李四'}
# res = name_dict['zhangsan']
# print(res)
# str = '我里乖乖'
# res = str[-2:]
# print(res)
# shutil.move(os.path.join(os.path.join(origin_dir,item),obj),os.path.join(origin_dir))
# for item in os.listdir(origin_dir):
#     if os.path.isdir(os.path.join(origin_dir,item)):
#         print(item)
# os.path.join()
