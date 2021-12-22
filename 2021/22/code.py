# https://adventofcode.com/2021/day/22

import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


def inter(ca, cb):
    return (
        [(max(e[0], f[0]), min(e[1], f[1])) for e, f in zip(ca, cb)]
        if not any(e[1] < f[0] or f[1] < e[0] for e, f in zip(ca, cb))
        else None
    )


def v(c):
    a = 1
    for l, h in c:
        a *= h - l + 1
    return a


def solve(datafile="input.txt"):
    cubes = []
    for _ in open(resolve(datafile)):
        o, _, cs = _.strip().partition(" ")
        c = [
            tuple([int(n) for n in _.split("..")])
            for _ in (_.partition("=")[-1] for _ in cs.split(","))
        ]
        for _, w in list(cubes):
            if i := inter(_, c):
                cubes.append((i, -1 * w))
        if o == "on":
            cubes.append((c, 1))

    return sum(v(c) * w for c, w in cubes)


def test():
    assert solve("test.txt") == 590784
    assert solve("test2.txt") == 2758514936282235


test()
print(solve("input.txt"))
print(solve("input2.txt"))
