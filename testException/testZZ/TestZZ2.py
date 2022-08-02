# _*_ coding: utf-8 _*_
import re

# data = """我始终！@@##73278fgh¥%…………&alkjdfsb1234
# 566667是中国人woaldsfkjzlkcjxv123*())<>
# """
#
#
# print(                               )
# #这个search后面带了+号，能全局匹配（因为是search）到第一个出现的中文字符串，换成；另外，没带加好，则只能匹配一个汉字
# # findall匹配到所有汉字，并返回到数组中
# #match则只能匹配一开始就是中文字符串的（一开始不是中文字符串就返回none）
#
#
# # 匹配所有单字符，英文，数字，特殊符号
# print(re.search('[\x00-\xff]+', data).group(0))
#
# # 匹配所有非单字符，入汉字和省略号
# print(re.findall('[^\x00-\xff]', data))
list = list()
list.append(1)
# list.append(2)
# list.append(3)
# count = 0
# for x in list:
#     count+=1
#     if count == len(list):
#         print(x)

str = 'gsgsgs  gsgsg  ffsdsg '
res = str.replace(" ","")
print(res)
print(str)