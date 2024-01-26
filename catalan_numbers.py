"""
Generator for Catalan numbers
https://en.wikipedia.org/wiki/Catalan_number
"""

import math
from decimal import *


LENGTH = 16
PRECISION = 192


def i_catalan(n):
    return math.factorial(2 * n) // math.factorial(n + 1) // math.factorial(n)


def r_catalan(n):
    if n < 2:
        return 1
    res = 0
    for i in range(n):
        res += r_catalan(i) * r_catalan(n - i - 1)
    return res


def division():
    nb = 500000
    getcontext().prec = PRECISION
    result = nb - (Decimal(nb) ** 2 - 1).sqrt()
    print('\033[92m' + f'{nb} - ({nb}^2 - 1)^0.5' + '\033[38m')
    print(result, '\n')
    splits = ['1']
    n = 12
    for idx in range(8, len(str(result)), n):
        splits.append(str(result)[idx:idx + n].lstrip('0'))
    print('\033[92m' + 'd_catalan' + '\033[38m')
    for i, nb in enumerate(splits):
        print('{:02}: '.format(i + 1) + nb)


for func in (i_catalan, r_catalan):
    print('\033[92m' + func.__name__ + '\033[38m')
    for j in range(LENGTH):
        print('{:02}: '.format(j + 1) + str(func(j)))
    print('')
division()
