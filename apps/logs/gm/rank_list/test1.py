import datetime
now_date = datetime.date.today().strftime("%m/%d/%Y")
print now_date
now_date = datetime.datetime.strptime(now_date, "%m/%d/%Y").date()
print now_date
print datetime.date.today()
