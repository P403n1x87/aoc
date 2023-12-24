# https://adventofcode.com/2023/day/24

from itertools import combinations

from aoctk.data import Vector
from aoctk.input import get_lines as gl


def parse(data, tr):
    return [
        tuple(tr(tuple(int(_) for _ in p.split(", "))) for p in line.split(" @ "))
        for line in gl(data)
    ]


def part_one(data="input.txt", a=200000000000000, b=400000000000000):
    return sum(
        all(a <= (_.conjugate() * (z1 + u * w1)).real <= b for _ in (1, 1j))
        for (z1, w1), (z2, w2) in combinations(
            parse(data, lambda _: complex(*_[:2])), 2
        )
        if (d := (w1.conjugate() * w2).imag)
        and (u := ((n := (z2 - z1).conjugate()) * w2).imag / d) > 0
        and (n * w1).imag / d > 0
    )


def part_two(data="input.txt"):
    (r1, v1), (r2, v2), (r3, v3) = parse(data, lambda _: Vector(*_))[2 : 2 + 3]

    m1 = (r3 - r2).x(v3 - v2)
    m2 = (r1 - r3).x(v1 - v3)
    m3 = (r2 - r1).x(v2 - v1)

    a1 = (r3 - r2) @ (v3.x(v2))
    a2 = (r1 - r3) @ (v1.x(v3))
    a3 = (r2 - r1) @ (v2.x(v1))

    v = (a1 * m2.x(m3) + a2 * m3.x(m1) + a3 * m1.x(m2)) / (m1 @ m2.x(m3))

    z1, z2 = complex(*r1[:2]), complex(*r2[:2])
    w1, w2 = complex(*(v1 - v)[:2]), complex(*(v2 - v)[:2])

    return int(
        (
            r1
            + (((z2 - z1).conjugate() * w2).imag / (w1.conjugate() * w2).imag)
            * (v1 - v)
        )
        @ Vector(1, 1, 1)
    )


def test():
    assert (_ := part_one("test.txt", 7, 27)) == 2, _
    assert (_ := part_two("test.txt")) == 47, _
