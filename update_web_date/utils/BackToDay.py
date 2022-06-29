import datetime
import time

from update_web_date.utils.DataSource import DataSource


# Create your tests here.
# 本地化使用的一个类，因为连接的是我本地数据库的test表
class BackToDay(object):
    def __init__(self, back_day, rely_day):
        self.valid_count = 0
        self.back_day = back_day
        self.rely_day = rely_day
        self.to_day = ''
        self.conn = None
        self.init_load()

    def init_load(self):
        data_dict = dict()
        data_dict['host'] = '127.0.0.1'
        data_dict['user'] = 'root'
        data_dict['passwd'] = '123456'
        data_dict['db'] = 'test'
        self.conn = DataSource(data_dict)

    def primary(self):
        # stamp = datetime.datetime.today().date()
        # 不采用上述方式的当天日期，把日期作为参数传入
        # print(stamp.strftime("%Y-%m-%d"))
        # print(type(stamp.strftime("%Y-%m-%d")))
        # stamp = datetime.date(2021,10,26)
        self.pop_to_day(self.rely_day.strftime("%Y-%m-%d"), self.back_day)
        return self.to_day[0]['date']

    def pop_to_day(self, currentday, back_day):
        currentday = self.sub_one_day(currentday)
        sql = "SELECT * FROM test.trade_date td where td.date = %s"
        result_list = self.conn.get_list(sql, currentday)
        if len(result_list) > 0:
            self.valid_count = self.valid_count + 1
            if self.valid_count == self.back_day:
                self.to_day = result_list
            else:
                self.pop_to_day(currentday, self.back_day)
        else:
            self.pop_to_day(currentday, self.back_day)

    def sub_one_day(self, day):
        # datetime.datetime.strptime(day, "%Y-%m-%d").date()
        cur_day = datetime.datetime.strptime(day, '%Y-%m-%d')
        yesterday_stamp = cur_day.timestamp() - (60 * 60 * 24)
        # print(yesterday_stamp)
        date_yesterday = time.localtime(yesterday_stamp)
        return time.strftime('%Y-%m-%d', date_yesterday)


if __name__ == '__main__':
    accord_day = datetime.date(2022, 6, 5)
    pt = BackToDay(2, accord_day)
    print(pt.primary())
    day = datetime.date.strftime(pt.to_day[0]['date'], "%Y-%m-%d")
    print(day)
