import datetime
import math

today = datetime.datetime.now()
mark = "2021-08-15"
mark_date = datetime.datetime(2021, 8, 15)

base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(60)]
for i in date_list:
    print(i)
    days = (i - mark_date).days % 28
    if days < 21:
        x = math.floor(days/7) + 1
        y = days % 7 + 1
        print(f"吃药了吗？今天吃第{x}周周{y}的药")
        if days == 0:
            print("如果修改吃药周期请修改代码")
    elif days == 21:
        print("今天不用吃药,如果修改吃药周期请修改代码")
    else:
        print("今天不用吃药")
