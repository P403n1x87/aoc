# https://adventofcode.com/2021/day/21

import os
from functools import cache


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


@cache
def r(z: complex, s: complex = 0, v: int = 0, p: complex = 1, t: int = 21) -> complex:
    DM = ((3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1))
    if v:
        w = z + v * p
        z, pc = complex(w.real % 10 or 10, w.imag % 10 or 10), p.conjugate()
        s += p * (pc * z).real
        if (pc * s).real >= t:
            return p
        p = pc * 1j
    return sum(m * r(z, s, d, p, t) for d, m in DM)


def solve(datafile="input.txt"):
    z = r(complex(*(int(_.partition(": ")[-1]) for _ in open(resolve(datafile)))))
    return int(max(z.real, z.imag))


def test():
    assert solve("test.txt") == 444356092776315


test()
print(solve())
