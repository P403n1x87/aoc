# https://adventofcode.com/2023/day/12

from functools import cache

from aoctk.input import get_lines


def combos(sf: str, gs: list[int]) -> int:
    @cache
    def dp(s: int = 0, g: int = 0, r: int = 0) -> int:
        if g == len(gs):
            return not sf.count("#", s)
        if s == len(sf):
            return g + 1 == len(gs) and r == gs[g]

        return ((dp(s + 1, g, r + 1) if r < gs[g] else 0) if sf[s] != "." else 0) + (
            ((dp(s + 1, g + 1, 0) if r == gs[g] else 0) if r else dp(s + 1, g, 0))
            if sf[s] != "#"
            else 0
        )

    return dp()


def solve(data: str, n: int) -> int:
    return sum(
        combos("?".join([sf] * n), [int(n) for n in ",".join([gs] * n).split(",")])
        for sf, gs in (_.split(" ", 1) for _ in get_lines(data))
    )


def part_one(data="input.txt"):
    return solve(data, 1)


def part_two(data="input.txt"):
    return solve(data, 5)


def test():
    assert part_one("test.txt") == 21
    assert part_two("test.txt") == 525152
