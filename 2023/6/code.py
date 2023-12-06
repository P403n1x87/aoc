# https://adventofcode.com/2023/day/6

from math import floor, prod

from aoctk.input import get_lines


def w(t, d):
    return 2 * floor((t + (t**2 - 4 * (d + 1)) ** 0.5) / 2) - t + 1


def part_one(data="input.txt"):
    return prod(
        w(t, d)
        for t, d in zip(
            *(
                [int(_) for _ in line.partition(":")[-1].split()]
                for line in get_lines(data)
            )
        )
    )


def part_two(data="input.txt"):
    return w(
        *(int(line.partition(":")[-1].replace(" ", "")) for line in get_lines(data))
    )


def test():
    assert part_one("test.txt") == 288
    assert part_two("test.txt") == 71503
