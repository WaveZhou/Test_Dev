from WindPy import w

w.start() # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒

w.isconnected() # 判断WindPy是否已经登录成功
what = w.wsd('600030.SH','CLOSE','2016-01-01','2016-01-05','')
print(what)