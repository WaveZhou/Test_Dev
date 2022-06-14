import logging

#创建一个logger日志对象
logger = logging.getLogger('test_logger')
logger.setLevel(logging.DEBUG)    #设置默认的日志级别

#创建日志格式对象
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


#创建StreamHandler对象
sh = logging.StreamHandler()
#StreamHandler对象自定义日志级别
sh.setLevel(logging.DEBUG)
#StreamHandler对象自定义日志格式
sh.setFormatter(formatter)

logger.addHandler(sh)    #logger日志对象加载StreamHandler对象
#日志输出
logger.info('newdream')
