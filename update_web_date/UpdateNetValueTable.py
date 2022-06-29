# _*_ coding: utf-8 _*_
from update_web_date.utils.DataSource import DataSource


class UpdateNetValueTable():
    def __init__(self, dict_obj, gw_dict):
        self.db = dict_obj['db']
        self.con = DataSource(dict_obj)
        self.gw_con = DataSource(gw_dict)

    def get_origin_net_value_list(self, frequency_code):
        """
        :param frequency_code: ,频次代码，这里指定0，1，2分别表示每日，每周，每月
        :return:origin_net_value_list 对应频次在(久铭)净值表或静久净值表中的结果行列表
        """
        from update_web_date.utils.BackToDay import BackToDay
        import datetime
        if self.db == 'jingjiu_ta':
            net_value_table = '静久净值表'
        else:
            net_value_table = '净值表'
        week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        per_friday_set = set()
        per_month_set = set()
        sql_max = 'SELECT MAX(`日期`) FROM `{}`'.format(net_value_table)
        sql_min = 'SELECT Min(`日期`) FROM `{}`'.format(net_value_table)
        max_date = self.con.get_one(sql_max, None)
        min_date = self.con.get_one(sql_min, None)
        max_date_day = max_date['MAX(`日期`)']
        min_date_day = min_date['Min(`日期`)']
        days = max_date_day - min_date_day
        for day in range(days.days + 1):
            min_date_day = min_date_day + datetime.timedelta(days=1)
            xing_qi = week_list[min_date_day.weekday()]
            if xing_qi == '星期六':
                btd = BackToDay(1, min_date_day)
                res_day = btd.primary()
                per_friday_set.add(res_day)
                # print(week_list[res_day.weekday()])
            if str(min_date_day).split('-')[-1] == '01':
                btd = BackToDay(1, min_date_day)
                res_day = btd.primary()
                per_friday_set.add(res_day)
                per_month_set.add(res_day)
            # min_date_day = min_date_day + datetime.timedelta(days=1)
        sql_get_net_value = 'SELECT * FROM `{}`'.format(net_value_table)
        origin_net_value_list = list()
        if frequency_code == 0:
            origin_net_value_list = self.con.get_list(sql_get_net_value, None)
        elif frequency_code == 1:
            sql_get_net_value += ' WHERE `日期` in %s'
            origin_net_value_list = self.con.get_list(sql_get_net_value, [per_friday_set])
        elif frequency_code == 2:
            sql_get_net_value += ' WHERE `日期` in %s'
            origin_net_value_list = self.con.get_list(sql_get_net_value, [per_month_set])

        return origin_net_value_list

    def get_format_frequecey_net_value_list(self, origin_net_value_list):
        """
        传入相应频次的净值表中的记录行列表数据，返回每日、每周或每月净值表字段要求的列表数据
        :param origin_net_value_list: 数据来源于净值表（这个是已经按每日、每周或每月要求整理过结果行）
        :return: net_value_list_temp  即返回 日期、产品代码、产品简称、单位净值 的列表
        """
        net_value_list_temp = list()
        for row in origin_net_value_list:
            res_time = row['日期']
            for key in dict(row).keys():
                if key == '日期':
                    continue
                # 拿着这个产品名称去产品要素表里找code，填充到净值对象中
                sql_new_product = 'SELECT `产品代码`FROM `最新产品要素表` WHERE `产品简称`= %s'
                code_dict = self.con.get_one(sql_new_product, [key])
                print(res_time, code_dict['产品代码'], key, row[key])
                net_value_list_temp.append([res_time, code_dict['产品代码'], key, row[key]])
        return net_value_list_temp

    def update_net_value_tabel(self, to_table_net_value_list, frequecy_table_name):
        """
        把前两步整理好的数据更新至对应的频次表中
        :param to_table_net_value_list: 待插入的净值记录
        :param frequecy_table_name: 对应的频次表
        :return: None
        """
        sql_query_perday = 'SELECT * FROM `{}`'.format(frequecy_table_name)
        perday_list = self.con.get_list(sql_query_perday, None)
        if len(perday_list) > 0:
            sql_delete_perday = 'DELETE FROM `{}`'.format(frequecy_table_name)
            self.con.modify(sql_delete_perday, None)
        sql_perday_update = 'INSERT INTO `{}`(`net_date`,`product_code`,`product_name`,`net_value`) VALUES (%s,%s,%s,%s)'.format(
            frequecy_table_name)
        sql_perday_delenull = 'DELETE FROM `{}` WHERE `net_value` is NULL '.format(frequecy_table_name)
        com_batch = tuple(to_table_net_value_list)
        self.con.multiple_modify(sql_perday_update, com_batch)
        self.con.modify(sql_perday_delenull, None)

    def update_performance_base(self):
        sql_get = "SELECT * FROM `业绩基准表`"
        res_list = self.con.get_list(sql_get, None)
        store_list = list()
        for dic in res_list:
            store_list.append([dic['日期'], dic['000300.SH'], dic['SPX.GI'], dic['HSI.HI'], dic['一年期定期存款利率']])

        sql_get_perfor = "SELECT * FROM `performance_base`"
        res_per_list = self.con.get_list(sql_get_perfor, None)
        if len(res_per_list) > 0:
            sql_del = "DELETE FROM `performance_base`"
            self.con.modify(sql_del, None)

        sql_insert_performance = "INSERT INTO `performance_base` (`base_date`,`hushen`,`biaopu`,`hengsheng`,`fixed_rate`) VALUES (%s,%s,%s,%s,%s)"
        com_batch = tuple(store_list)
        self.con.multiple_modify(sql_insert_performance, com_batch)

    def update_netvalue_gw(self, local_table, map_tabel):
        sql_get_date = 'SELECT DISTINCT(`net_date`) FROM `{}` pn WHERE pn.net_date > (SELECT MAX(`net_date`) FROM `{}` )'.format(
            local_table, map_tabel)
        res_date_list = self.con.get_list(sql_get_date, None)
        store_list = []
        if len(res_date_list) > 0:
            for day in res_date_list:
                one_day = day['net_date']
                sql_get_netvalue = 'SELECT * FROM `{}` WHERE  `net_date` = %s'.format(local_table)
                res_net_value_list = self.con.get_list(sql_get_netvalue, [one_day])
                for net_value in res_net_value_list:
                    store_list.append([net_value['net_date'], net_value['product_code'], net_value['product_name'],
                                       net_value['net_value']])
            sql_insert_to_wz = 'INSERT INTO `{}`(`net_date`,`product_code`,`product_name`,`net_value`) VALUES (%s,%s,%s,%s)'.format(
                local_table)
            tuple_store_list = tuple(store_list)
            self.gw_con.multiple_modify(sql_insert_to_wz, tuple_store_list)
        # 补充过一下，在最大日期相等的时候，在本地表某产品有净值记录但在网站表上却没有，找到这些产品，并把它用来查本地表净值，再上传到官网。
        if len(res_date_list) == 0:
            sql_get_max_date = 'SELECT MAX(`net_date`) FROM {}'.format(local_table)
            max_date = unvt.con.get_one(sql_get_max_date, None)['MAX(`net_date`)']
            sql_get_list = 'SELECT * FROM `{}` pn  WHERE pn.net_date = %s AND pn.product_code not in (SELECT `product_code` FROM `{}`  WHERE `net_date` = %s  )'.format(
                local_table, map_tabel)
            res_dict_list = unvt.con.get_list(sql_get_list, [max_date, max_date])
            if len(res_dict_list) != 0:
                store_net_list = list()
                for dict in res_dict_list:
                    store_net_list.append(
                        [dict['net_date'], dict['product_code'], dict['product_name'], dict['net_value']])
                sql_insert_wz = 'INSERT INTO `{}` (`net_date`,`product_code`,`product_name`,`net_value`) VALUES (%s,%s,%s,%s)'.format(
                    local_table)
                unvt.gw_con.multiple_modify(sql_insert_wz, store_net_list)


if __name__ == '__main__':
    dict_obj_input = {'host': '127.0.0.1', 'user': 'root', 'passwd': '123456', 'db': 'jiuming_ta_new'}
    dict_obj_wz = {'host': '121.40.107.3', 'user': 'jiuming2018', 'passwd': 'ByA3nFjspni2365e', 'db': 'jiuming2018'}
    frequecy_table_list = ['perday_netvalue', 'perweek_netvalue', 'permonth_netvalue']
    unvt = UpdateNetValueTable(dict_obj_input, dict_obj_wz)
    for i in range(3):
        origin_list = unvt.get_origin_net_value_list(i)
        format_list = unvt.get_format_frequecey_net_value_list(origin_list)
        unvt.update_net_value_tabel(format_list, frequecy_table_list[i])
    # 把wavezhou本地的大于网站表的最新日期的记录，增加操作到网站数据库
    for i in range(3):
        unvt.update_netvalue_gw(frequecy_table_list[i], frequecy_table_list[i] + '_gw')

    # sql_get_list = 'SELECT * FROM `perday_netvalue` pn  WHERE pn.net_date = %s AND pn.product_code not in (SELECT `product_code` FROM `perday_netvalue_copy1`  WHERE `net_date` = %s  )'
    # res_dict_list = unvt.con.get_list(sql_get_list, ['2022-06-24', '2022-06-24'])
    # store_net_list = list()
    # for dict in res_dict_list:
    #     store_net_list.append([dict['net_date'], dict['product_code'], dict['product_name'],
    #                            dict['net_value']])
    # sql_insert = 'INSERT INTO `{}` (`net_date`,`product_code`,`product_name`,`net_value`) VALUES (%s,%s,%s,%s)'.format(
    #     'perday_netvalue_copy1')
    # unvt.con.multiple_modify(sql_insert, tuple(store_net_list))
    # unvt.update_performance_base()
    # unvt.con.close()
