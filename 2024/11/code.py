# https://adventofcode.com/2024/day/11

from functools import cache
from typing import Iterable

from aoctk.input import get_tuples


def solve(data: str, t: int) -> int:
    (ss,) = get_tuples(data, transformer=int)

    def e(s: int) -> Iterable[int]:
        if s == 0:
            yield 1
        elif len(t := str(s)) % 2 == 0:
            yield from [int(t[: len(t) // 2]), int(t[len(t) // 2 :])]
        else:
            yield s * 2024

    @cache
    def n(s: int, t: int) -> int:
        return 1 if t == 0 else sum(n(_, t - 1) for _ in e(s))

    return sum(n(_, t) for _ in ss)


def part_one(data="input.txt"):
    return solve(data, 25)


def part_two(data="input.txt"):
    return solve(data, 75)


def test():
    assert (_ := part_one("test.txt")) == 55312, _
    assert (_ := part_two("test.txt")) == 65601038650482, _
