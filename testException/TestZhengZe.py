# _*_ coding: utf-8 _*_
import re
#respons = re.match(r'^[0-9]*$','30天多少个1字')
#respons = re.findall('\d+','30天多少个1字')#返回数字字符串的数组
mo = r'[\u4e00-\u9fa5]*'  #=============>>匹配的是字符串首位出现的汉字字符串
mo2= r'[\u4E00-\u9FA5]+'   #=============>>匹配整个字符串中第一次出现的汉字字符串
res = re.search(mo2, 'fsdff汉字hfhe中国')
print(res)  # <re.Match object; span=(0, 2), match='我是'>