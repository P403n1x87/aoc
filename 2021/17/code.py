# https://adventofcode.com/2021/day/17

import os
from functools import cache


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


def solve(datafile="input.txt"):
    @cache
    def s(a):
        return a * (a + 1) >> 1 if a > 0 else 0

    def x(t, v):
        return s(v) - s(v - t)

    with open(resolve(datafile)) as f:
        (xl, xh), (yl, yh) = (
            tuple(int(_) for _ in p[2:].split(".."))
            for p in f.readline().strip().partition(": ")[-1].split(", ")
        )
        vs = set()
        for vy in range(-yl - 1, yl - 1, -1):
            t, y, vyt, ts = 2 * vy + 1, 0, -vy - 1, []
            while y > yl:
                y += vyt
                vyt -= 1
                t += 1
                if yl <= y <= yh:
                    ts.append(t)
            if not ts:
                continue

            for vx in range(xh, int((-1 + (1 + 8 * xl) ** 0.5) / 2) - 1, -1):
                if any(xl <= x(t, vx) <= xh for t in ts):  # TODO[perf]: this is slow
                    vs.add(complex(vx, vy))

        return s(int(max(_.imag for _ in vs))), len(vs)


def test():
    assert solve("test.txt") == (45, 112)


test()
print(solve())
