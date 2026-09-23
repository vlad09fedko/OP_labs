import math

a = 3
b = 8
h = 0.2

x = a
while x <= b:
    try:
        if x < 5:
            print(math.log(abs(math.log(abs(math.log(x, 3)), 4)), 5))
        if 5 <= x < 7:
            print(1/(x ** 2 + 16))
        if x >= 7:
            print(math.log(x) + math.cos(x))
        x += h
    except ValueError:
        print('Value error!')
        break