# https://adventofcode.com/2021/day/11

import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


def solve(datafile="input.txt"):
    ADJS = {complex(i, j) for i in range(-1, 2) for j in range(-1, 2)} - {0j}

    cave = {
        complex(i, j): int(v)
        for i, r in enumerate(
            enumerate((int(_) for _ in line.strip()))
            for line in open(resolve(datafile))
        )
        for j, v in r
    }

    def inc(cave, z):
        over = set()
        for e in ADJS:
            if cave.get(z + e, 0):
                cave[z + e] += 1
                if cave[z + e] >= 10:
                    over.add(z + e)
        return over

    fs = 0
    for s, _ in enumerate(iter(int, 1)):
        for z in cave:
            cave[z] += 1

        off = {z for z, v in cave.items() if v == 10}
        while off:
            n = off.pop()
            cave[n] = 0
            off |= inc(cave, n)
            if s < 100:
                fs += 1

        if set(cave.values()) == {0}:
            break

    return fs, s + 1


def test():
    assert solve("test.txt") == (1656, 195)


test()
print(solve())
