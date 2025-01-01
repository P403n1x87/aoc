# https://adventofcode.com/2024/day/22

from aoctk.func import window
from aoctk.input import get_lines


def rand(v: int, n: int) -> int:
    a = v
    for _ in range(n):
        a = (a ^ (a << 6)) % 16777216
        a = (a ^ (a >> 5)) % 16777216
        a = (a ^ (a << 11)) % 16777216
    return a


def dm(v: int, n: int) -> int:
    a = v
    vs = [a % 10]
    for _ in range(n - 1):
        a = (a ^ (a << 6)) % 16777216
        a = (a ^ (a >> 5)) % 16777216
        a = (a ^ (a << 11)) % 16777216
        vs.append(a % 10)
    ds = [b - a for a, b in zip(vs, vs[1:])]
    wm = {}
    for i, w in enumerate(window(ds, 4), 4):
        if w[-1] > 0 and w not in wm:  # skip if the last element is negative
            wm[w] = vs[i]
    return wm


def part_one(data="input.txt"):
    return sum(rand(int(ln), 2000) for ln in get_lines(data))


def part_two(data="input.txt"):
    dms = [dm(int(ln), 2000) for ln in get_lines(data)]
    return max(sum(d.get(k, 0) for d in dms) for k in {k for d in dms for k in d})


def test():
    assert (_ := part_one("test.txt")) == 37327623, _
    assert (_ := part_two("test2.txt")) == 23, _
