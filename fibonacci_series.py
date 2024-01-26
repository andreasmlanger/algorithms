"""
Different generators for Fibonacci series
"""

import time


LENGTH = 34


def print_elapsed_time(t):
    if t > 1:
        print('\033[92m' + str(round(t, 3)) + ' seconds\n\033[38m')
    else:
        print('\033[92m' + str(round(1000 * t, 2)) + ' milliseconds\n\033[38m')


def f_fibonacci(n):  # functional
    phi = (1 + 5 ** 0.5) / 2  # golden ratio
    return int(round(phi ** (n + 1) / 5 ** 0.5, 0))


def i_fibonacci(n):  # inductive
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return a + b


def r_fibonacci(n):  # recursive
    if n < 2:
        return 1
    return r_fibonacci(n - 1) + r_fibonacci(n - 2)


for func in (f_fibonacci, i_fibonacci, r_fibonacci):
    start = time.time()
    for j in range(LENGTH):
        print(func(j), end=', ')
    print('...\n\033[92m' + func.__name__ + ' - ', end='')
    print_elapsed_time(time.time() - start)
