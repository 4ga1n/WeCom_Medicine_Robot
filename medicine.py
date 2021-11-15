import datetime
import math
import os
from notification import send_notify
import settings

mark_date = datetime.datetime.strptime(settings.MARK, '%Y-%m-%d')

def is_time_not_disterb(date):
    if date.hour < 7:
        return True

def is_today_eaten(date):
    filename = settings.DB_PATH + date.strftime("%Y-%m-%d") + ".txt"
    return os.path.isfile(filename)

def eat(date):
    filename = settings.DB_PATH + date.strftime("%Y-%m-%d") + ".txt"
    with open(filename,'w') as f:
        f.write("True")

def fake_date(date):
    if date.hour < 12:
        d = datetime.timedelta(days=-1)
        return date + d
    else:
        return date

def need_to_eat(date):
    today = datetime.datetime.now()
    days = (today - mark_date).days % 28
    x = math.floor(days/7) + 1
    y = days % 7 + 1
    if days < 21:
        return True
    else:
        return False

def check_today(date):
    if is_today_eaten(date):
        print("今天已经吃药了")
        return
    days = (date - mark_date).days % 28
    x = math.floor(days/7) + 1
    y = days % 7 + 1
    if y == 5:
        send_notify("记得约看牙的号",settings.TOUSER)
    if days < 21:
        print(f"吃药了吗？今天吃第{x}周周{y}的药")
        send_notify(f"吃药了吗？今天吃第{x}周周{y}的药", settings.TOUSER)
        if date.hour < 12:
            send_notify(f"猪没吃药，今天吃第{x}周周{y}的药", settings.REMIND_USER)
        if y == 5:
            send_notify("记得约看牙的号",settings.TOUSER)
        if days == 0:
            print("如果修改吃药周期请修改代码")
            send_notify("如果修改吃药周期请修改代码",settings.TOUSER)
    elif days == 21:
        print("今天不用吃药,如果修改吃药周期请修改代码")
        send_notify("今天不用吃药,如果修改吃药周期请修改代码",settings.TOUSER)
        eat(date)
    else:
        print("今天不用吃药")
        send_notify("今天不用吃药",settings.TOUSER)
        eat(date)

if __name__ == "__main__":
    today = fake_date(datetime.datetime.now())
    check_today(today)

