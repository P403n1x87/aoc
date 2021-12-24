# https://adventofcode.com/2021/day/24

import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


def monad(ins):
    cs, s = [], []
    for i in range(14):
        for _ in range(4):
            next(ins)
        d, a = next(ins), int(next(ins))
        for _ in range(9):
            next(ins)
        b = int(next(ins))
        for _ in range(2):
            next(ins)

        if d == "1":
            s.append((i, b))
        else:
            j, e = s.pop()
            cs.append((i, j, e + a))

    lo, hi = [None] * 14, [None] * 14
    for i, j, d in cs:
        h, l = 9 - max(d, 0), 1 - min(d, 0)
        hi[j], lo[j], hi[i], lo[i] = h, l, h + d, l + d

    return "".join([str(_) for _ in hi]), "".join([str(_) for _ in lo])


def solve(datafile="input.txt"):
    return monad((_.strip().split()[-1] for _ in open(resolve(datafile))))


print(solve())
