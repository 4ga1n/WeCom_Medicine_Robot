import datetime
from medicine import check_today,fake_date

d = datetime.timedelta(days=1)
d2 = datetime.timedelta(hours=1)

today = fake_date(datetime.datetime.now()+d+d2*14)
print(today)
check_today(today)

