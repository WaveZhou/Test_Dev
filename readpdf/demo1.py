# _*_ coding: utf-8 _*_
import pdfplumber

file = r'D:\Test\23003943-1124.pdf'

with pdfplumber.open(file) as pdf:
    print(pdf.pages)  # Page对象列表
    page = pdf.pages[0]
    print(page.extract_text())
    print(type(page.extract_text()))
    # for row in page.extract_table():
    #     print(row)
