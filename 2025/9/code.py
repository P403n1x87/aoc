# https://adventofcode.com/2025/day/9

from itertools import combinations

from aoctk.data import Path2D
from aoctk.data import Range as R
from aoctk.input import get_tuples


def area(u: complex, v: complex) -> int:
    d = v - u
    return int((abs(d.real) + 1) * (abs(d.imag) + 1))


def part_one(data="input.txt"):
    return max(
        area(u, v)
        for u, v in combinations(
            [complex(*_) for _ in get_tuples(data, sep=",", transformer=int)], 2
        )
    )


def part_two(data="input.txt"):
    c = Path2D.from_vertices(
        ts := [complex(*_) for _ in get_tuples(data, sep=",", transformer=int)]
    ).contour()

    for a, u, v in sorted(
        ((area(u, v), u, v) for u, v in combinations(ts, 2)),
        key=lambda _: _[0],
        reverse=True,
    ):
        rx = R(min(u.real, v.real), max(u.real, v.real))
        ry = R(min(u.imag, v.imag), max(u.imag, v.imag))

        if not any(p.real in rx and p.imag in ry for p in c):
            return a


def test():
    assert (_ := part_one("test.txt")) == 50, _
    assert (_ := part_two("test.txt")) == 24, _
