import os
import re


orgin_path = r'D:\Users\Administrator\AppData\Local\Programs\PycharmWorkSpace\Test_Dev\testException\load_path'
#target_path = r'D:\Users\Administrator\AppData\Local\Programs\PycharmWorkSpace\Test\testException\target'
# new_path = os.path.join(orgin_path,'已处理_8001001277帐单(盯市)20220325.TXT')
# old_path = os.path.join(orgin_path,'8001001277帐单(盯市)20220325.TXT')


with open(os.path.join(orgin_path,'550825.txt'),'r') as f:
    res_content = f.read()
    #print(res_content)
    #print(type(res_content))
    #日期 Date：20220722
    #日期 Date:20220718
    #regix = re.compile('对帐日期: (\d{4}[-/]?\d{2}[-/]?\d{2})')#日  期:20160921-20181028
    #res = re.search(r'日  期:.*(\d{4}[-/]?\d{2}[-/]?\d{2})',res_content).group(0)

    res = re.search(r'日期 Date:.*(\d{4}[-/]?\d{2}[-/]?\d{2})',res_content).group(0)
    begin_date = res.split(':')[1].split('-')[0].strip()
    end_date = res.split(':')[1].split('-')[1].strip()
    res_date = res.split("：")[1]
    print(res_date)
    import datetime
#
#     begin_date_str = str(datetime.datetime.date(datetime.datetime.strptime(begin_date, '%Y%m%d')))
#     print(begin_date_str)
#     print('开始日期:',end=begin_date_str)
#     end_date_str = str(datetime.datetime.date(datetime.datetime.strptime(end_date, '%Y%m%d')))
#     print('结束日期:', end=end_date_str)
    #print(res.split(':')[1].strip().split('-')[0])

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
