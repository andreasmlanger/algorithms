"""
https://opensource.com/article/20/6/python-passwords
https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
When it exists (both numbers relatively prime), a modular multiplicative inverse is unique
"""

from mod import Mod
import os
import random
import sys


MERSENNE = [0, 2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607]  # Mersenne primes
NR = 13
SECRET = 'xyz'


def int_from_bytes(s):
    if type(s) is not bytes:
        s = s.encode('utf-8')
    acc = 0
    for b in s:
        acc = acc * 256
        acc += b
    return acc


def int_to_string(i):
    s = ''
    while i > 1:
        r = int(i) % 256
        s = chr(r) + s
        i = (i - r) // 256
    return s


prompt = 'What is your secret? (Default: ' + '\033[92m' + SECRET + '\033[0m) '
secret = input(prompt)
if secret == '':
    secret = SECRET

secret = int_from_bytes(secret)


P = 2 ** MERSENNE[NR] - 1  # 13th Mersenne prime

if secret > P:  # Make sure secret is smaller than P
    sys.exit('Too small Mersenne prime')
else:
    print('Secret: ' + '\033[92m' + str(secret) + '\033[0m', end='')
    print(' | Mersenne prime: ' + '\033[92m' + str(P) + '\033[0m')

secret = Mod(secret, P)

polynomial = [secret]
for _ in range(2):
    polynomial.append(Mod(int_from_bytes(os.urandom(16)), P))

print('Polynomial:', polynomial)  # 3 coefficients of polynomial a + bx + cx^2


def evaluate(coefficients, x_):
    acc = 0
    power = 1
    for c in coefficients:
        acc += c * power
        power *= x_
    return acc


shards = {}
for j in range(5):
    x = Mod(int_from_bytes(os.urandom(16)), P)
    y = evaluate(polynomial, x)
    shards[j] = (x, y)

# Delete two random shards
n1, n2 = random.sample(range(5), 2)
del shards[n1]
del shards[n2]

for k, v in shards.items():
    print(f'Shard ' + '\033[92m' + str(k) + '\033[0m' + ': ' + str(v))

retrieved_shards = list(shards.values())


def retrieve_original(shrds):  # Lagrange interpolation
    xj_s = [s[0] for s in shrds]
    acc = 0
    for i in range(len(shrds)):
        others = list(xj_s)
        xi = others.pop(i)
        factor = 1
        for xj in others:
            factor *= xj // (xj - xi)  # (0 - xj) / (xi - xj)  |  floor division = inverse
        acc += factor * shrds[i][1]  # yi
    return acc  # P(x) at x = 0: first coefficient (constant)


retrieved_secret = int(retrieve_original(retrieved_shards))

print('Retrieved secret: ' + '\033[36m' + str(int_to_string(retrieved_secret)) + '\033[0m')
