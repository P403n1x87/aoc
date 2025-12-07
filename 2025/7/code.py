# https://adventofcode.com/2025/day/7

from functools import cache

from aoctk.input import get_bounded_2d_grid as b2dg


def part_one(data="input.txt"):
    bs = {(ss := b2dg(data, str)).find("S")}
    _, h = ss.size
    c = 0
    for _ in range(h):
        nbs = set()
        for b in bs:
            if (n := b + 1j) in ss:
                nbs |= {n + 1, n - 1}
                c += 1
            else:
                nbs.add(n)
        bs = nbs
    return c


def part_two(data="input.txt"):
    s = (ss := b2dg(data, str)).find("S")
    w, h = ss.size
    z = h * 1j

    @cache
    def n(b: complex) -> int:
        if b.imag == s.imag or b in ss:
            return b == s

        m = n(u := b - 1j)
        if b + 1 in ss:
            m += n(u + 1)
        if b - 1 in ss:
            m += n(u - 1)

        return m

    return sum(n(x + z) for x in range(w + 2))


def test():
    assert (_ := part_one("test.txt")) == 21, _
    assert (_ := part_two("test.txt")) == 40, _
