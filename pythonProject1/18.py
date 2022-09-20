from random import *

a = [2, 3, 4, 6]
b = ['sin', 'cos', 'tg', 'ctg']
for i in range(41):
    c = '-' if randint(0, 1) == 0 else ''
    print(b[randint(0, 3)] + '(' + c + str(randint(1, 8)) + 'pi/' + str(a[randint(0, 3)]) + ')', end='          ')
    if (i + 1) % 3 == 0:
        print()