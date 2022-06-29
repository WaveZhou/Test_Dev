# _*_ coding: utf-8 _*_
import os, shutil

from MysqlProxy import MysqlProxy
import datetime

base = "D:\\Test\\"
target = 'D:\\Target\\'

# 很明显，在刚接受这个对账单后台更新的项目时，我的想法很22222
wait_to_transfer_str_guo_tou = '国投安信期货账户'
wait_to_transfer_str_zxjt_lr = '中信建投两融账户'


def classify_dir_to_trade_date(date):
    import datetime
    from MysqlProxy import MysqlProxy
    fridge_date = date.replace('-', '')
    print(fridge_date)
    print(date)
    str = '收件日'
    origin = base + str + fridge_date + ' 当天'
    wait_to_transfer_trade_today = '久铭产品交割单' + fridge_date

    for item in os.listdir(origin):
        print(item)
        if item == wait_to_transfer_str_guo_tou or item == wait_to_transfer_trade_today:
            sub_target = '交易日' + fridge_date
            if os.path.exists(os.path.join(target, sub_target, item)):
                os.remove(os.path.join(target, sub_target, item))
            if not os.path.isdir(os.path.join(target, sub_target)):
                os.mkdir(os.path.join(target, sub_target))

            shutil.copytree(os.path.join(origin, item), os.path.join(target, sub_target), dirs_exist_ok=True)

    mp = MysqlProxy()
    find_next_day(date, mp, fridge_date, wait_to_transfer_trade_today)


#
def find_next_day(date, mp, fridge_date, wait_to_transfer_trade_today):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    date = date + datetime.timedelta(days=1)
    res = recuirse_next_day(date, mp)
    flag = True
    if res is not None:
        flag = False
    print(res)
    if flag:
        print("不是交易日的情况")
        # 如果不是交易日，则判断这个当日目录下是否存在wait_to_transfer_trade_today，存在的话，则遍历这个目录，这个目录下目录名不为清算数据的目录，迁移到指定交易日
        # 把久铭产品交割单brige移动到交易日
        if not isinstance(date, str):
            date = datetime.datetime.strftime(date, '%Y-%m-%d')
        res = find_next_day(date, mp, fridge_date, wait_to_transfer_trade_today)
        print(res)
        # res = mp.get_one(sql, [date)
    else:
        # 则直接迁移里面的国投安信期货账户和wait_to_transfer_trade_today到指定交易日目录
        date = datetime.datetime.strftime(date, '%Y-%m-%d')
        date = date.replace("-", "")
        origin = base + '收件日' + date + ' 当天'
        for item in os.listdir(origin):
            print(item)
            sub_target = '交易日' + fridge_date
            if item == wait_to_transfer_str_zxjt_lr or item == wait_to_transfer_trade_today:
                if not os.path.exists(os.path.join(target, sub_target)):
                    os.mkdir(os.path.join(target, sub_target))
                shutil.copytree(os.path.join(origin, item), os.path.join(target, sub_target), dirs_exist_ok=True)
                # if os.path.exists(os.path.join(target,sub_target,item)):
                #     os.remove(os.path.join(target,sub_target,item))
                # shutil.copytree(os.path.join(origin, item), os.path.join(target, sub_target))
                # shutil.copytree(os.path.join(origin,item),os.path.join(target,sub_target))
    # shutil.copy(os.path.join(target,sub_target,item))

    # print("是交易日哦")
    # next_day = int(date) + 1
    # print(next_day)
    # 判断next_day是否为交易日，是，则直接迁移里面的中信建投两融账户和wait_to_transfer_trade_today到指定交易日目录


def recuirse_next_day(date, mp):
    import datetime
    sql = 'select * from trade_date where date = %s'
    print(date)
    res = mp.get_one(sql, [date])
    return res


# day = datetime.datetime.strptime('2020-2-18 00:00:00', '%Y-%m-%d %H:%M:%S')
classify_dir_to_trade_date('2022-02-17')
# mp = MysqlProxy()
# date = datetime.datetime.strptime('2022-02-18 ', '%Y-%m-%d ')
# print(type(date))
# print(date)
# sql = 'select * from trade_date where date = %s'
# #date = date + datetime.timedelta(days=3)
# print(date)
# res = mp.get_one(sql,[date])
# print(res)
