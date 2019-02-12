a = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M")).split()
b = [int(i) for i in a[0].split("-")]
c = [int(i) for i in a[1].split(":")]
summary = c[0] * 60 + c[1] + b[1] * 24 * 60 + b[1] * 24 * 30 * 60 + b[2] * 365 * 24 * 60
