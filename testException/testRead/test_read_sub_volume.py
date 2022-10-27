# _*_ coding: utf-8 _*_
import pymysql.cursors, os, openpyxl, datetime
import pandas as pd
import re

from Constants import Subject_Map_Type
from testException.utils.MysqlProxy import MysqlProxy
from Check_Bill_Test.utils.Log_Record import Log

# store_words_map_list = dict()
mp = MysqlProxy()
# wait_to_insert_list = list()
Currency, Exchange_rate, Quantity, Unit_cost, Cost_currency, Cost_proportion, Quotation, Market_currency_value, Market_value_proportion, Valuation_appreciation, Suspension_information, Equity_information = None, None, None, None, None, None, None, None, None, None, None, None

logger = Log('Not_Mapped_Subject')


class Load_Valuation_table(object):
    def __init__(self, path, file, pro_id, value_date,trusteeship):
        self.sys_para = Subject_Map_Type
        self.path = path
        self.file = file
        self.pro_id = pro_id
        self.value_date = value_date
        self.wait_to_insert_list = list()
        self.trusteeship = trusteeship
        self.mp = MysqlProxy()

    def get_all_match_info(self, pro_id, gz_sub_name, map_type, subject_type=None):
        global ins_pro_info
        if map_type in ['02', '03', '04', '05']:
            sql_get_ins_pro_name = """
                                   SELECT
                                   ins.Ins_sim_name,
                                   pf.Pro_sim_name 
                                   FROM
                                       `pro_essential_factor` pf
                                       LEFT JOIN `institution_information` ins ON pf.Pro_trusteeship_code = ins.Ins_code 
                                   WHERE
                                   pf.Pro_code = %s
                                   """
            ins_pro_info = self.mp.get_one(sql_get_ins_pro_name, [pro_id])
        if map_type == self.sys_para.Map_type['普通账户类科目映射关系']:
            #  要替换掉 sub_code 中的机构代码.账户号  和    sub_name的机构简称_账户号
            ins_simple_name = str(gz_sub_name).split('_')[-1]

            sql_get_ins_and_acc = """
                SELECT
                ins.`Ins_code`,
                ins.`Ins_sim_name`,
                ai.`account` 
                FROM
                `account_information` ai
                LEFT JOIN `institution_information` ins ON ai.ins_code = ins.Ins_code 
                WHERE
                ai.pro_code = %s
                AND ins.Ins_sim_name LIKE %s
                AND ai.type_code = '01'
                AND ai.`status` IN ('1','3')
                """

            if self.pro_id in ['SJU632']:
                ins_account_info_list = self.mp.get_list(sql_get_ins_and_acc,[pro_id, str(ins_simple_name) + '%%'])
            else:
                ins_account_info_list = self.mp.get_list(sql_get_ins_and_acc, [pro_id, str(ins_simple_name)[0:2] + '%%'])

            if len(ins_account_info_list) == 1:
                res_ins_code = ins_account_info_list[0]['Ins_code']
                res_account = ins_account_info_list[0]['account']
                ins_sim_name = ins_account_info_list[0]['Ins_sim_name']
                return [res_ins_code, ins_sim_name, res_account]
            elif len(ins_account_info_list) < 1:
                raise RuntimeError("{}这天的托管机构{}的{}估值表上存在产品账户信息表中未收录的普通账户,科目名称为{}".format(self.value_date,
                                                                                         ins_pro_info[
                                                                                             'Ins_sim_name'],
                                                                                         ins_pro_info[
                                                                                             'Pro_sim_name'],
                                                                                         gz_sub_name))
            else:
                temp_list = list()
                for rri in ins_account_info_list:
                    ins_code = rri['Ins_code']
                    account = rri['account']
                    ins_sim_name = rri['Ins_sim_name']
                    temp_list.append([ins_code, ins_sim_name, account])
                return {'pt': temp_list}

                # raise RuntimeError("{}这天的托管机构{}的{}估值表上匹配多个产品账户信息表中的普通账户记录,科目名称为{}".format(self.value_date,
                #                                                                           ins_pro_info[
                #                                                                               'Ins_sim_name'],
                #                                                                           ins_pro_info[
                #                                                                               'Pro_sim_name'],
                #                                                                           gz_sub_name))
        elif map_type == self.sys_para.Map_type['期货账户类科目映射关系']:
            sql_get_ins_and_acc = """
            SELECT
            ins.`Ins_code`,
            ins.`Ins_sim_name`,
            ai.`account` 
            FROM
            `account_information` ai
            LEFT JOIN `institution_information` ins ON ai.ins_code = ins.Ins_code 
            WHERE
            ai.pro_code = %s
            AND ai.type_code = '03'
            AND ai.`status` in ('1','2','3')
                    """
            ins_account_info_list = self.mp.get_list(sql_get_ins_and_acc, [pro_id])
            if len(ins_account_info_list) == 1:
                res_ins_code = ins_account_info_list[0]['Ins_code']
                res_account = ins_account_info_list[0]['account']
                ins_sim_name = ins_account_info_list[0]['Ins_sim_name']
                return [res_ins_code, ins_sim_name, res_account]
            elif len(ins_account_info_list) < 1:
                raise RuntimeError("{}这天的托管机构{}的{}估值表上存在产品账户信息表中未收录的期货账户,科目名称为{}".format(self.value_date,
                                                                                         ins_pro_info[
                                                                                             'Ins_sim_name'],
                                                                                         ins_pro_info[
                                                                                             'Pro_sim_name'],
                                                                                         gz_sub_name))
            else:
                raise RuntimeError("{}这天的托管机构{}的{}估值表上匹配多个产品账户信息表中的期货账户记录,科目名称为{}".format(self.value_date,
                                                                                          ins_pro_info[
                                                                                              'Ins_sim_name'],
                                                                                          ins_pro_info[
                                                                                              'Pro_sim_name'],
                                                                                          gz_sub_name))
        elif map_type == self.sys_para.Map_type['期权账户类科目映射关系']:
            sql_get_ins_and_acc = """
                        SELECT
                        ins.`Ins_code`,
                        ins.`Ins_sim_name`,
                        ai.`account` 
                        FROM
                        `account_information` ai
                        LEFT JOIN `institution_information` ins ON ai.ins_code = ins.Ins_code 
                        WHERE
                        ai.pro_code = %s
                        AND ai.`status` = '1'
                        AND ai.type_code = '04'
                                """
            ins_account_info_list = self.mp.get_list(sql_get_ins_and_acc, [pro_id])
            if len(ins_account_info_list) == 1:
                res_ins_code = ins_account_info_list[0]['Ins_code']
                res_account = ins_account_info_list[0]['account']
                ins_sim_name = ins_account_info_list[0]['Ins_sim_name']
                return [res_ins_code, ins_sim_name, res_account]
            elif len(ins_account_info_list) < 1:
                raise RuntimeError("{}这天的托管机构{}的{}估值表上存在产品账户信息表中未收录的期权账户,科目名称为{}".format(self.value_date,
                                                                                         ins_pro_info[
                                                                                             'Ins_sim_name'],
                                                                                         ins_pro_info[
                                                                                             'Pro_sim_name'],
                                                                                         gz_sub_name))
            else:
                temp_list = list()
                for rri in ins_account_info_list:
                    ins_code = rri['Ins_code']
                    account = rri['account']
                    ins_sim_name = rri['Ins_sim_name']
                    temp_list.append([ins_code, ins_sim_name, account])
                return {'qq': temp_list}

                # raise RuntimeError("{}这天的托管机构{}的{}估值表上匹配多个产品账户信息表中的期权账户记录,科目名称为{}".format(self.value_date,
                #                                                                           ins_pro_info[
                #                                                                               'Ins_sim_name'],
                #                                                                           ins_pro_info[
                #                                                                               'Pro_sim_name'],
                #                                                                           gz_sub_name))
        elif map_type in [self.sys_para.Map_type['投资股票类科目映射关系'], self.sys_para.Map_type['投资基金类科目映射关系']]:
            # 进入证券代码型的
            print(pro_id, gz_sub_name)
            stock_code = str(gz_sub_name).split('_')[0].split('.')[-1]
            security_name = str(gz_sub_name).split('_')[1]
            return [stock_code, security_name]
            #  处理普通账户类型的映射
        elif map_type == self.sys_para.Map_type['投资自营产品类科目映射关系']:
            try:
                product_sim_name = re.search(r"(\w+)私募.+", gz_sub_name).groups(0)
            except AttributeError:
                try:
                    product_sim_name = re.search(r"(\w+)证券.+", gz_sub_name).groups(0)
                except AttributeError:
                    raise RuntimeError("估值表{}的科目{}未被投资自营产品类科目映射关系正确处理".format(self.pro_id,gz_sub_name))
            if 'B' in gz_sub_name:
                product_sim_name = product_sim_name[0] + 'B类'
            elif 'A' in gz_sub_name:
                product_sim_name = product_sim_name[0] + 'A类'
            else:
                product_sim_name = product_sim_name[0]
            sql_get_pro_code_and_name = "SELECT `Pro_code`,`Pro_full_name` FROM `pro_essential_factor` pf WHERE pf.`Pro_sim_name`=%s"
            pro_code_name = self.mp.get_one(sql_get_pro_code_and_name, product_sim_name)
            return [pro_code_name['Pro_code'], pro_code_name['Pro_full_name']]

    def replace_all_match_mark(self, replaced_list, replace_list, map_type=None, subject_type=None):
        res_subject_code = str(replaced_list[0])
        res_subject_name = str(replaced_list[1])
        if subject_type == '04':
            store_code = res_subject_code.replace("证券代码", replace_list[0])
            store_name = res_subject_name.replace("证券名称", replace_list[1])
        elif subject_type == '05':
            store_code = res_subject_code.replace('自营产品代码', replace_list[0])
            store_name = res_subject_name.replace('自营产品全称', replace_list[1])
        # elif subject_type
        else:
            store_code = res_subject_code.replace("机构代码.账户号", replace_list[0] + '.' + replace_list[2])
            store_name = res_subject_name.replace("机构简称_账户号", replace_list[1] + '_' + replace_list[2])

        return [store_code, store_name]

    # 机构代码.账户号  机构简称_账户号
    def set_value(self, data_frame, row):
        global Currency, Exchange_rate, Quantity, Unit_cost, Cost_currency, Cost_proportion, Quotation, Market_currency_value, Market_value_proportion, Valuation_appreciation, Suspension_information, Equity_information
        if not data_frame.isnull().iloc[row, 2]:
            Currency = data_frame.iloc[row, 2]
        else:
            Currency = None
        if not data_frame.isnull().iloc[row, 3]:
            Exchange_rate = data_frame.iloc[row, 3]
        else:
            Exchange_rate = None
        if not data_frame.isnull().iloc[row, 4]:
            Quantity = data_frame.iloc[row, 4]
        else:
            Quantity = None
        if not data_frame.isnull().iloc[row, 5]:
            Unit_cost = data_frame.iloc[row, 5]
        else:
            Unit_cost = None
        if not data_frame.isnull().iloc[row, 6]:
            Cost_currency = data_frame.iloc[row, 6]
        else:
            Cost_currency = None
        if not data_frame.isnull().iloc[row, 7]:
            Cost_proportion = data_frame.iloc[row, 7]
        else:
            Cost_proportion = None
        if not data_frame.isnull().iloc[row, 8]:
            Quotation = data_frame.iloc[row, 8]
        else:
            Quotation = None
        if not data_frame.isnull().iloc[row, 9]:
            Market_currency_value = data_frame.iloc[row, 9]
        else:
            Market_currency_value = None
        if not data_frame.isnull().iloc[row, 10]:
            Market_value_proportion = data_frame.iloc[row, 10]
        else:
            Market_value_proportion = None
        if not data_frame.isnull().iloc[row, 11]:
            Valuation_appreciation = data_frame.iloc[row, 11]
        else:
            Valuation_appreciation = None
        if not data_frame.isnull().iloc[row, 12]:
            Suspension_information = data_frame.iloc[row, 12]
        else:
            Suspension_information = None
        if not data_frame.isnull().iloc[row, 13]:
            Equity_information = data_frame.iloc[row, 13]
        else:
            Equity_information = None

    def real_load_to_base(self):
        for ele in self.wait_to_insert_list:
            sql_get_is_exist = "SELECT `Id` FROM `pro_subject_volume` WHERE `Date`=%s AND `Pro_code`=%s AND `Sub_code`=%s"
            try:
                date_format = datetime.datetime.strptime(ele[0], '%Y%m%d').date()
            except ValueError:
                date_format = datetime.datetime.strptime(ele[0], '%Y-%m-%d').date()
            res_exist_id = self.mp.get_one(sql_get_is_exist, [date_format, ele[1], ele[2]])
            if res_exist_id is not None:
                sql_delete = "DELETE FROM `pro_subject_volume` WHERE `Date`=%s AND `Pro_code`=%s"
                mp.modify(sql_delete, [date_format, ele[1]])
                break

        insert_batch_sql = "INSERT INTO `pro_subject_volume` (`Date`,`Pro_code`,`Sub_code`,`Sub_name`,`Currency`,`Exchange_rate`,`Quantity`,`Unit_cost`,`Cost_currency`," \
                           "`Cost_proportion`,`Quotation`,`Market_currency_value`,`Market_value_proportion`,`Valuation_appreciation`,`Suspension_information`,`Equity_information`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.mp.multiple_modify(insert_batch_sql, tuple(self.wait_to_insert_list))
        self.mp.close()

    def store_to_wait_insert_list(self, value_date, pro_id, sub_code, sub_name):
        self.wait_to_insert_list.append(
            [value_date, pro_id, sub_code, sub_name,
             Currency,
             Exchange_rate, Quantity, Unit_cost, Cost_currency, Cost_proportion, Quotation,
             Market_currency_value,
             Market_value_proportion, Valuation_appreciation, Suspension_information,
             Equity_information]
        )

    def load_file(self):
        data_frame = pd.read_excel(os.path.join(self.path, self.file))
        rows = data_frame.index.T.shape[0]
        if self.pro_id == 'SJT913':
            print("暂停")
        for row in range(rows):
            if not data_frame.isnull().iloc[row, 0]:
                global Currency, Exchange_rate, Quantity, Unit_cost, Cost_currency, Cost_proportion, Quotation, Market_currency_value, Market_value_proportion, Valuation_appreciation, Suspension_information, Equity_information
                if '.' in data_frame.iloc[row, 0]:
                    if not str(data_frame.iloc[row + 1, 0]).__contains__(data_frame.iloc[row, 0]):
                        # store_need_map_list.append(data_frame.iloc[row, 0])
                        sql_get_code_and_name = "SELECT js.`Subject_code`,js.`Subject_name`,js.`Subject_type`,pm.`Ins_sub_code`,pm.`Map_type` FROM `jm_subject_system` js LEFT JOIN `pro_subject_map` pm ON js.Id=pm.Map_jss_id WHERE pm.Ins_code=%s AND pm.Ins_sub_code=%s"
                        result_one = self.mp.get_one(sql_get_code_and_name, ['021', data_frame.iloc[row, 0]])
                        self.set_value(data_frame, row)
                        if result_one is not None:
                            if result_one['Subject_type'] == self.sys_para.Subject_type['固定型科目']:
                                self.store_to_wait_insert_list(self.value_date, self.pro_id, result_one['Subject_code'],
                                                               result_one['Subject_name'])
                            elif result_one['Map_type'] == self.sys_para.Map_type['信用账户类科目映射关系'] and result_one[
                                'Subject_type'] == self.sys_para.Subject_type['券商型科目']:
                                # self.pro_id  02  1
                                sql_get_account_ins_sim_name = "SELECT ins.`Ins_code`,ins.`Ins_sim_name` FROM institution_information ins INNER JOIN account_information ai on ins.Ins_code=ai.ins_code WHERE ai.pro_code =%s AND ai.type_code=%s AND ai.`status`=%s"
                                # 进入券商型科目的处理
                                ins_info = self.mp.get_one(sql_get_account_ins_sim_name, [self.pro_id, '02', '1'])
                                result_subject_code = str(result_one['Subject_code'])
                                result_subject_name = str(result_one['Subject_name'])
                                store_subject_code = result_subject_code.replace("机构代码", ins_info['Ins_code'])
                                store_subject_name = result_subject_name.replace("机构简称", ins_info['Ins_sim_name'])
                                self.store_to_wait_insert_list(self.value_date, self.pro_id, store_subject_code,
                                                               store_subject_name)
                            elif result_one['Map_type'] == self.sys_para.Map_type['信用账户类科目映射关系'] and result_one[
                                'Subject_type'] == self.sys_para.Subject_type['券商账户号型科目']:
                                sql_get_ins_and_account = "SELECT ins.`Ins_code`,ins.`Ins_sim_name`,ai.`account` FROM institution_information ins INNER JOIN account_information ai on ins.Ins_code=ai.ins_code WHERE ai.pro_code =%s AND ai.type_code=%s AND ai.`status`=%s"
                                ins_and_account = self.mp.get_one(sql_get_ins_and_account, [self.pro_id, '02', '1'])
                                result_subject_code = str(result_one['Subject_code'])
                                result_subject_name = str(result_one['Subject_name'])
                                store_subject_code = result_subject_code.replace("机构代码.账户号",
                                                                                 ins_and_account['Ins_code'] + '.' +
                                                                                 ins_and_account['account'])
                                store_subject_name = result_subject_name.replace("机构简称_账户号",
                                                                                 ins_and_account['Ins_sim_name'] + '_' +
                                                                                 ins_and_account['account'])
                                self.store_to_wait_insert_list(self.value_date, self.pro_id, store_subject_code,
                                                               store_subject_name)
                        else:
                            # print("科目代码的上级科目，用券商代码和它去查询映射表。结果集记录等于1，直接靠Map_type的映射来处理。如果大于1，则参考估值表上的科目名称或科目代码信息")
                            sql_get_code_and_name = "SELECT pm.`Ins_sub_code`,pm.`Map_type`,pm.`Map_jss_id`,js.`Subject_code`,js.`Subject_name`,js.`Subject_type`,js.`Is_leaf_subject`,js.`Subject_level` FROM `jm_subject_system` js LEFT JOIN `pro_subject_map` pm ON js.Id=pm.Map_jss_id WHERE pm.Ins_code=%s AND pm.Ins_sub_code like %s ORDER BY pm.`Id`"
                            tg_sub_code = str(data_frame.iloc[row, 0])
                            match_sub_code = tg_sub_code.split('.')[-1]
                            match_code = str(data_frame.iloc[row, 0]).replace('.' + match_sub_code, '')
                            result_list = self.mp.get_list(sql_get_code_and_name, ['021', match_code + '%%'])
                            print("数量是：=========》", len(result_list))
                            if len(result_list) > 1:
                                if 'HH' in data_frame.iloc[row, 0]:
                                    logger.output_log({'file_name': r'D:\BackUp\bugOut\log.txt',
                                                       'message': '{}存在未映射科目，科目代码为{}，科目名称为{}'.format(self.file,
                                                                                                     data_frame.iloc[
                                                                                                         row, 0],
                                                                                                     data_frame.iloc[
                                                                                                         row, 1])})
                                    continue
                                for ele in result_list:
                                    if match_sub_code[0:2] in ele['Ins_sub_code']:
                                        # 1031 先写期货类型的映射
                                        print(ele['Subject_code'], ele['Subject_name'])
                                        ins_account_info_list = self.get_all_match_info(self.pro_id,
                                                                                        data_frame.iloc[row, 1],
                                                                                        ele['Map_type'],
                                                                                        ele['Subject_type'])
                                        # 机构代码.账户号  机构简称_账户号
                                        wait_replaced_list = [ele['Subject_code'], ele['Subject_name']]
                                        try:
                                            if ele['Map_type'] == self.sys_para.Map_type['固定科目类科目映射关系'] and len(
                                                    str(data_frame.iloc[row, 0]).split('.')) != len(str(ele['Subject_level'])):
                                                break
                                            elif ele['Map_type'] == self.sys_para.Map_type['固定科目类科目映射关系'] and len(
                                                    str(data_frame.iloc[row, 0]).split('.')) == len(
                                                str(ele['Subject_level'])):
                                                self.store_to_wait_insert_list(self.value_date, self.pro_id,
                                                                               ele['Subject_code'], ele['Subject_name'])
                                                break
                                        except Exception as e:
                                            print(data_frame.iloc[row, 1])
                                            raise e
                                        if type(ins_account_info_list) == dict:
                                            if 'qq' in ins_account_info_list.keys():
                                                if type(ins_account_info_list['qq']) == list:
                                                    if self.pro_id == 'SJT913':
                                                        for iai in ins_account_info_list['qq']:
                                                            # res_ins_code, ins_sim_name, res_account
                                                            if str(data_frame.iloc[row, 1]).split('_')[-1] == str(
                                                                    iai[1])[0:2]:
                                                                res_store_list = self.replace_all_match_mark(
                                                                    wait_replaced_list, iai,
                                                                    subject_type=ele['Subject_type'])
                                                                self.store_to_wait_insert_list(self.value_date,
                                                                                               self.pro_id,
                                                                                               res_store_list[0],
                                                                                               res_store_list[1])
                                                                break
                                                            elif str(data_frame.iloc[row,0]) == '1021.QQ01' and iai[1] == '中信证券':
                                                                res_store_list = self.replace_all_match_mark(
                                                                    wait_replaced_list, iai,
                                                                    subject_type=ele['Subject_type'])
                                                                self.store_to_wait_insert_list(self.value_date,
                                                                                               self.pro_id,
                                                                                               res_store_list[0],
                                                                                               res_store_list[1])
                                                                break
                                                            else:
                                                                if self.is_no_need_map(self.trusteeship,
                                                                                       data_frame.iloc[row, 0]):
                                                                    logger.output_log(
                                                                        {'file_name': r'D:\BackUp\bugOut\log.txt',
                                                                         'message': '{}存在未映射科目，科目代码为{}，科目名称为{}'.format(
                                                                             self.file,
                                                                             data_frame.iloc[
                                                                                 row, 0],
                                                                             data_frame.iloc[
                                                                                 row, 1])})
                                                    elif self.pro_id == 'SS6382':
                                                        for iai in ins_account_info_list['qq']:
                                                            if str(data_frame.iloc[row, 0]).split(".")[1][-2:] == 'ZX':
                                                                res_store_list = self.replace_all_match_mark(
                                                                    wait_replaced_list, ins_account_info_list['qq'][1],
                                                                    subject_type=ele['Subject_type'])
                                                                self.set_value(data_frame, row)
                                                                self.store_to_wait_insert_list(self.value_date,
                                                                                               self.pro_id,
                                                                                               res_store_list[0],
                                                                                               res_store_list[1])
                                                                break
                                                            else:
                                                                res_store_list = self.replace_all_match_mark(
                                                                    wait_replaced_list, ins_account_info_list['qq'][0],
                                                                    subject_type=ele['Subject_type'])
                                                                self.store_to_wait_insert_list(self.value_date,
                                                                                               self.pro_id,
                                                                                               res_store_list[0],
                                                                                               res_store_list[1])
                                                                break
                                                    else:
                                                        raise RuntimeError("{}估值表中的科目映射多条产品账户信息表记录".format(self.pro_id))
                                                    break
                                        else:
                                            res_store_list = self.replace_all_match_mark(wait_replaced_list,
                                                                                         ins_account_info_list,
                                                                                         subject_type=ele[
                                                                                             'Subject_type'])
                                            self.store_to_wait_insert_list(self.value_date, self.pro_id,
                                                                           res_store_list[0], res_store_list[1])
                                            break
                                    elif ele['Map_type'] == self.sys_para.Map_type['期权账户类科目映射关系']:
                                        print('期权类')
                                        if match_sub_code[0:2] in ele['Ins_sub_code']:
                                            print("计息")
                                            ins_account_info_list = self.get_all_match_info(self.pro_id,
                                                                                            data_frame.iloc[row, 1],
                                                                                            ele['Map_type'],
                                                                                            ele['Subject_type'])
                                            wait_replaced_list = [ele['Subject_code'], ele['Subject_name']]
                                            res_store_list = self.replace_all_match_mark(wait_replaced_list,
                                                                                         ins_account_info_list,
                                                                                         subject_type=ele[
                                                                                             'Subject_type'])
                                            self.store_to_wait_insert_list(self.value_date, self.pro_id,
                                                                           res_store_list[0], res_store_list[1])
                                            break
                                        else:
                                            # 非计息
                                            ins_account_info_list = self.get_all_match_info(self.pro_id,
                                                                                            data_frame.iloc[row, 1],
                                                                                            ele['Map_type'],
                                                                                            ele['Subject_type'])
                                            wait_replaced_list = [ele['Subject_code'], ele['Subject_name']]
                                            res_store_list = self.replace_all_match_mark(wait_replaced_list,
                                                                                         ins_account_info_list,
                                                                                         subject_type=ele[
                                                                                             'Subject_type'])
                                            self.store_to_wait_insert_list(self.value_date, self.pro_id,
                                                                           res_store_list[0], res_store_list[1])
                                            break

                                    elif ele['Map_type'] == self.sys_para.Map_type['普通账户类科目映射关系']:
                                        if match_sub_code[0:2] in ele['Ins_sub_code']:
                                            ins_account_info_list = self.get_all_match_info(self.pro_id,
                                                                                            data_frame.iloc[row, 1],
                                                                                            ele['Map_type'],
                                                                                            ele['Subject_type'])
                                            wait_replaced_list = [ele['Subject_code'], ele['Subject_name']]
                                            res_store_list = self.replace_all_match_mark(wait_replaced_list,
                                                                                         ins_account_info_list,
                                                                                         subject_type=ele[
                                                                                             'Subject_type'])
                                            self.store_to_wait_insert_list(self.value_date, self.pro_id,
                                                                           res_store_list[0], res_store_list[1])
                                            break
                                        else:
                                            #  非计息
                                            ins_account_info_list = self.get_all_match_info(self.pro_id,
                                                                                            data_frame.iloc[row, 1],
                                                                                            ele['Map_type'],
                                                                                            ele['Subject_type'])
                                            if type(ins_account_info_list) == list:

                                                wait_replaced_list = [ele['Subject_code'], ele['Subject_name']]
                                                res_store_list = self.replace_all_match_mark(wait_replaced_list,
                                                                                             ins_account_info_list,
                                                                                             subject_type=ele[
                                                                                                 'Subject_type'])
                                                self.store_to_wait_insert_list(self.value_date, self.pro_id,
                                                                               res_store_list[0], res_store_list[1])
                                                break
                                            elif type(ins_account_info_list) == dict:
                                                if 'pt' in ins_account_info_list.keys():
                                                    for iai in ins_account_info_list['pt']:
                                                        if self.pro_id == 'SR7565' and str(data_frame.iloc[row,0]) == '1031.23':
                                                            wait_replaced_list = [ele['Subject_code'],
                                                                                  ele['Subject_name']]
                                                            res_store_list = self.replace_all_match_mark(
                                                                wait_replaced_list,
                                                                iai,
                                                                subject_type=ele[
                                                                    'Subject_type'])
                                                            self.store_to_wait_insert_list(self.value_date, self.pro_id,
                                                                                           res_store_list[0],
                                                                                           res_store_list[1])
                                                            break
                                                        elif self.pro_id == 'ST2960':
                                                            # 在托管估值表上只记录了一个普通账户科目，实际上有两个普通账户，所以去掉账户号
                                                            ins_code = None
                                                            ins_name = None
                                                            for iai in ins_account_info_list['pt']:
                                                                ins_code = iai[0]
                                                                ins_name = iai[1]
                                                                break
                                                            wait_sub_code = str(result_list[1]['Subject_code'])[:-4]
                                                            wait_sub_name = str(result_list[1]['Subject_name'])[:-4]
                                                            sub_code = wait_sub_code.replace("机构代码", ins_code)
                                                            sub_name = wait_sub_name.replace("机构简称", ins_name)
                                                            self.store_to_wait_insert_list(self.value_date, self.pro_id,
                                                                                           sub_code, sub_name)
                                                            break
                                                        else:
                                                            raise RuntimeError(
                                                                "{}估值表科目在产品账户信息表中对应多条".format(self.pro_id))
                                                    break
                                    elif ele['Map_type'] == self.sys_para.Map_type['投资自营产品类科目映射关系']:
                                        pro_code_name_info_list = self.get_all_match_info(self.pro_id,
                                                                                          data_frame.iloc[row, 1],
                                                                                          ele['Map_type'])
                                        wait_replaced_list = [ele['Subject_code'], ele['Subject_name']]
                                        res_store_list = self.replace_all_match_mark(wait_replaced_list,
                                                                                     pro_code_name_info_list,
                                                                                     subject_type=ele['Subject_type'])
                                        self.store_to_wait_insert_list(self.value_date, self.pro_id, res_store_list[0],
                                                                       res_store_list[1])
                                        break
                            elif len(result_list) == 1:
                                ele = result_list[0]
                                if ele['Map_type'] == self.sys_para.Map_type['固定科目类科目映射关系'] and len(
                                        str(data_frame.iloc[row, 0]).split('.')) != len(str(ele['Subject_level'])):
                                    continue
                                if ele['Map_type'] == self.sys_para.Map_type['普通账户类科目映射关系']:
                                    # 存出保证金普通账户利息映
                                    if self.pro_id == 'ST2960':
                                        ins_account_info_list = self.get_all_match_info(self.pro_id,
                                                                                        data_frame.iloc[row, 1],
                                                                                        ele['Map_type'],
                                                                                        ele['Subject_type'])
                                        wait_sub_code = ele['Subject_code'][:-4]
                                        wait_sub_name = ele['Subject_name'][:-4]
                                        sub_code = wait_sub_code.replace("机构代码", ins_account_info_list['pt'][0][0])
                                        sub_name = wait_sub_name.replace("机构简称", ins_account_info_list['pt'][0][1])
                                        self.store_to_wait_insert_list(self.value_date, self.pro_id, sub_code, sub_name)
                                    else:
                                        ins_account_info_list = self.get_all_match_info(self.pro_id,
                                                                                        data_frame.iloc[row, 1],
                                                                                        ele['Map_type'])
                                        wait_replaced_list = [ele['Subject_code'], ele['Subject_name']]
                                        res_store_list = self.replace_all_match_mark(wait_replaced_list,
                                                                                     ins_account_info_list)
                                        self.store_to_wait_insert_list(self.value_date, self.pro_id, res_store_list[0],
                                                                       res_store_list[1])
                                if ele['Subject_type'] == self.sys_para.Subject_type['证券代码型科目']:
                                    ele = result_list[0]
                                    wait_replaced_list = [result_list[0]['Subject_code'],
                                                          result_list[0]['Subject_name']]

                                    stock_code_and_name = self.get_all_match_info(self.pro_id,
                                                                                  data_frame.iloc[row, 0] + '_' +
                                                                                  data_frame.iloc[row, 1],
                                                                                  ele['Map_type'], ele['Subject_type'])
                                    res_store_list = self.replace_all_match_mark(wait_replaced_list,
                                                                                 stock_code_and_name,
                                                                                 subject_type=ele['Subject_type'])
                                    self.store_to_wait_insert_list(self.value_date, self.pro_id, res_store_list[0],
                                                                   res_store_list[1])
                                if ele['Subject_type'] == self.sys_para.Subject_type['固定型科目'] or result_list[0][
                                    'Map_type'] == self.sys_para.Map_type['固定科目类科目映射关系']:
                                    ele = result_list[0]
                                    self.store_to_wait_insert_list(self.value_date, self.pro_id, ele['Subject_code'],
                                                                   ele['Subject_name'])
                            else:
                                if self.is_no_need_map(self.trusteeship, data_frame.iloc[row, 0]):
                                    logger.output_log(
                                        {'file_name': r'D:\BackUp\bugOut\log.txt',
                                         'message': '{}存在未映射科目，科目代码为{}，科目名称为{}'.format(
                                             self.file,
                                             data_frame.iloc[
                                                 row, 0],
                                             data_frame.iloc[
                                                 row, 1])})
                    else:
                        self.set_value(data_frame, row)
                        if self.pro_id == 'SS6382':
                            if data_frame.iloc[row, 0] == '1021.QQ01':
                                sql_get_code_and_name = "SELECT pm.`Ins_sub_code`,pm.`Map_type`,pm.`Map_jss_id`,js.`Subject_code`,js.`Subject_name`,js.`Subject_type`,js.`Is_leaf_subject`,js.`Subject_level` FROM `jm_subject_system` js LEFT JOIN `pro_subject_map` pm ON js.Id=pm.Map_jss_id WHERE pm.Ins_code=%s AND pm.Ins_sub_code like %s ORDER BY pm.`Id`"
                                tg_sub_code = str(data_frame.iloc[row, 0])
                                match_sub_code = tg_sub_code.split('.')[-1]
                                match_code = str(data_frame.iloc[row, 0]).replace('.' + match_sub_code, '')
                                res_list = self.mp.get_list(sql_get_code_and_name, ['021', match_code + '%%'])
                                matched_database_one = None
                                for ele in res_list:
                                    if 'QQ' in ele['Ins_sub_code'] and 'QX' not in ele['Ins_sub_code']:
                                        matched_database_one = ele
                                wait_replaced_list = [matched_database_one['Subject_code'],
                                                      matched_database_one['Subject_name']]
                                ins_account_info_list = self.get_all_match_info(self.pro_id,
                                                                                data_frame.iloc[row, 1],
                                                                                matched_database_one['Map_type'],
                                                                                matched_database_one['Subject_type'])
                                for iai in ins_account_info_list['qq']:
                                    if str(data_frame.iloc[row, 0]).split(".")[1][-2:] == 'ZX':
                                        res_store_list = self.replace_all_match_mark(
                                            wait_replaced_list, ins_account_info_list['qq'][1],
                                            subject_type=matched_database_one['Subject_type'])
                                        self.store_to_wait_insert_list(self.value_date, self.pro_id, res_store_list[0],
                                                                       res_store_list[1])
                                        break
                                    else:
                                        res_store_list = self.replace_all_match_mark(
                                            wait_replaced_list, ins_account_info_list['qq'][0],
                                            subject_type=matched_database_one['Subject_type'])
                                        self.store_to_wait_insert_list(self.value_date, self.pro_id, res_store_list[0],
                                                                       res_store_list[1])
                                        break
                            elif not str(data_frame.iloc[row,0]).startswith('1021'):
                                pass
                            elif str(data_frame.iloc[row,0]).split(".")[-1] in ['03','23']:
                                pass
                            else:
                                if self.is_no_need_map(self.trusteeship, data_frame.iloc[row, 0]):
                                    logger.output_log(
                                        {'file_name': r'D:\BackUp\bugOut\log.txt',
                                         'message': '{}存在未映射科目，科目代码为{}，科目名称为{}'.format(
                                             self.file,
                                             data_frame.iloc[
                                                 row, 0],
                                             data_frame.iloc[
                                                 row, 1])})
                        else:
                            pass
                else:
                    self.set_value(data_frame, row)
                    sql_get_rows = "SELECT js.`Subject_code`,js.`Subject_name`,pm.`Map_type` FROM `jm_subject_system` js LEFT JOIN `pro_subject_map` pm ON js.Id=pm.Map_jss_id WHERE pm.Ins_code=%s AND pm.Ins_sub_code=%s AND pm.`Map_jss_id` is not Null"
                    res_one = self.mp.get_one(sql_get_rows, ['021', data_frame.iloc[row, 0]])
                    self.set_value(data_frame, row)
                    if res_one is not None:
                        if res_one['Map_type'] == self.sys_para.Map_type['文字类一列科目映射关系']:
                            Market_currency_value = data_frame.iloc[row, 1]
                            if ',' in Market_currency_value:
                                Market_currency_value = str(Market_currency_value).replace(',', '')
                            self.store_to_wait_insert_list(self.value_date, self.pro_id, res_one['Subject_code'],
                                                           res_one['Subject_name'])
                        elif res_one['Map_type'] == self.sys_para.Map_type['文字类全科目映射关系']:
                            self.store_to_wait_insert_list(self.value_date, self.pro_id, res_one['Subject_code'],
                                                           res_one['Subject_name'])
        if self.pro_id == 'SGF044':
            print("=????????>>>>>>")
        else:
            self.real_load_to_base()


if __name__ == '__main__':
    base_dir = r'D:\Users\Administrator\AppData\Local\Programs\PycharmWorkSpace\Test_Dev\testException\valuation_table\招商证券'
    # base_dir = r'D:\Users\Administrator\AppData\Local\Programs\PycharmWorkSpace\Test_Dev\testException\origin'
    # file_name = 'SN0910久铭1号私募证券投资基金委托资产资产估值表20220825.xls'
    count = 0
    # lvt = Load_Valuation_table(base_dir, file_name, 'SN0910','20220825')
    # lvt.load_file()
    for file in os.listdir(base_dir):
        product_id, product, value_date = re.search(r'([A-Za-z0-9]+)(\w+)私募[^\d]+(\d+)', file).groups()
        trust_name = os.getcwd().split(os.path.sep)[-2]
        print(trust_name)
        lvt = Load_Valuation_table(base_dir, file, product_id, value_date,trust_name)
        try:
            # if product_id == 'SJR635':
            #     continue
            lvt.load_file()
        except Exception as e:
            print(e)
            raise RuntimeError("{}运行异常：{}".format(file, str(e)))
        count += 1
        print(file, "加载完成")
        print("第{}个".format(count))

# resss = data_frame.index
# int_tuple = resss.T.shape
# print(int_tuple[0])
# # list_key_words = ['单位净值', '实收资本', '资产净值', '资产合计', '负债合计']
# store_need_map_list = list()
# for row in range(int_tuple[0]):
#     if data_frame.iloc[row,0] in list_key_words:
#
#         if data_frame.iloc[row,0] != '单位净值':
#             print(data_frame.iloc[row,9])
#         else:
#             print(data_frame.iloc[row,1])


# for ele in store_need_map_list:
#     sql_get_code_and_name = "SELECT js.`Subject_code`,js.`Subject_name` FROM `jm_subject_system` js LEFT JOIN `pro_subject_map` pm ON js.Id=pm.Map_jss_id WHERE pm.Ins_code=%s AND pm.Ins_sub_code=%s"
#     # 这个返回的list可能小于1，等于1 或者大于1。 小于1则表示数据库的科目代码是用了通配符，等于1则可能是固定型；大于1则需通过科目名称【或科目代码】来判断应该属于哪行映射记录
#     result_one = mp.get_one(sql_get_code_and_name, ['021',ele])
#     if result_one is not None:
#         print(result_one['Subject_code'],result_one['Subject_name'])
#
# # for row in range(int_tuple[0]):
# #     if data_frame.iloc[row,0] in list_key_words:
# #
# #         if data_frame.iloc[row,0] != '单位净值':
# #             print(data_frame.iloc[row,9])
# #         else:
# #             print(data_frame.iloc[row,1])
#
# for ele in store_words_map_list.keys():
#     print(ele, end=":")
#     print(store_words_map_list[ele])
