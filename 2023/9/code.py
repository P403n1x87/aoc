# https://adventofcode.com/2023/day/9

from aoctk.input import get_lines


def infer(s: list[int]) -> int:
    ends = [s[-1]]
    while s[0] != s[-1]:  # faster than checking all numbers
        s = [b - a for a, b in zip(s, s[1:])]
        ends.append(s[-1])
    return sum(ends)


def solve(data: str, backward: bool = False) -> int:
    return sum(
        infer(_[::-1] if backward else _)
        for _ in ([int(_) for _ in line.split()] for line in get_lines(data))
    )


def part_one(data="input.txt"):
    return solve(data)


def part_two(data="input.txt"):
    return solve(data, backward=True)


def test():
    assert part_one("test.txt") == 114
    assert part_two("test.txt") == 2
