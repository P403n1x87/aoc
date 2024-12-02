# https://adventofcode.com/2024/day/2

import typing as t

from aoctk.input import get_tuples


def is_safe(report: tuple[int]) -> bool:
    return any(
        (
            all(1 <= d * _ <= 3 for _ in set(a - b for a, b in zip(report, report[1:])))
            for d in (1, -1)
        )
    )


def solve(data, cond) -> int:
    return sum(cond(r) for r in get_tuples(data, transformer=int))


def part_one(data="input.txt"):
    return solve(data, is_safe)


def part_two(data="input.txt"):
    return solve(
        data,
        lambda r: is_safe(r)
        or any(is_safe(s) for s in (r[0:i] + r[i + 1 :] for i in range(len(r)))),
    )


def test():
    assert (_ := part_one("test.txt")) == 2, _
    assert (_ := part_two("test.txt")) == 4, _
