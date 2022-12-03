# https://adventofcode.com/2022/day/3

from aoctk.input import get_lines, get_many


def solve(singletons):
    return sum(
        c - ord("A") + 27 if c <= ord("Z") else c - ord("a") + 1
        for s in singletons
        for c in (ord(_) for _ in s)
    )


def part_one(data="input.txt"):
    return solve(
        (set(r[: len(r) >> 1]) & set(r[len(r) >> 1 :]) for r in get_lines(data))
    )


def part_two(data="input.txt"):
    return solve((set.intersection(*g) for g in get_many(data, 3, set)))


def test():
    assert part_one("test.txt") == 157
    assert part_two("test.txt") == 70
