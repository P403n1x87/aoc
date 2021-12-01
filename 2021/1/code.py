# https://adventofcode.com/2021/day/1

import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


def solve(ws, datafile="input.txt"):
    return (lambda ds=[int(_) for _ in open(resolve(datafile))]: sum(a < b for a, b in zip(ds, ds[ws:])))()


def test():
    assert solve(1, "test.txt") == 7
    assert solve(3, "test.txt") == 5


test()
print(solve(1))
print(solve(3))
