# https://adventofcode.com/2020/day/25

from math import ceil
from typing import Generator

MAGIC = 20201227


def read(source: str) -> tuple[int, int]:
    return tuple(int(_) for _ in open(source))


def dlog(a: int, b: int, m: int) -> int:
    sqm = ceil(m ** 0.5)
    tab = {pow(b, i, m): i for i in range(sqm)}
    g, r = pow(b, -sqm, m), a
    for i in range(m):
        if r in tab:
            return sqm * i + tab[r]
        r = (r * g) % m


def solve(source: str) -> int:
    c, d = read(source)
    ls = dlog(c, 7, MAGIC)
    return pow(d, ls, MAGIC)


assert 14897079 == solve("2020/25/test.txt")
print(solve("2020/25/input.txt"))