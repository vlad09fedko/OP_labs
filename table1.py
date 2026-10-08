import math

a = 3
b = 8
h = 0.2

x = a
while x <= b:
    try:
        if x < 5:
            print( math.log( abs(math.log( abs(math.log(x, 3) ), 4) ), 5) ) # log3(3) = 1 ; log4(1) = 0 ; log5(0) doesn't exist
        if 5 <= x < 7:
            print(1/(x ** 2 + 16))
        if x >= 7:
            print(math.log(x) + math.cos(x))
        x += h
        x = round(x, 1)
        print(f'x = {x}') 
    except ValueError:
        print('Value error!')
        break