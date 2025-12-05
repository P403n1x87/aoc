# https://adventofcode.com/2025/day/5

from aoctk.data import Range, weighted_union_size
from aoctk.input import get_groups


def part_one(data="input.txt"):
    r, i = get_groups(data)
    ranges = [Range.parse(_) for _ in r]
    ingredients = [int(_) for _ in i]
    return sum(any(i in r for r in ranges) for i in ingredients)


def part_two(data="input.txt"):
    r, _ = get_groups(data)
    return weighted_union_size(Range.weighted_union([Range.parse(_) for _ in r]))


def test():
    assert (_ := part_one("test.txt")) == 3, _
    assert (_ := part_two("test.txt")) == 14, _
