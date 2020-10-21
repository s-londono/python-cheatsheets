import datetime

# Parse time string
t1 = datetime.datetime.strptime("2020-10-21 10:12:03", "%Y-%m-%d %H:%M:%S")
t2 = datetime.datetime.strptime("2020-10-25 23:47:58", "%Y-%m-%d %H:%M:%S")

# Make a time interval
i1 = datetime.timedelta(hours=2, minutes=3, seconds=25)
i2 = datetime.timedelta(weeks=2)

# Time intervals can be added to times
t3 = t1 + i1
t4 = t2 - i2

print(t3)
print(t4)

# Format a time as string, with a specific format
print(t3.strftime("%Y-%m-%d %H:%M:%S"))
print(t4.strftime("%Y.%m.%d %H:%M:%S"))
