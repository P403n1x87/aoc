# https://adventofcode.com/2022/day/2

from aoctk.input import get_lines


def solve(score, data="input.txt"):
    return sum(
        score(ord(a) - ord("A"), ord(x) - ord("X"))
        for a, x in (_.split(" ", 1) for _ in get_lines(data))
    )


def part_one(data="input.txt"):
    return solve(lambda t, u: u + 1 + (((u - t) % 3 + 1) % 3) * 3, data)


def part_two(data="input.txt"):
    return solve(lambda t, u: (t + u - 1) % 3 + 1 + u * 3, data)


def test():
    assert part_one("test.txt") == 15
    assert part_two("test.txt") == 12
