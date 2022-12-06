# https://adventofcode.com/2022/day/6

from aoctk.input import get_lines


def solve(n, data):
    (stream,) = get_lines(data)

    for i, c in enumerate(
        len(set(stream[i : i + n])) == n for i in range(len(stream) - n)
    ):
        if c:
            return i + n


def part_one(data="input.txt"):
    return solve(4, data)


def part_two(data="input.txt"):
    return solve(14, data)


def test():
    assert part_one("test.txt") == 7
    assert part_two("test.txt") == 19
