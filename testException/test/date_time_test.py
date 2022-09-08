import datetime
datetime_d =datetime.datetime.now()
print(datetime_d)
print(datetime_d.date())
date_obj = datetime_d.date()
rs = datetime.datetime.strftime(date_obj,'%Y-%m-%d')

print(type(rs))
print(rs)
