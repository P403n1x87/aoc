# https://adventofcode.com/2023/day/9

from aoctk.func import iteratewhile
from aoctk.input import get_lines


def solve(data: str, backward: bool = False) -> int:
    return sum(
        sum(
            _[-1]
            for _ in iteratewhile(
                lambda _: not (_[0] == _[-1] == 0),
                lambda x: [b - a for a, b in zip(x, x[1:])],
                _[::-1] if backward else _,
            )
        )
        for _ in ([int(_) for _ in line.split()] for line in get_lines(data))
    )


def part_one(data="input.txt"):
    return solve(data)


def part_two(data="input.txt"):
    return solve(data, backward=True)


def test():
    assert part_one("test.txt") == 114
    assert part_two("test.txt") == 2
