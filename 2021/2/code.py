# https://adventofcode.com/2021/day/2

import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


def solve1(datafile="input.txt"):
    D = {"f": 1 + 0j, "d": 1j, "u": -1j}
    z = sum([D[d[0]] * int(m) for d, m in (_.strip().rsplit(" ", maxsplit=1) for _ in open(resolve(datafile)))])
    return int(z.real * z.imag)


def solve2(datafile="input.txt"):
    aim = 0
    z = 0j
    for d, m in (_.strip().rsplit(" ", maxsplit=1) for _ in open(resolve(datafile))):
        v = int(m)
        if d[0] == "d":
            aim += v
        elif d[0] == "u":
            aim -= v
        else:
            z += v * (1 + aim * 1j)

    return int(z.real * z.imag)


def test():
    assert solve1("test.txt") == 150
    assert solve2("test.txt") == 900


test()
print(solve1())
print(solve2())
