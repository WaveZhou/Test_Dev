# _*_ coding: utf-8 _*_
import pdfplumber
import re

# file = r'D:\Test\160083361.pdf'
# cd203cffe8524069b3e2136833a47d432022061320220619.pdf
# D:\Users\Administrator\AppData\Local\Programs\PycharmWorkSpace\Test_Dev\testException\load_path
base_dir = r'D:\Users\Administrator\AppData\Local\Programs\PycharmWorkSpace\Test_Dev\testException\load_path\cd203cffe8524069b3e2136833a47d432022061320220619.pdf'

# from Check_Bill_Test.utils.Transform_FileName import Transform_FileName
# tf = Transform_FileName()
# res = tf.get_filename_without_date('cd203cffe8524069b3e2136833a47d432022061320220619.pdf')
# print(res)
with pdfplumber.open(base_dir) as pdf:
    print(pdf.pages)  # Page对象列表
    page = pdf.pages[0]
    print(page.extract_text())
    print(type(page.extract_text()))
    # Date : 2021-12-29
    # res = re.search(r'Date.*:.*(\d{4}[-/]?\d{2}[-/]?\d{2})', page.extract_text()).group(0).split(':')[1].strip()
    res = re.search(r': 1 :(\d{4}[-/]?\d{2}[-/]?\d{2})', page.extract_text()).group(0)[-8:-4]
    print(res)
    # res = re.search(r'\d{4}[-/]+\d{2}[-/]+\d{2}',page.extract_text()).group(0)
    # res_year = res.split('-')[0]
    # print(res_year)
    # print(type(page.extract_text()))
    # for row in page.extract_table():
    #     print(row)
