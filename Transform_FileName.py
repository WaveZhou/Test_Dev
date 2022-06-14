import re, datetime

# suppose_arrive_str = '0011000048久铭专享6号.txt'  # 在文件名配置表中
# actually_ariive_str = '0011000048久铭专享6号20220217.txt'
# # 从trade_date表中，拿到2022-02-17周四这天
# trade_date = '2022-02-17'
# # 那么结合交易日表，这天的交易日应到文件名字符串就变为
# act_suppose_arrive = suppose_arrive_str + trade_date.strip()  # 去掉中间-，字符串相连
"""
传入带有日期的文件名字符串，
返回:
①正确匹配的日期字符串
②不带日期的字符串
"""


class Transform_FileName(object):
    def __init__(self):
        pass

    # def __init__(self, origin_date: str):
    #     self.regex_str = '\d{4}[-/]?\d{2}[-/]?\d{2}'
    #     self.subject = origin_date

    # 校验日期字符串的合法性
    def validate(self, date_text: str):
        if int(date_text[0:4]) in (2021, 2022, 2023, 2024):
            pass
        else:
            return False
        try:
            if date_text != datetime.datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
            return True
        except ValueError:
            try:
                if date_text != datetime.datetime.strptime(date_text, "%Y/%m/%d").strftime('%Y/%m/%d'):
                    raise ValueError
                return True
            except ValueError:
                try:
                    if date_text != datetime.datetime.strptime(date_text, "%Y%m%d").strftime('%Y%m%d'):
                        raise ValueError
                    return True
                except ValueError:
                    # raise ValueError("错误日期格式或日期,格式是年-月-日")
                    return False

    # 从多个匹配出的日期字符串中返回正确的一个
    def right_match(self, matches_list):
        for match in matches_list:
            if self.validate(match):
                return match
        return None

    # 获取字符串中匹配到的日期
    def get_date(self, subject: str, regex='\d{4}[-/]?\d{2}[-/]?\d{2}'):

        regex = re.compile(regex)
        matches_list = regex.findall(subject)
        if len(matches_list) == 0:
            pass
        right_date = ''
        if len(matches_list) != 0:
            right_date = self.right_match(matches_list)
        return right_date

    # 获取去掉日期的字符串
    def get_filename_without_date(self, subject: str, regex='\d{4}[-/]?\d{2}[-/]?\d{2}'):
        right_date = self.get_date(subject, regex)
        if right_date != '':
            res_file_name = re.sub(str(right_date), '', subject)
        else:
            res_file_name = subject
        return res_file_name


if __name__ == '__main__':
    # regex_str = '\d{4}[-/]?\d{2}[-/]?\d{2}'
    # subject = '0011000048久铭专享6号20220217.txt'
    # subject = '上海久铭投资管理有限公司－久铭1号私募证券投资基金_661026000005_股票期权对账单(人民币)_20220217.xls上海久铭投资管理有限公司－久铭1号私募证券投资基金_661026000005_股票期权对账单(人民币)_20220217.xls'
    subject = '217739久铭价值1号私募证券投资基金20211221.xlsx'
    tf = Transform_FileName()
    # subject = '0011000048久铭专享6号20220217.txt'
    if tf.get_date(subject) == '':
        print("果然空窜")
    print(tf.get_date(subject))
    print(tf.get_filename_without_date(subject, '\d{4}\d{2}\d{2}'))

    # regex = re.compile(regex_str)
    # matches_list = regex.findall(subject)
    # right_date = get_right_date(matches_list)
    # print(type(right_date))
    # print(right_date)
    # res_file_name = re.sub(right_date, '', subject)
    # print(type(res_file_name))
    # print(res_file_name)

# result= re.sub(regex, '', subject)
# print(result)

# 其他格式匹配. 如2016-12-24与2016/12/24的日期格式.
# date_reg_exp = re.compile('\d{4}[-/]?\d{2}[-/]?\d{2}')
#
# test_str = """
#      平安夜圣20221201诞节2016-12-24的日子与去年2015/12/24的是有不同哦.
#      """
# # 根据正则查找所有日期并返回
# res = re.search(date_reg_exp,test_str).group(0)
# # matches_list=date_reg_exp.findall(test_str)
# #
# # # 列出并打印匹配的日期
# # for match in matches_list:
# #   print (match)
# print(res)

# 20220217的文件目录下，都是对账结束日为20220217的对账单【有的是解压后的子目录，需二次遍历，最终在这目录下都是这一天收盘后的对账单】
# 遍历该文件夹下的所有文件，发现文件名能与act_suppose_arrive匹配的，就把该文件名记录到实到表。
