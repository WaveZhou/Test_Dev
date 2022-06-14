# _*_ coding: utf-8 _*_

"""
@Author: Wave Zhou
"""

import shutil, datetime, os, logging


# end_date_str = str(datetime.datetime.now().date())
# 'C:\\BackUp\\bugOut\\{}-{}-log.txt'.format(end_date_str, self.name)

class Log(object):
    def __init__(self, root_name: str):
        self.logger = logging.getLogger(root_name)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
        #                     filename=filename,
        #                     filemode='w',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
        #                     # a是追加模式，默认如果不写的话，就是追加模式
        #                     format=
        #                     '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        #                     # 日志格式
        #                     )
        self.logging = logging  # 也可以在构造方法中只保留这句，其他的在其他方法中调用slef.logging
        self.fh = None

    def output_log(self, info_map: dict):
        #logging.debug(info_map['message'])
        if not self.logger.handlers:
            fh = self.logging.FileHandler(info_map['file_name'], mode='w', encoding=None, delay=False)
            fh.setLevel(logging.INFO)
            fh.setFormatter(self.formatter)
            self.fh = fh
            self.logger.addHandler(fh)
        self.logger.info(info_map['message'])
        return self.logger

    def show_debug(self, message: str):
        logging.debug(message)

    def remove(self):
        self.logger.removeHandler(self.fh)


if __name__ == '__main__':
    message1 = 'zhangsan daoci yiyou'
    message2 = 'lisi daoci yiyou'

    logger = Log('ROOT_WAVE')
    # logger.output_log({'file_name': r'D:\BackUp\bugOut\log.txt', 'message': message1})
    # logger.output_log({'file_name': r'D:\BackUp\bugOut\log.txt', 'message': message1})
    # logger.output_log({'file_name': r'D:\BackUp\bugOut\log.txt', 'message': message1})
    # logger.remove()
    logger2 = Log('ROOT_Zhou')
    logger2.show_debug('agggggggggggg')
    # logger2.output_log({'file_name': r'D:\BackUp\watchOut\log.txt', 'message': message2})
    # logger2.output_log({'file_name': r'D:\BackUp\watchOut\log.txt', 'message': message2})
    # logger2.output_log({'file_name': r'D:\tem\watchOut\log.txt', 'message': message2})
