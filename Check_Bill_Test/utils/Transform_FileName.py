"""
@Author: Wave Zhou
"""
import re, datetime

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
    subject = '上海久铭投资管理有限公司－久铭1号私募证券投资基金_661026000005_股票期权对账单(人民币)_20220217.xls上海久铭投资管理有限公司－久铭1号私募证券投资基金_661026000005_股票期权对账单(人民币)_20220217.xls'
    # subject = '8034648_21800127.pdf'
    tf = Transform_FileName()
    # subject = '0011000048久铭专享6号20220217.txt'
    if tf.get_date(subject) == '':
        print("果然空窜")
    print(tf.get_date(subject))
    print(tf.get_filename_without_date(subject))

# 20220217的文件目录下，都是对账结束日为20220217的对账单【有的是解压后的子目录，需二次遍历，最终在这目录下都是这一天收盘后的对账单】
# 遍历该文件夹下的所有文件，发现文件名能与act_suppose_arrive匹配的，就把该文件名记录到实到表。
