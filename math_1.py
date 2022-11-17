def ceil_1(a):
    if a >= 0:
        b = int(a)
    else:
        b = int(a) - 1
    return b


c = ceil_1(4.5)
print(c)
