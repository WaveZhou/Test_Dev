# _*_ coding: utf-8 _*_
import re,datetime
# line = "result of fold 0, instance 3.";
#
#
# pattern = r'w*.[a-z]{5}.[a-z]*'
# prog = re.compile(pattern)
# string = 'www.baidu.com'
# result = prog.match(string)
#
# #print(pattern.group(0))
# print(result)
from Check_Bill_Test.utils.Transform_FileName import Transform_FileName

# date  = datetime.datetime.now()
# str = datetime.datetime.strftime(date,'%Y')
# print(type(str))
# print(str[-2:])
str = '905-客户-股票期权客户对账单20220301-0331.xls'

res = re.search( '\d{8}-\d{4}',str).group(0)
begin_date = res[4:8]
print(begin_date)
result = re.sub( res,'',str)

print(res)
print(result)
print(str.split('.')[0])
tf = Transform_FileName()
date = tf.get_date('905-客户-股票期权客户对账单20220301-0331.xls')
print(date)
# str = 'pipeimobancharset=UTF-8 ,charset= GBK'
# print(re.search(r'charset=(.+)',str).group(1))



# charset = 'charset='
# if str.__contains__(charset):
#     print('zhaodaoole')
# if -1:
#     print("666666666")
# def called():
#     print("aaa")
#     for i in range(10):
#         print(i)
#         if i == 2:
#             #pass
#             #raise Exception("2异常")
#             return "2字符串"
#         if i == 3:
#             continue
#         print(i)
#
#
# try:
#     result = called()
#     print(result)
# except Exception as result:
#     print(result)
# print("666")