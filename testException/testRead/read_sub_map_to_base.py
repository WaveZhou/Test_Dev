# _*_ coding: utf-8 _*_
import pandas as pd
import os

from utils.MysqlProxy import MysqlProxy

if __name__ == '__main__':
    base_dir = r'D:\Users\Administrator\AppData\Local\Programs\PycharmWorkSpace\Test_Dev\testException\origin'
    file_name = '科目映射关系.xlsx'
    mp = MysqlProxy()
    # pd.ExcelFile()
    # data_frame = pd.read_excel(os.path.join(base_dir, file_name))
    xl = pd.ExcelFile(os.path.join(base_dir, file_name))
    for name in xl.sheet_names:
        df = pd.read_excel(xl, name)
    # print(data_frame)
    #     columes = df.shape[1]
    #     rows = df.shape[0]
        #rows2 = df.index.T.shape[1]
        # print(columes)
        # print(rows)
        # for i in range(8):
        rows_int = df.index.T.shape[0]
        sql_get_ins_code = "SELECT `Ins_code` FROM `institution_information` WHERE `Ins_sim_name`=%s "
        sel_get_map_type_value = "SELECT `ParaValue` FROM `sys_para` WHERE ParaType='Map_Type' AND `ParaKey`=%s "
        sql_get_jss_id = "SELECT `Id` FROM `jm_subject_system` WHERE `Subject_code`=%s"

        store_list = list()
        count = 0
        for row in range(rows_int):
            count += 1
            number = df.iloc[row,-1]
            ins_sim_name = df.iloc[row,1]
            subject_code = df.iloc[row,0]
            print(name,subject_code,count)
            map_type_key = df.iloc[row,2]
            map_jm_subject_code = df.iloc[row,3] if not df.isnull().iloc[row,3] else None
            # 准备去获取code
            ins_code = mp.get_one(sql_get_ins_code,[ins_sim_name])['Ins_code']
            try:
                map_type_code = mp.get_one(sel_get_map_type_value,[map_type_key])['ParaValue']
            except TypeError:
                print(name,ins_sim_name,subject_code)
                raise Exception
            TEMP = mp.get_one(sql_get_jss_id,[map_jm_subject_code])
            jss_id = mp.get_one(sql_get_jss_id,[map_jm_subject_code])['Id'] if mp.get_one(sql_get_jss_id,[map_jm_subject_code]) is not None else None
            store_list.append([ins_code,subject_code,map_type_code,jss_id])
        sql_insert_pro_subject_map = "INSERT INTO `pro_subject_map` (`Ins_code`,`Ins_sub_code`,`Map_type`,`Map_jss_id`) VALUES (%s,%s,%s,%s)"
        mp.multiple_modify(sql_insert_pro_subject_map,tuple(store_list))
        if name == '中信证券':
            break
    mp.close()
    print("okk")