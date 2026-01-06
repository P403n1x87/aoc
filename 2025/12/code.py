# https://adventofcode.com/2025/day/12

from math import prod

from aoctk.input import get_groups


def part_one(data="input.txt"):
    *_, areas = get_groups(data)
    c = 0
    for area in areas:
        ds, _, ps = area.partition(": ")
        c += eval(ps.replace(" ", "+")) * 9 - prod(map(int, ds.split("x"))) < 3
    return c


def part_two(data="input.txt"):
    pass


def test():
    assert (_ := part_one("test.txt")) == 2, _
    assert (_ := part_two("test.txt")) is None, _
