"""
Generator for Bernoulli numbers
https://en.wikipedia.org/wiki/Bernoulli_number
"""

from math import comb
from fractions import Fraction
from functools import lru_cache  # keeps result of function in cache if already calculated


@lru_cache
def bernoulli(n):
    if n == 0:
        return Fraction(1)
    elif n == 1:
        return Fraction(-1/2)
    s = Fraction(0)
    if n % 2:  # B(n) = 0 when n is odd
        return s
    for k in range(n):
        s += bernoulli(k) * comb(n, k) / (n + 1 - k)
    return -s


for i in range(10):
    print(f'B{2 * i}', bernoulli(2 * i).as_integer_ratio())
