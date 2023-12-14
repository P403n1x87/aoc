# https://adventofcode.com/2023/day/14

from itertools import count, takewhile

from aoctk.data import bij
from aoctk.input import get_unbound_2d_grid as u2dg


def roll(p: dict, r: complex, d: complex, s: int, b: int) -> complex:
    t = d * s
    return r + (
        sum(
            p.get(c) != "O"
            for c in takewhile(
                lambda c: 0 <= (d.conjugate() * c).real < b and p.get(c) != "#",
                count(r, t),
            )
        )
        * t
    )


def part_one(data="input.txt"):
    p = u2dg(data)
    _, h = p.size()
    return int(
        sum(
            h - _.imag
            for _ in {roll(p, c, 1j, -1, h): v for c, v in p.items() if v == "O"}
        )
    )


def part_two(data="input.txt"):
    p = u2dg(data)
    (w, h), sp, C = p.size(), {}, 1000000000
    for c in count(1):
        for d, s, b in ((1j, -1, h), (1, -1, w), (1j, 1, h), (1, 1, w)):
            p = {roll(p, c, d, s, b): v for c, v in p.items()}
        if (s := sp.setdefault(frozenset(p for p, v in p.items() if v == "O"), c)) != c:
            return int(sum(h - _.imag for _ in bij(sp).inv[((C - s) % (c - s)) + s]))


def test():
    assert part_one("test.txt") == 136
    assert part_two("test.txt") == 64
