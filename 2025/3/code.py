# https://adventofcode.com/2025/day/3

from aoctk.func import argmax
from aoctk.input import get_lines


def jolts(pack: str, n: int) -> int:
    a, i, m = 0, -1, len(pack)
    for k in range(n):
        a = a * 10 + int(pack[(i := argmax(pack[i + 1 : m + k + 1 - n]) + i + 1)])
    return a


def part_one(data="input.txt"):
    return sum(jolts(p, 2) for p in get_lines(data))


def part_two(data="input.txt"):
    return sum(jolts(p, 12) for p in get_lines(data))


def test():
    assert (_ := part_one("test.txt")) == 357, _
    assert (_ := part_two("test.txt")) == 3121910778619, _
