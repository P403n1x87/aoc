# https://adventofcode.com/2025/day/4

from aoctk.data import D8
from aoctk.input import get_bounded_2d_grid


def part_one(data="input.txt"):
    rolls = get_bounded_2d_grid(data)
    return sum(sum(r + d in rolls for d in D8) < 4 for r in rolls)


def part_two(data="input.txt"):
    rolls, a = get_bounded_2d_grid(data), 0
    while lifted := {r for r in rolls if sum(r + d in rolls for d in D8) < 4}:
        a += len(lifted)
        rolls.remove(lifted)
    return a


def test():
    assert (_ := part_one("test.txt")) == 13, _
    assert (_ := part_two("test.txt")) == 43, _
