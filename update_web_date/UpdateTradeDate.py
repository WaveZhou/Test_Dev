import pymysql
from WindPy import *

w.start();
a = w.tdays("2016-01-01","2024-01-01").Times;
b = 0


con = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test', charset='utf8')
cursor = con.cursor()  # 使用cursor()方法获取操作游标
cursor.execute("SELECT * FROM `trade_date`",None)
date_list = cursor.fetchall()
print(date_list)
if len(date_list) > 0:
    sql = 'DELETE FROM `trade_date`'
    cursor.execute(sql,None)
    con.commit()
for i in a:
    b = b + 1;
    sql = "INSERT INTO `trade_date` (`id`, `date`) VALUES ('%d', '%s');"%(b,i)
    cursor.execute(sql)
#info = cursor.fetchall()
    con.commit()
cursor.close()  # 关闭游标
con.close()  # 关闭数据库连接
