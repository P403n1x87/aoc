# https://adventofcode.com/2023/day/11

from itertools import chain, pairwise

from aoctk.input import get_unbound_2d_grid as u2dg
from aoctk.metric import manhattan2d as m2d


def steps(seq: list[int], size: int) -> list[int]:
    c, cs, nseq = 0, [0] * size, sorted(set(range(size)) - set(seq))
    for a, b in pairwise(chain(nseq, [size])):
        cs[a:b] = [c := c + 1] * (b - a)
    return cs


def solve(data: str, factor: int) -> int:
    u = u2dg(data, filter=lambda _: _ != ".")
    w, h = u.size()
    cx, cy = (
        steps((int((e.conjugate() * g).real) for g in u), d)
        for e, d in ((1, w), (1j, h))
    )
    gs = list(u.keys())

    return sum(
        m2d(gs[i], gs[j])
        + (
            abs(cx[int(gs[i].real)] - cx[int(gs[j].real)])
            + abs(cy[int(gs[i].imag)] - cy[int(gs[j].imag)])
        )
        * (factor - 1)
        for i in range(len(gs))
        for j in range(i + 1, len(gs))
    )


def part_one(data="input.txt"):
    return solve(data, 2)


def part_two(data="input.txt"):
    return solve(data, 1000000)


def test():
    assert part_one("test.txt") == 374
    assert solve("test.txt", 10) == 1030
    assert solve("test.txt", 100) == 8410
