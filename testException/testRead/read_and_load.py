import re,datetime

import pymysql.cursors,os
# v1.0.0及以上
from pymysql.converters import escape_string

# 连接数据库
# connect = pymysql.Connect(
#     host='localhost',
#     port=3306,
#     user='root',
#     passwd='123456',
#     db='jm_statement',
#     charset='utf8'
# )
#
# # 获取游标
# cursor = connect.cursor()
base_dir = r'D:\Users\Administrator\AppData\Local\Programs\PycharmWorkSpace\Test\testException\origin'
#日       期:20220329
#对帐期间：2021年12月17日---2021年12月17日
#对账起止日期： 2021年12月17日 - 2021年12月17日
with open(os.path.join(base_dir,'99148740-1217.TXT'), "r") as f:  # 打开文件
    res_content = f.read()
    #print(res_content)
    #res = re.search(r'日.*期.*:.*(\d{4}[-/]?\d{2}[-/]?\d{2})', res_content).group(0)
    res_date_str = re.search(r'对账起止日期：.*(.*)',res_content).group(0)
    begin_date_str = res_date_str.split('：')[1].strip().split('-')[0].strip()
    res_date_str = res_date_str.split('：')[1].strip().split('-')[1].strip()
    begin_date = datetime.datetime.strptime(begin_date_str,'%Y年%m月%d日').strftime('%Y-%m-%d')
    res_date = datetime.datetime.strptime(res_date_str,'%Y年%m月%d日').strftime('%Y-%m-%d')
    print(type(begin_date))
    print(begin_date,res_date)


    # res_date = res.split(':')[1].strip()
    # print(res_date)
    # res_date_str = res.split(':')[1].strip()
    # start_date = res_date_str.split('-')[0].strip()
    # end_date = res_date_str.split('-')[1].strip()
    # print(start_date,end=':')
    # print(end_date)
    # str__value_key_r = data.split('{')[1]
    # str__value_key_l = str__value_key_r.split('}')[0]
    # print(str__value_key_l)
    # key_value_str_array = str__value_key_l.split(',')
    # for k_v in key_value_str_array:
    #    value = k_v.split(':')[0]
    #    value = eval(value)
    #    key = k_v.split(':')[1]
    #    sql = "INSERT INTO jm_statement.suppose_arrive (account_id, account_number,valid_status) VALUES ( '%s', '%s', '%s' )"
    #    data = (key,value,1)
    #    cursor.execute(sql % data)
    #    connect.commit()




# 插入数据
# sql = "INSERT INTO jm_statement.suppose_arrive (account_id, account_number,valid_status) VALUES ( '%s', '%s', '%s' )"
# data = ('一级科员', '法律类', '大学本科以上','郑州市')
# cursor.execute(sql % data)
# connect.commit()
# print('成功插入', cursor.rowcount, '条数据')