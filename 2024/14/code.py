# https://adventofcode.com/2024/day/14

from collections import defaultdict
from math import prod

from aoctk.data import Bounded2DGrid as G
from aoctk.data import wrap
from aoctk.input import get_lines


def robots(data: str) -> iter:
    yield from (
        (complex(*(int(_) for _ in p)) for p in (_.split(b",") for _ in pv))
        for pv in (
            _.encode().translate(None, b"pv=").split(b" ") for _ in get_lines(data)
        )
    )


def part_one(data="input.txt", w=101, h=103):
    qs = defaultdict(int)

    for p in (
        _
        for _ in (wrap(p + 100 * v, w, h) for p, v in robots(data))
        if _.real != (w2 := (w >> 1)) and _.imag != (h2 := (h >> 1))
    ):
        qs[((p.real > w2) << 1) | (p.imag > h2)] += 1

    return prod(qs.values())


def part_two(data="input.txt"):
    # Pattern at 48, occurring every 101 iterations from that
    G({wrap(p + 6512 * v, 101, 103): "*" for p, v in robots(data)}).print()

    return 6512


def test():
    assert (_ := part_one("test.txt", 11, 7)) == 12, _
