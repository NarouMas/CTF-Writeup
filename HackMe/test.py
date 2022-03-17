x = 5930
n = 57495273401700408170574007939962125332744354406174743101833215448581817805393

def foo(num):
    if num < 2:
        return 1
    return foo(num - 1) * num % n

for i in range(100):
    print(i, ' ', foo(i))

import math
math.factorial()