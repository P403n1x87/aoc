# https://adventofcode.com/2021/day/7

import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


def round(n):
    return int(n) if n - int(n) < 0.5 else int(n) + 1


def median(l):
    return l[len(l) >> 1] if len(l) % 1 else (l[(len(l) >> 1) - 1] + l[len(l) >> 1]) / 2


def solve(datafile="input.txt"):
    ps = sorted([int(_) for _ in open(resolve(datafile)).read().strip().split(",")])

    med = median(ps)
    p1, p2 = round(med), round(sum(ps) / len(ps) - med / (2 * len(ps)))

    return (
        sum(abs(_ - p1) for _ in ps),
        sum((abs(_ - p2) * (abs(_ - p2) + 1)) >> 1 for _ in ps),
    )


def test():
    assert solve("test.txt") == (37, 168)


test()
print(solve())
