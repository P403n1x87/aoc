# https://adventofcode.com/2021/day/18

import os
from copy import deepcopy


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


def reduce(n):
    def explode(e, p=""):
        def add(v, n, p, i):
            try:
                c = n
                for _ in p[: p.rindex(str(1 - i))]:
                    c = c[int(_)]
            except ValueError:
                return
            if isinstance(c[i], int):
                c[i] += v
                return
            c = c[i]
            while not isinstance(c[1 - i], int):
                c = c[1 - i]
            c[1 - i] += v

        if isinstance(e, int):
            return False

        if len(p) == 3:
            for i, m in enumerate(e):
                if not isinstance(m, int):
                    (l, h), fp = m, p + str(i)
                    e[i] = 0
                    add(h, n, fp, 1)
                    add(l, n, fp, 0)
                    return True

        for i, m in enumerate(e):
            if explode(m, p + str(i)):
                return True

        return False

    def split(e):
        for i, v in enumerate(e):
            if isinstance(v, int):
                if v >= 10:
                    lo = v >> 1
                    e[i] = [lo, v - lo]
                    return True
            else:
                if split(v):
                    return True
        return False

    while explode(n) or split(n):
        pass

    return n


def mag(n):
    if isinstance(n, int):
        return n
    return sum(a * mag(b) for a, b in zip([3, 2], n))


def solve(datafile="input.txt"):
    ns = [eval(_.strip()) for _ in open(resolve(datafile))]

    a = ns[0]
    for _ in ns[1:]:
        a = reduce(deepcopy([a, _]))
    return mag(a), max(mag(reduce(deepcopy([a, b]))) for a in ns for b in ns)


def test():
    assert solve("test.txt") == (4140, 3993)


test()
print(solve())
