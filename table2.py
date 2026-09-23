import math

a = 0.0
b = 0.2
h = 0.02
d = 0.001

x = a
while x <= b:
    total_sum = 0.0
    n = 1
    
    while True:
        term = (x ** (2 * n) - 1) / math.factorial(2 * n - 1)
        total_sum += term
        
        if abs(term) < d:
            break
            
        n += 1

    print(total_sum)
    x += h