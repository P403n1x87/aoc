# https://adventofcode.com/2023/day/18

from itertools import accumulate, chain

from aoctk.data import Path2D
from aoctk.input import get_lines as gl

M = {"D": 1j, "U": -1j, "L": -1, "R": 1}


def dig(vs):
    path = Path2D(list(accumulate(chain([0], vs))))
    return path.pick() + len(path)


def part_one(data="input.txt"):
    return dig(M[d] * int(n) for d, n, _ in (_.split(" ", 2) for _ in gl(data)))


def part_two(data="input.txt"):
    return dig(
        int(c[2:-2], 16) * 1j ** int(c[-2])
        for _, _, c in (_.split(" ", 2) for _ in gl(data))
    )


def test():
    assert part_one("test.txt") == 62
    assert part_two("test.txt") == 952408144115
