# -*- coding: utf-8 -*-

tuple1 = ("日期1", '分类账户1')
file_name1 = '甲'

tuple2 = ("日期2", '分类账户2')
file_name2 = '已'

dict = dict()
dict[file_name1] = tuple1
dict[file_name2] = tuple2

for filename, tuple in dict.items():
    print(filename, end="==========")
    print(tuple)


# class Person(object):
#     def __init__(self):
#         print("自动走这个方法")
#         self.age = '11'
#         print(self.age)
#
#     def change(self):
#         self.age = 26


