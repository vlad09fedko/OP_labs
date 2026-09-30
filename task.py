"""
Варіант 23
Перетин двох послідовностей
Враховуючи дві послідовності A і B відповідно розміру N і M, 
надрукувати кількість елементів у перетині (або загальних елементів) двох послідовностей. 
Перетин двох послідовностей можна визначити як набір, що містить різні спільні елементи між двома послідовностями
"""

import random

# input data:
my_list1 = [random.randint(1, 100) for _ in range(100)]
my_list2 = [random.randint(1, 100) for _ in range(100)]

# decision
my_set1 = set(my_list1)
my_set2 = set(my_list2)
res = []

for num1 in my_set1:
    for num2 in my_set2:
        if(num1 == num2):
            res.append(num1)
            break

print(f'Count of intersection: {len(res)}\nResult: {res}')