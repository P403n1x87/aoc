# https://adventofcode.com/2022/day/14

from aoctk.data import Unbound2DGrid
from aoctk.input import get_tuples


def solve(floor, data="input.txt"):
    cave = Unbound2DGrid()

    for line in (
        zip(_, _[1:])
        for _ in get_tuples(data, " -> ", lambda _: complex(*map(int, _.split(","))))
    ):
        for a, b in line:
            d = b - a
            n = d / abs(d)
            for _ in range(int(abs(d)) + 1):
                cave[a + n * _] = "#"

    s, c, y_max = 500, 0, cave.bounds()[-1].hi

    def deposit():
        nonlocal s, c, cave
        cave[s], s, c = "o", 500, c + 1

    while (not floor and s.imag < y_max) or (floor and 500 not in cave):
        if floor and s.imag > y_max:
            deposit()
        for d in (1j, 1j - 1, 1j + 1):
            if s + d not in cave:
                s += d
                break
        else:
            deposit()

    return c


def part_one(data="input.txt"):
    return solve(False, data)


def part_two(data="input.txt"):
    return solve(True, data)


def test():
    assert part_one("test.txt") == 24
    assert part_two("test.txt") == 93
