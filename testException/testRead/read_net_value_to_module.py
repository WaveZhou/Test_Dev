import openpyxl,os

base_dir = r'D:\Users\Administrator\AppData\Local\Programs\PycharmWorkSpace\Test_Dev\testException\origin'
#file = os.path.join(base_dir,'��Ʒ��ֵ����ģ��-20220909120107.xlsx')
work_book_obj = openpyxl.load_workbook(filename='��Ʒ��ֵ����ģ��-20220909120107.xls')
sheet = work_book_obj.sheetnames[0]
print(sheet)
# with open('��Ʒ��ֵ����ģ��-20220909120107.xlsx','r',encoding= 'charmap') as csvfile:
#     print(csvfile)
wb = openpyxl.Workbook()
# sheet = wb.active
# sheet.title = 'δ�����˵��˻���Ϣ'
# sheet['A1'] = '��Ʒ����'
# sheet['B1'] = 'ȯ��'
# sheet['C1'] = '�˻�����'
# sheet['D1'] = '�˻���'
# sheet['E1'] = '�Ϻ�����'
# sheet['F1'] = '���ڿ���'
# sheet['G1'] = '��������'
# sheet['H1'] = '����Ӫҵ��'
# sheet['I1'] = '��ϵ��'
# sheet['J1'] = '����'
# sheet['K1'] = '�ֻ�'
# sheet['L1'] = '�绰'
# sheet['M1'] = '΢��'