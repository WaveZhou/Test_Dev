# _*_ coding: utf-8 _*_
import datetime
import os
# 识别出每个券商账户文件夹下的文件的日期，is not RAR是哪个日期就放到哪个日期对应的target年月日目录下
# 如果RAR，则查看券商账户是啥，如果康康是55826.txt的还是盯市文件的，先解压出里面的文件，再根据文件里的对账单日期，放进对应的target年月日目录
import re
import shutil
import pandas as pd
import pdfplumber

from Check_Bill_Test.Institution.impl.DongBei import DongBei
from Check_Bill_Test.Institution.impl.AnXin import AnXin
from Check_Bill_Test.Institution.impl.ChangJiang import ChangJiang
from Check_Bill_Test.Institution.impl.GuoJun import GuoJun
from Check_Bill_Test.Institution.impl.GuoTouAnXin import GuoTouAnXin
from Check_Bill_Test.Institution.impl.HuaChuang import HuaChuang
from Check_Bill_Test.Institution.impl.JianXin import JianXin
from Check_Bill_Test.Institution.impl.NanHua import NanHua
from Check_Bill_Test.Institution.impl.XingYe import XingYe
from Check_Bill_Test.Institution.impl.YinHe import YinHe
from Check_Bill_Test.Institution.impl.YongAn import YongAn
from Check_Bill_Test.Institution.impl.ZhongXinJianTou import ZhongXinJianTou
from Check_Bill_Test.Institution.impl.ZhongCaiQiHuo import ZhongCaiQiHuo
from Check_Bill_Test.Institution.AbstractInstitution import AbstractInstitution
from Check_Bill_Test.utils.Log_Record import Log
from Check_Bill_Test.utils.MysqlProxy import MysqlProxy

from Transform_FileName import Transform_FileName

settings = {
    'origin_path': r'D:\整理券商对账单\origin\收件日20220612 当天',
    'target_path': r'D:\整理券商对账单\target',
    'not_matched': r'D:\整理券商对账单\notMatchedFile',
    'bugOut': r'D:\BackUp\bugOut'
}
temp_store_rar = list()
tf = Transform_FileName()
institution_map = {
    '南华期货账户': 'NanHua',
    '国君普通账户': 'GuoJun',
    '国君期权账户': 'GuoJun',
    '国投安信期货账户': 'GuoTouAnXin',
    '安信期货账户': 'AnXin',
    '建信期货账户': 'JianXin',
    '永安期货账户': 'YongAn',
    '银河普通账户': 'YinHe',
    '银河期货账户': 'YinHe',
    '长江期货账户': 'ChangJiang',
    '中信建投普通账户': 'ZhongXinJianTou',
    '东北普通账户': 'DongBei',
    '华创期货账户': 'HuaChuang',
    '中财期货账户': 'ZhongCaiQiHuo'
}
mp = MysqlProxy()

origin_count = 0
date_str = str(datetime.datetime.now().date())
run_date = ''
logger1 = Log('File_Match_Institution_Type')
logger2 = Log('File_Match_Suppose_Arrive')
logger3 = Log('File_Match_Multi_Account')
logger4 = Log('Key_Map_Error')
date_type = datetime.datetime.now()
flag = True
not_dealed = 0


class Auto_Increment:
    def __init__(self):
        self.num = 0
        self.target_file = None
        self.target_pre_file = None

    def get_add_one(self):
        self.num += 1
        return self.num

    def set_target_file(self, file: str):
        self.target_file = file

    def set_target_pre_file(self, file: str):
        self.target_pre_file = file


def rename_to_new_dir(origin_path, target_path, re_file_name, signal, flag):
    """
    源目录下的文件拷贝或剪切到目标目录，并更换目标目录的文件名
    :param origin_path: 源目录（精确到文件）
    :param target_path: 目标目录（只到目录）
    :param re_file_name: 新文件名名
    :param signal: 信号，1. 为拷贝， 2. 为剪切
    :param flag:目标目录文件已存在 增量为True,替换为False
    :return:Auto_Increment类的对象
    """
    # old_path = os.path.join(settings['origin_path'], institution, file_name)
    # new_path_parent = os.path.join(settings['not_matched'], date_str, dir_name)
    if not os.path.exists(target_path):
        os.makedirs(target_path, exist_ok=True),
    new_path = os.path.join(target_path, re_file_name)
    ai = Auto_Increment()
    count = 0
    if flag:
        map_dict = dict()
        while os.path.exists(new_path):
            new_path = os.path.join(target_path, re_file_name.split('.')[0] + '(' + str(ai.get_add_one()) + ').' +
                                    re_file_name.split('.')[1])
            map_dict[count] = new_path.split('\\')[-1]
            count += 1
        target_file = new_path.split('\\')[-1]
        ai.set_target_file(str(target_file))
        if count >= 2:
            ai.set_target_pre_file(str(map_dict[count - 2]))
    else:
        if os.path.exists(new_path):
            os.remove(new_path)
    if signal == 1:
        shutil.copy(origin_path, new_path)
    elif signal == 2:
        os.rename(origin_path, new_path)
    return ai


# 新增数据进对账单到达表
def insert_into_statement_arrive(account_id, res_date, file_name):
    sql_query = 'SELECT file_name FROM jm_statement.statement_arrive WHERE id=%s AND start_date=%s AND end_date=%s AND file_name=%s AND `status`=%s'
    res_arrived = mp.get_one(sql_query, [account_id, res_date, res_date, file_name, 1])
    if res_arrived is None:
        sql_add = 'INSERT into statement_arrive (`id`,`start_date`,`end_date`,`file_name`,`status`) VALUES (%s,%s,%s,%s,1)'
        mp.modify(sql_add, [account_id, res_date, res_date, file_name])


def add_to_statement_arrive(res_date: str, res_account_id: list, start_date=None):
    if start_date is not None:
        begin_date = start_date
    else:
        begin_date = res_date
    count = 0
    for res_account in res_account_id:
        count += 1
        res_account = res_account['account_id']
        sql_get_product_type = 'SELECT product,belong,`type` from jm_statement.account_information WHERE id=%s'
        product_type = mp.get_one(sql_get_product_type, [res_account])
        product = product_type['product']
        belong = product_type['belong']
        account_type = product_type['type']
        # 先查询该记录在实到表中是否存在（id,文件名，起止日期，状态都一样），如果已存在，则不做操作，不存在则新增
        # sql_query = 'SELECT file_name FROM jm_statement.statement_arrive WHERE id=%s AND start_date=%s AND end_date=%s AND file_name=%s AND `status`=%s'
        # res_arrived = mp.get_one(sql_query, [account_id, res_date, res_date, file_or_rar, 1])
        # if res_arrived is None:
        #     sql_add = 'INSERT into statement_arrive (`id`,`start_date`,`end_date`,`file_name`,`status`) VALUES (%s,%s,%s,%s,1)'
        #     mp.modify(sql_add, [account_id, res_date, res_date, file_or_rar])
        # else:
        #     pass
        # 把对账单拷贝到按产品分类和按券商分类，然后给对账单原始未知文件名前加上已处理_
        # 对应的券商信息表id，源对账单目录，源对账单文件名，对账单开始日期，对账单结束日期，目标对账单目录1 ，目标对账单目录2，目标对账单文件名，处理日期和时间，是否有效
        # if '-' in res_date
        if '-' in res_date:
            res_date = ''.join(res_date.split('-'))
        if '/' in res_date:
            res_date = ''.join(res_date.split('/'))
        origin_path_parent = os.path.join(settings['origin_path'], institution)
        origin_path = os.path.join(origin_path_parent, file_or_rar)
        target_path_by_product = os.path.join(settings['target_path'], '交易日' + res_date, '对账单按产品整理',
                                              product, belong + account_type)
        target_path_by_institution = os.path.join(settings['target_path'], '交易日' + res_date, '对账单按券商整理',
                                                  belong + account_type, product)
        if not file_or_rar.startswith('已处理'):
            res_pro = rename_to_new_dir(origin_path, target_path_by_product, file_or_rar, 1, True)
            rename_to_new_dir(origin_path, target_path_by_institution, file_or_rar, 1, True)
            current_time = datetime.datetime.now()
            try:
                if res_pro.num > 0:
                    # 则把这个数减去1后的对账单目标目录的记录改成无效，并写入新增修改后的目标目录到数据库arrive
                    if res_pro.num - 1 == 0:
                        sql_update_target_filename = 'UPDATE statement_arrive SET `status` = %s WHERE id = %s AND target_file_name = %s AND end_date = %s'
                        mp.modify(sql_update_target_filename, [0, res_account, file_or_rar, res_date])
                        print('把原来样子的文件名改成无效，把**（1）.txt的目标文件名写入数据库')
                    else:
                        sql_update_target_filename = 'UPDATE statement_arrive SET `status` = %s WHERE id = %s AND target_file_name = %s AND end_date = %s '
                        mp.modify(sql_update_target_filename, [0, res_account, res_pro.target_pre_file, res_date])
                        print('把数据库中**（res_num_pro-1）.txt的目标文件名改为无效，把**（res_num_pro）写入数据库')
                    # 把拷贝到target目录的文件写入数据库到达表
                    sql_insert_target_filename = 'INSERT INTO statement_arrive (`id`,`origin_path`,`origin_file_name`,`start_date`,`end_date`,`target_path_product`,`target_path_institution`,`target_file_name`,`operate_time`,`status`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    mp.create(sql_insert_target_filename,
                              [res_account, origin_path, file_or_rar, begin_date, res_date,
                               target_path_by_product,
                               target_path_by_institution, res_pro.target_file, current_time, 1])
                else:
                    # 直接把目标目录写入arrive表
                    sql_insert_target_filename = 'INSERT INTO statement_arrive (`id`,`origin_path`,`origin_file_name`,`start_date`,`end_date`,`target_path_product`,`target_path_institution`,`target_file_name`,`operate_time`,`status`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

                    mp.create(sql_insert_target_filename,
                              [res_account, origin_path, file_or_rar, begin_date, res_date,
                               target_path_by_product,
                               target_path_by_institution, res_pro.target_file, current_time, 1])
            except:
                print(file_or_rar,institution)
            # 写完arrive表，准备把源目录下的相应文件改为已处理
            if count == len(res_account_id):
                rename_to_new_dir(origin_path, origin_path_parent, '已处理_' + file_or_rar, 2, True)


while flag:
    try:
        os.listdir(settings['origin_path'])
    except FileNotFoundError:
        print('今日无对账单')
        break
    for institution in os.listdir(settings['origin_path']):

        if institution == '托管估值表' or institution == '未知数据' or institution == '清算数据':
            continue
        if os.path.isfile(os.path.join(settings['origin_path'], institution)):
            continue
        if os.path.isdir(os.path.join(settings['origin_path'], institution)):
            for file_or_rar in os.listdir(os.path.join(settings['origin_path'], institution)):
                if file_or_rar.startswith('已处理'):
                    continue
                if file_or_rar.endswith('rar') or file_or_rar.endswith('RAR') or file_or_rar.endswith(
                        'ZIP') or file_or_rar.endswith('zip'):
                    temp_store_rar.append(file_or_rar)
                    # print('是需要解压压缩包的文件')
                    if institution == '国君普通账户':
                        print('暂停')
                    try:
                        institution_class = institution_map[institution]
                        cur_belong = institution[0:2]
                        cur_type = institution[-4:-2]
                        institution_impl = locals()[institution_class](cur_belong, cur_type)
                        if isinstance(institution_impl, AbstractInstitution):
                            institution_impl.load_file_content_for_date(
                                os.path.join(settings['origin_path'], institution))
                            # 文件中的日期及文件名（可能含有多个）都需要返回
                    except KeyError:
                        subject_words = '在Map映射中未匹配到键或值'
                        bug_out_path = os.path.join(settings['bugOut'], subject_words)
                        if not os.path.exists(bug_out_path):
                            os.makedirs(bug_out_path, exist_ok=True)
                        bug_out_path = bug_out_path + r'\{}-log.txt'.format(date_str)
                        logger4.show_debug('券商账户为{}的文件夹名未在institution_map中匹配到键'.format(institution))
                        logger4.output_log({'file_name': bug_out_path,
                                            'message': '券商账户为{}的文件夹名未在institution_map中匹配到键'.format(institution)})
                        rename_to_new_dir(os.path.join(settings['origin_path'], institution, file_or_rar),
                                          os.path.join(settings['origin_path'], institution), '已处理_' + file_or_rar, 2,
                                          False)
                        continue

                else:
                    origin_count = origin_count + 1
                    res_date = tf.get_date(file_or_rar)
                    begin_date = None
                    res_file_without_date = ''
                    if institution == '特别处理':
                        df = pd.read_excel(os.path.join(settings['origin_path'],institution,file_or_rar))
                        data = df.iloc[2, 1]
                        start_date_origin_str = str(data).split('--')[0].strip()
                        begin_date = datetime.datetime.strptime(start_date_origin_str, '%Y年%m月%d日').strftime(
                            '%Y-%m-%d')
                        end_date_origin_str = str(data).split('--')[1].strip()
                        res_date = datetime.datetime.strptime(end_date_origin_str, '%Y年%m月%d日').strftime(
                            '%Y-%m-%d')
                        #pass
                        # if '8001002072' in file_or_rar:
                        #     begin_date = file_or_rar.split('.')[0].split('_')[1]
                        #     res_date = file_or_rar.split('.')[0].split('_')[2]
                        #     res_file_without_date = '8001002072'
                        # else:
                        #     res_file_without_date = file_or_rar.split('.')[0].split('-')[0]
                        #     begin_date = file_or_rar.split('.')[0].split('-')[1]
                        #     res_date = file_or_rar.split('.')[0].split('-')[2]

                    if res_date is None or res_date == '':
                        if institution == '中银国际普通账户':
                            if '股票期权' in file_or_rar:
                                try:
                                    # 905-客户-股票期权客户对账单20220301-0331.xls
                                    str_date = datetime.datetime.strftime(date_type, '%Y')
                                    year_now = str_date[-2:]
                                    res_date = '20' + year_now + file_or_rar.split('.')[0][-4:]  # 取的结束日期
                                    res = re.search(r'\d{8}-\d{4}', file_or_rar).group(0)
                                    begin_date = res[4:8]
                                    res_file_without_date = re.sub(res, '', file_or_rar)
                                except AttributeError:
                                    df = pd.read_excel(os.path.join(settings['origin_path'], institution, file_or_rar))
                                    begin_date_str = str(df.iloc[1, 0]).split("：")[1].split('-')[0].strip()
                                    begin_date = datetime.datetime.strptime(begin_date_str,
                                                                            "%Y年%m月%d日").date().strftime(
                                        '%Y-%m-%d')
                                    end_date_str = str(df.iloc[1, 0]).split("：")[1].split('-')[1].strip()
                                    res_date = datetime.datetime.strptime(end_date_str, "%Y年%m月%d日").date().strftime(
                                        '%Y-%m-%d')
                            elif '.txt' in file_or_rar:
                                res_file_without_date = file_or_rar.split('.')[0].split('-')[0] + '-' + '.' + \
                                                        file_or_rar.split('.')[1]
                                with open(os.path.join(settings['origin_path'], institution, file_or_rar), 'r') as f:
                                    res = re.search(r'统计日期:.+(\d{4}[-/]?\d{2}[-/]?\d{2})', f.read()).group(0)
                                    res_date_str = res.split(':')[1].strip()
                                    begin_date = res_date_str.split('-')[0].strip()  # 对账单开始时间
                                    end_date = res_date_str.split('-')[1].strip()
                                    res_date = end_date
                        elif institution == '兴业普通账户':
                            if file_or_rar.endswith('txt'):
                                with open(os.path.join(settings['origin_path'], institution, file_or_rar), 'r') as f:
                                    try:
                                        res_content = f.read()
                                        res = re.search(r'对帐日期:.+(\d{4}[-/]?\d{2}[-/]?\d{2})', res_content).group(0)
                                    except AttributeError:
                                        res = re.search(r'统计日期:.+(\d{4}[-/]?\d{2}[-/]?\d{2})', res_content).group(0)
                                    res_date_str = res.split(':')[1].strip()
                                    begin_date = res_date_str.split('-')[0].strip()
                                    end_date = res_date_str.split('-')[1].strip()
                                    # 检查一下start_date是否与end_date相等
                                    res_date = end_date
                            elif file_or_rar.endswith('pdf'):

                                try:
                                    with pdfplumber.open(
                                            os.path.join(settings['origin_path'], institution, file_or_rar)) as pdf:
                                        print(pdf.pages)  # Page对象列表
                                        page = pdf.pages[0]
                                        res = re.search(r'统计日期:.*(\d{4}[-/]?\d{2}[-/]?\d{2})',
                                                        page.extract_text()).group(0)
                                        res_date_str = res.split(':')[1].strip()
                                        begin_date = res_date_str.split('-')[0].strip()
                                        res_date = res_date_str.split('-')[1].strip()
                                        # 检查一下start_date是否与end_date相等
                                except AttributeError:
                                    if '2880005122久铭专享17号' in file_or_rar:
                                        print()

                        elif institution == '兴业期权账户':
                            with open(os.path.join(settings['origin_path'], institution, file_or_rar), 'r') as f:
                                try:
                                    res_content = f.read()
                                    res = re.search(r'起止日期:.+(\d{4}[-/]?\d{2}[-/]?\d{2})', res_content).group(0)
                                except AttributeError:
                                    res = re.search(r'统计日期:.+(\d{4}[-/]?\d{2}[-/]?\d{2})', res_content).group(0)
                                res_date_str = res.split(':')[1].strip()
                                start_date = res_date_str.split('-')[0].strip()
                                end_date = res_date_str.split('-')[1].strip()
                                res_date = start_date
                        elif institution == '国君期权账户':
                            with pdfplumber.open(
                                    os.path.join(settings['origin_path'], institution, file_or_rar)) as pdf:
                                print(pdf.pages)  # Page对象列表
                                page = pdf.pages[0]
                                res_date = \
                                    re.search(r'日期:.*(\d{4}?\d{2}?\d{2})', page.extract_text()).group(0).split(':')[
                                        1].strip()
                        elif '中信建投' in institution:
                            res_date = tf.get_date(file_or_rar)
                            if res_date == '' or res_date is None:
                                if '股票期权' in file_or_rar:
                                    with pdfplumber.open(
                                            os.path.join(settings['origin_path'], institution, file_or_rar)) as pdf:
                                        print(pdf.pages)  # Page对象列表
                                        page = pdf.pages[0]
                                        res_date = \
                                            re.search(r'日期:.*(\d{4}?\d{2}?\d{2})', page.extract_text()).group(0).split(
                                                ':')[
                                                1].strip()
                                else:
                                    if file_or_rar.endswith('pdf'):
                                        with pdfplumber.open(os.path.join(settings['origin_path'], institution, file_or_rar)) as pdf:

                                            page = pdf.pages[0]
                                            try:
                                                res = re.search(r'\d{4}[-/]+\d{2}[-/]+\d{2}',page.extract_text()).group(0)
                                                res_year = res.split('-')[0]
                                            except AttributeError:
                                                res_year = \
                                                    re.search(r'日期:.*(\d{4}?\d{2}?\d{2})', page.extract_text()).group(0).split(':')[1].strip()[-8:-4]
                                                #res_year = re.search(r': 1 :(\d{4}[-/]?\d{2}[-/]?\d{2})',page.extract_text()).group(0)[-8:-4]
                                                #rename_to_new_dir(os.path.join(settings['origin_path'],institution,file_or_rar),'D:\迅雷下载\扫描件待处理',file_or_rar,2,False)
                                            month_and_day = file_or_rar.split('.')[0].split('-')[1]
                                            res_date = res_year + month_and_day

                                    elif file_or_rar.endswith('TXT') or file_or_rar.endswith('txt'):
                                        try:
                                            with open(os.path.join(settings['origin_path'], institution, file_or_rar),
                                                      'r') as f:  # 打开文件
                                                res_date_str = re.search(r'对帐期间：.*(.*)', f.read()).group(0)
                                                begin_date_str = res_date_str.split('：')[1].strip().split('---')[
                                                    0].strip()
                                                res_date_str = res_date_str.split('：')[1].strip().split('---')[
                                                    1].strip()
                                                begin_date = datetime.datetime.strptime(begin_date_str,
                                                                                        '%Y年%m月%d日').strftime(
                                                    '%Y-%m-%d')
                                                res_date = datetime.datetime.strptime(res_date_str,
                                                                                      '%Y年%m月%d日').strftime('%Y-%m-%d')
                                        except AttributeError:
                                            with open(os.path.join(settings['origin_path'], institution, file_or_rar),
                                                      'r') as f:  # 打开文件
                                                res_date_str = re.search(r'对账起止日期：.*(.*)', f.read()).group(0)
                                                begin_date_str = res_date_str.split('：')[1].strip().split('-')[
                                                    0].strip()
                                                res_date_str = res_date_str.split('：')[1].strip().split('-')[1].strip()
                                                begin_date = datetime.datetime.strptime(begin_date_str,
                                                                                        '%Y年%m月%d日').strftime(
                                                    '%Y-%m-%d')
                                                res_date = datetime.datetime.strptime(res_date_str,
                                                                                      '%Y年%m月%d日').strftime('%Y-%m-%d')
                                    res_file_without_date = file_or_rar.split('.')[0].split('-')[0] + '-' + '.' + \
                                                            file_or_rar.split('.')[1]
                            else:
                                res_file_without_date = tf.get_filename_without_date(file_or_rar)
                        elif institution == '南华期货账户':
                            with open(os.path.join(settings['origin_path'], institution, file_or_rar), 'r') as f:
                                res_content = f.read()
                                res = re.search(r'Date.+(\d{4}[-/]?\d{2}[-/]?\d{2})', res_content).group(0)
                                res_date = res.split('：')[1].strip()
                        elif institution == '永安期货账户':
                            try:
                                with open(os.path.join(settings['origin_path'], institution, file_or_rar), 'r') as f:
                                    res_content = f.read()
                                    res = re.search(r'日期:.+(\d{4}[-/]?\d{2}[-/]?\d{2})', res_content).group(0)
                                    res_date = res.split(':')[1].strip()
                            except AttributeError:
                                subject_words = '对账单文件名在应到表中未匹配'
                                old_path = os.path.join(settings['origin_path'], institution, file_or_rar)
                                target_path = os.path.join(settings['not_matched'], date_str, subject_words)
                                rename_to_new_dir(old_path, target_path, '未匹配_' + file_or_rar, 1, False)
                                rename_to_new_dir(os.path.join(settings['origin_path'], institution, file_or_rar),
                                                  os.path.join(settings['origin_path'], institution),
                                                  '已处理_' + file_or_rar, 2,
                                                  False)
                                bug_out_path = os.path.join(settings['bugOut'], subject_words)
                                if not os.path.exists(bug_out_path):
                                    os.makedirs(bug_out_path, exist_ok=True)
                                bug_out_path = bug_out_path + r'\{}-log.txt'.format(date_str)
                                # '文件名为{}的，券商账户类型为{}的对账单在应到表中未匹配到记录，'.format(file_or_rar, institution)
                                logger2.show_debug('文件名[ {} ]、券商账户类型为[ {} ]的对账单在应到表中未匹配到记录'.format(file_or_rar,
                                                                                                   institution))
                                logger2.output_log({'file_name': bug_out_path,
                                                    'message': '文件名[ {} ]、券商账户类型为[ {} ]的对账单在应到表中未匹配到记录'.format(
                                                        file_or_rar,
                                                        institution)})
                        elif institution == '华创期货账户':
                            with open(os.path.join(settings['origin_path'], institution, file_or_rar), 'r') as f:
                                res_content = f.read()
                                res = re.search(r'日期:.+(\d{4}[-/]?\d{2}[-/]?\d{2})', res_content).group(0)
                                res_date = res.split(':')[1].strip()
                        # try:
                        #     if institution_map[institution] == 'XingYe':
                        #         xy = XingYe()
                        #         xy.load_file_content_for_date('兴业', '普通')
                        # except:
                        #     pass
                        # 这个分支里只要把res_date从文件中读取并赋值就好

                        elif institution == '招商证券':
                            file_path = os.path.join(settings['origin_path'], institution, file_or_rar)
                            df = pd.read_excel(file_path)
                            if file_or_rar.__contains__('期权'):
                                data = df.iloc[1, 0]
                                res_date = str(data).split('.')[0]
                            elif file_or_rar.__contains__('对账单'):
                                data = df.iloc[1, 1]
                                res_date = ''.join(filter(str.isdigit, data))
                            elif file_or_rar.__contains__('信用对账'):
                                data = df.iloc[0, 3]
                                begin_date = str(data).split('-')[0].strip()
                                res_date = str(data).split('-')[1].strip()
                            else:
                                raise RuntimeError('文件名{}没有对应的解析对账日期方法'.format(file_or_rar))
                        elif institution == '长江期货账户':
                            try:
                                with open(os.path.join(settings['origin_path'], institution, file_or_rar), 'r') as f:
                                    res_content = f.read()
                                    res = re.search(r'日.*期:.*(\d{4}[-/]?\d{2}[-/]?\d{2})', res_content).group(0)
                                    res_date = res.split(':')[1].strip()
                            except UnicodeDecodeError:
                                with open(os.path.join(settings['origin_path'], institution, file_or_rar), encoding='utf-8') as f:
                                    res_content = f.read()
                                    res = re.search(r'日.*期:.*(\d{4}[-/]?\d{2}[-/]?\d{2})', res_content).group(0)
                                    res_date = res.split(':')[1].strip()
                        elif '海通' in institution:
                            if '普通' in institution:
                                try:
                                    with open(os.path.join(settings['origin_path'], institution, file_or_rar),
                                              encoding='utf-8') as f:
                                        res_content = f.read()
                                        begin_date_str = re.search(r'开始日期.*：.*(\d{4}[-/]?\d{2}[-/]?\d{2})',
                                                                   res_content).group(0)
                                        if '结束'in begin_date_str:
                                            begin_date_str = begin_date_str.split('结')[0]
                                        begin_date = begin_date_str.split('：')[1].strip()
                                        res_date_str = re.search(r'结束日期.*：.*(\d{4}[-/]?\d{2}[-/]?\d{2})',
                                                                 res_content).group(0)
                                        res_date = res_date_str.split('：')[1].strip()
                                except UnicodeDecodeError:
                                    with open(os.path.join(settings['origin_path'], institution, file_or_rar),
                                              'r') as f:
                                        res_content = f.read()
                                        begin_date_str = re.search(r'开始日期.*：.*(\d{4}[-/]?\d{2}[-/]?\d{2})',
                                                                   res_content).group(0)
                                        begin_date = begin_date_str.split('：')[1].strip()
                                        res_date_str = re.search(r'结束日期.*：.*(\d{4}[-/]?\d{2}[-/]?\d{2})',
                                                                 res_content).group(0)
                                        res_date = res_date_str.split('：')[1].strip()
                            elif '期权' in institution:
                                try:
                                    with open(os.path.join(settings['origin_path'], institution, file_or_rar),
                                              'r') as f:
                                        res_content = f.read()
                                        print(res_content)
                                        res = re.search(r'日.*期.*:.*(\d{4}[-/]?\d{2}[-/]?\d{2})', res_content).group(0)
                                        res_date = res.split(':')[1].strip()
                                except AttributeError:
                                    with open(os.path.join(settings['origin_path'], institution, file_or_rar),
                                              'r') as f:
                                        res_content = f.read()
                                        print(res_content)
                                        res = re.search(r'日.*期.*(\d{4}[-/]?\d{2}[-/]?\d{2})', res_content).group(0)
                                        res_date = res.split('期')[1].strip()
                        elif institution == '建信期货账户':
                            with open(os.path.join(settings['origin_path'], institution, file_or_rar), 'r') as f:
                                res_content = f.read()
                                res = re.search(r'日期.*Date.*：.*(\d{4}[-/]?\d{2}[-/]?\d{2})', res_content).group(0)
                                res_date = res.split('：')[1].strip()
                        elif institution == '银河期货账户':
                            with open(os.path.join(settings['origin_path'], institution, file_or_rar), 'r') as f:
                                res_content = f.read()
                                res = re.search(r'日期.*Date.*:.*(\d{4}[-/]?\d{2}[-/]?\d{2})', res_content).group(0)
                                res_date = res.split(':')[1].strip()
                        elif institution == '补发账单':
                            df = pd.read_excel(os.path.join(settings['origin_path'], institution, file_or_rar))
                            if '融资融券' in file_or_rar:
                                begin_date_str = str(df.iloc[0, 0]).split(":")[1].split('--')[0].strip()
                                begin_date = datetime.datetime.strptime(begin_date_str, "%Y年%m月%d日").date().strftime(
                                    '%Y-%m-%d')
                                end_date_str = str(df.iloc[0, 0]).split(":")[1].split('--')[1].strip()
                                res_date = datetime.datetime.strptime(end_date_str, "%Y年%m月%d日").date().strftime(
                                    '%Y-%m-%d')
                            else:
                                begin_date_str = str(df.iloc[1, 0]).split("：")[1].split('-')[0].strip()
                                begin_date = datetime.datetime.strptime(begin_date_str, "%Y年%m月%d日").date().strftime(
                                    '%Y-%m-%d')
                                end_date_str = str(df.iloc[1, 0]).split("：")[1].split('-')[1].strip()
                                res_date = datetime.datetime.strptime(end_date_str, "%Y年%m月%d日").date().strftime(
                                    '%Y-%m-%d')
                        elif institution == '手动分类':
                            if '久铭稳健22号私募证券投资基金' in file_or_rar:
                                df = pd.read_excel(os.path.join(settings['origin_path'], institution, file_or_rar))
                                data = df.iloc[0, 0]
                                res_date = datetime.datetime.strftime(data, '%Y-%m-%d')
                        elif institution == '中信海外':
                            with pdfplumber.open(
                                    os.path.join(settings['origin_path'], institution, file_or_rar)) as pdf:
                                page = pdf.pages[0]
                                print(page.extract_text())
                                res_date = \
                                    re.search(r'Date.*:.*(\d{4}[-/]?\d{2}[-/]?\d{2})', page.extract_text()).group(
                                        0).split(
                                        ':')[1].strip()
                        else:
                            # 把它放到上一级目录去
                            print('此时的券商账户类型目录为：', end="")
                            print(institution)
                            rename_to_new_dir(os.path.join(settings['origin_path'], institution, file_or_rar),
                                              os.path.join(settings['origin_path'], '未知数据'), '待处理_' + file_or_rar, 1,
                                              False)
                            res_date = '0000-00-00'
                    if res_file_without_date == '':
                        res_file_without_date = tf.get_filename_without_date(file_or_rar)
                    if institution == '招商证券':
                        if file_or_rar.__contains__('('):
                            res_file_without_date = file_or_rar.split('(')[0].strip()
                    if institution == '补发账单':
                        res_file_without_date = str(file_or_rar).split('.')[0][:-4]
                    # if '特别中信建投' == institution:
                    #     res_file_without_date = str(file_or_rar).split('.')[0].split('-')[0] + '.' + str(file_or_rar).split('.')[1]
                    if institution == '中财期货账户':
                        res_file_without_date = tf.get_filename_without_date(file_or_rar, '\d{4}\d{2}\d{2}')
                        res_date = tf.get_date(file_or_rar, '\d{4}\d{2}\d{2}')
                    sql_get = 'SELECT account_id FROM jm_statement.suppose_arrive WHERE `account_number` = %s AND valid_status =1;'
                    res_account_id = mp.get_list(sql_get, [res_file_without_date.strip().replace(' ', '')])

                    if institution in ('未知数据', '手动分类', '清算数据', '申万宏源', '华泰互换', '华创手动'):
                        pass
                        # print(file_or_rar)
                    else:
                        if len(res_account_id) != 0:
                            account_id = res_account_id[0]['account_id']
                            # 用当前的券商account_id去查询账户信息表中的券商及账户类型，看是否与文件夹institution相匹配
                            sql_get_belong_type = 'SELECT belong,`type` from jm_statement.account_information where id = %s'
                            res_belong_type_json = mp.get_one(sql_get_belong_type, [account_id])
                            simple_belong = res_belong_type_json['belong'][0:2]
                            simple_type = res_belong_type_json['type'][0:2]
                            if simple_belong == '华泰' and simple_type == '收益':
                                simple_type = '互换'
                            if simple_type == '信用':
                                simple_type = '两融'
                            if res_belong_type_json['type'][-2:] == '互换':
                                simple_belong = '收益'
                            # sql_get = 'SELECT account_id FROM jm_statement.suppose_arrive WHERE `account_number` = %s AND valid_status =1;'
                            # res_account_id = mp.get_list(sql_get, [res_file_without_date])
                            if simple_belong in institution and simple_type in institution:
                                pass
                            else:
                                # 文件名在应到表中关联的券商账户机构信息为：simple,账户类型为type，与该文件所在目录institution不匹配
                                subject_words = '对账单文件关联券商和账户类型问题'
                                bug_out_path = os.path.join(settings['bugOut'], subject_words)
                                if not os.path.exists(bug_out_path):
                                    os.makedirs(bug_out_path, exist_ok=True)
                                bug_out_path = bug_out_path + r'\{}-log.txt'.format(date_str)
                                # 文件内容的重命名，同时到更新到新目录
                                # old_path = os.path.join(settings['origin_path'], institution, file_name)
                                # new_path_parent = os.path.join(settings['not_matched'], date_str, dir_name)
                                old_path = os.path.join(settings['origin_path'], institution, file_or_rar)
                                target_path = os.path.join(settings['not_matched'], date_str, subject_words)
                                rename_to_new_dir(old_path, target_path, '券商和账户类型有问题_' + file_or_rar, 1, False)
                                # 文件名[{}]所在目录券商类型{}未与账户信息表券商{}、类型{}正确匹配
                                logger1.output_log({'file_name': bug_out_path,
                                                    'message': '文件名[{}]所在目录券商类型{}与账户信息表{}券商、{}类型未正确匹配'.format(
                                                        file_or_rar,
                                                        institution,
                                                        simple_belong,
                                                        simple_type)})
                    if institution == '华创手动':
                        print('=================')
                    if len(res_account_id) > 1:
                        sql = "SELECT `status` FROM jm_statement.account_information WHERE `id` = %s "
                        temp_account_id_list = list()
                        if institution == '华创手动':
                            for res_id in res_account_id:
                                account_id = res_id['account_id']
                                account_status = mp.get_one(sql, [account_id])
                                if account_status['status'] == '1':
                                    temp_account_id_list.append({'account_id': account_id})
                            add_to_statement_arrive(res_date, temp_account_id_list)
                        else:
                            subject_words = '文件名在应到表匹配到多条记录'
                            old_path = os.path.join(settings['origin_path'], institution, file_or_rar)
                            target_path = os.path.join(settings['not_matched'], date_str, subject_words)
                            rename_to_new_dir(old_path, target_path, '多记录匹配_' + file_or_rar, 1, False)
                            bug_out_path = os.path.join(settings['bugOut'], subject_words)
                            if not os.path.exists(bug_out_path):
                                os.makedirs(bug_out_path, exist_ok=True)
                            bug_out_path = bug_out_path + r'\{}-log.txt'.format(date_str)
                            logger3.output_log(
                                {'file_name': bug_out_path, 'message': '文件名{}在对账单应到表中匹配了多个券商账户'.format(file_or_rar)})

                    elif len(res_account_id) == 1:
                        # 在应到表中匹配到了券商账户id,在实到表中做新增

                        add_to_statement_arrive(res_date, res_account_id, begin_date)

                        # account_id = res_account_id[0]['account_id']
                        # sql_get_product_type = 'SELECT product,belong,`type` from jm_statement.account_information WHERE id=%s'
                        # product_type = mp.get_one(sql_get_product_type, [account_id])
                        # product = product_type['product']
                        # belong = product_type['belong']
                        # account_type = product_type['type']
                        # # 先查询该记录在实到表中是否存在（id,文件名，起止日期，状态都一样），如果已存在，则不做操作，不存在则新增
                        # # sql_query = 'SELECT file_name FROM jm_statement.statement_arrive WHERE id=%s AND start_date=%s AND end_date=%s AND file_name=%s AND `status`=%s'
                        # # res_arrived = mp.get_one(sql_query, [account_id, res_date, res_date, file_or_rar, 1])
                        # # if res_arrived is None:
                        # #     sql_add = 'INSERT into statement_arrive (`id`,`start_date`,`end_date`,`file_name`,`status`) VALUES (%s,%s,%s,%s,1)'
                        # #     mp.modify(sql_add, [account_id, res_date, res_date, file_or_rar])
                        # # else:
                        # #     pass
                        # # 把对账单拷贝到按产品分类和按券商分类，然后给对账单原始未知文件名前加上已处理_
                        # # 对应的券商信息表id，源对账单目录，源对账单文件名，对账单开始日期，对账单结束日期，目标对账单目录1 ，目标对账单目录2，目标对账单文件名，处理日期和时间，是否有效
                        # # if '-' in res_date
                        # if '-' in res_date:
                        #     res_date = ''.join(res_date.split('-'))
                        # if '/' in res_date:
                        #     res_date = ''.join(res_date.split('/'))
                        # origin_path_parent = os.path.join(settings['origin_path'], institution)
                        # origin_path = os.path.join(origin_path_parent, file_or_rar)
                        # target_path_by_product = os.path.join(settings['target_path'], '交易日' + res_date, '对账单按产品整理',
                        #                                       product, belong + account_type)
                        # target_path_by_institution = os.path.join(settings['target_path'], '交易日' + res_date, '对账单按券商整理',
                        #                                           belong + account_type, product)
                        # if not file_or_rar.startswith('已处理'):
                        #     res_pro = rename_to_new_dir(origin_path, target_path_by_product, file_or_rar, 1, True)
                        #     res_ins = rename_to_new_dir(origin_path, target_path_by_institution, file_or_rar, 1, True)
                        #     current_time = datetime.datetime.now()
                        #     if res_pro.num > 0:
                        #         # 则把这个数减去1后的对账单目标目录的记录改成无效，并写入新增修改后的目标目录到数据库arrive
                        #         if res_pro.num - 1 == 0:
                        #             sql_update_target_filename = 'UPDATE statement_arrive SET `status` = %s WHERE id = %s AND target_file_name = %s '
                        #             mp.modify(sql_update_target_filename, [0, account_id, file_or_rar])
                        #             print('把原来样子的文件名改成无效，把**（1）.txt的目标文件名写入数据库')
                        #         else:
                        #             sql_update_target_filename = 'UPDATE statement_arrive SET `status` = %s WHERE id = %s AND target_file_name = %s '
                        #             mp.modify(sql_update_target_filename, [0, account_id, res_pro.target_pre_file])
                        #             print('把数据库中**（res_num_pro-1）.txt的目标文件名改为无效，把**（res_num_pro）写入数据库')
                        #         # 把拷贝到target目录的文件写入数据库到达表
                        #         sql_insert_target_filename = 'INSERT INTO statement_arrive (`id`,`origin_path`,`origin_file_name`,`start_date`,`end_date`,`target_path_product`,`target_path_institution`,`target_file_name`,`operate_time`,`status`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                        #         mp.create(sql_insert_target_filename,
                        #                   [account_id, origin_path, file_or_rar, res_date, res_date,
                        #                    target_path_by_product,
                        #                    target_path_by_institution, res_pro.target_file, current_time, 1])
                        #     else:
                        #         # 直接把目标目录写入arrive表
                        #         sql_insert_target_filename = 'INSERT INTO statement_arrive (`id`,`origin_path`,`origin_file_name`,`start_date`,`end_date`,`target_path_product`,`target_path_institution`,`target_file_name`,`operate_time`,`status`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                        #         mp.create(sql_insert_target_filename,
                        #                   [account_id, origin_path, file_or_rar, res_date, res_date,
                        #                    target_path_by_product,
                        #                    target_path_by_institution, res_pro.target_file, current_time, 1])
                        #     # 写完arrive表，准备把源目录下的相应文件改为已处理
                        #
                        #     rename_to_new_dir(origin_path, origin_path_parent, '已处理_' + file_or_rar, 2, True)
                    else:  # 在应到表中没有匹配到券商id，日志记录对账单文件名，康康是否应该配置新的应到对账单文件
                        # 文件内容的重命名，同时到更新到新目录
                        subject_words = '对账单文件名在应到表中未匹配'
                        old_path = os.path.join(settings['origin_path'], institution, file_or_rar)
                        target_path = os.path.join(settings['not_matched'], date_str, subject_words)
                        rename_to_new_dir(old_path, target_path, '未匹配_' + file_or_rar, 2, False)
                        # 未在应到表中匹配到的文件名的日志记录
                        bug_out_path = os.path.join(settings['bugOut'], subject_words)
                        if not os.path.exists(bug_out_path):
                            os.makedirs(bug_out_path, exist_ok=True)
                        bug_out_path = bug_out_path + r'\{}-log.txt'.format(date_str)
                        # '文件名为{}的，券商账户类型为{}的对账单在应到表中未匹配到记录，'.format(file_or_rar, institution)
                        logger2.show_debug('文件名[ {} ]、券商账户类型为[ {} ]的对账单在应到表中未匹配到记录'.format(file_or_rar,
                                                                                           institution))
                        logger2.output_log({'file_name': bug_out_path,
                                            'message': '文件名[ {} ]、券商账户类型为[ {} ]的对账单在应到表中未匹配到记录'.format(file_or_rar,
                                                                                                       institution)})
    for institution in os.listdir(settings['origin_path']):

        if institution == '托管估值表' or institution == '未知数据' or institution == '清算数据':
            continue
        if os.path.isfile(os.path.join(settings['origin_path'], institution)):
            continue
        for file in os.listdir(os.path.join(settings['origin_path'], institution)):
            if not file.startswith('已处理'):
                not_dealed += 1
    if not_dealed > 0:
        not_dealed = 0
    else:
        flag = False

mp.close()
print('本次处理完成 ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

#
