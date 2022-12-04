# https://adventofcode.com/2022/day/4

from aoctk.data import Range
from aoctk.input import get_tuples


def solve(cond, data):
    return sum(
        cond(*_) or cond(*_[::-1])
        for _ in get_tuples(data, ",", lambda d: Range(*(map(int, d.split("-")))))
    )


def part_one(data="input.txt"):
    return solve(Range.__contains__, data)


def part_two(data="input.txt"):
    return solve(Range.overlaps, data)


def test():
    assert part_one("test.txt") == 2
    assert part_two("test.txt") == 4
