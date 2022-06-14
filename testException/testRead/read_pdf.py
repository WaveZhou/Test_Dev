# _*_ coding: utf-8 _*_
import pdfplumber
import re
#file = r'D:\Test\160083361.pdf'
base_dir = r'D:\Users\Administrator\AppData\Local\Programs\PycharmWorkSpace\Test\testException\origin\23003943-0210.pdf'
with pdfplumber.open(base_dir) as pdf:
    print(pdf.pages)  # Page对象列表
    page = pdf.pages[0]
    print(page.extract_text())
    print(type(page.extract_text()))
    #Date : 2021-12-29
    #res = re.search(r'Date.*:.*(\d{4}[-/]?\d{2}[-/]?\d{2})', page.extract_text()).group(0).split(':')[1].strip()
    res = re.search(r': 1 :(\d{4}[-/]?\d{2}[-/]?\d{2})',page.extract_text()).group(0)[-8:-4]
    print(res)
    # res = re.search(r'\d{4}[-/]+\d{2}[-/]+\d{2}',page.extract_text()).group(0)
    # res_year = res.split('-')[0]
    # print(res_year)
    #print(type(page.extract_text()))
    # for row in page.extract_table():
    #     print(row)
