# https://adventofcode.com/2023/day/3

from collections import defaultdict
from math import prod

from aoctk.data import D8
from aoctk.input import get_unbound_2d_grid


def part_one(data="input.txt"):
    engine = get_unbound_2d_grid(
        data,
        transformer=lambda c: int(c) if c.isnumeric() else "*",
        filter=lambda c: c != ".",
    )

    w, h = engine.size()
    s = 0
    for j in range(h):
        n, p = 0, False
        for i in range(w):
            c = i + j * 1j
            e = engine.get(c)
            if isinstance(e, int):
                n, p = n * 10 + e, p or any(engine.get(c + _) == "*" for _ in D8)
            else:
                s += n if p else 0
                n, p = 0, False
        if p:
            s += n

    return s


def part_two(data="input.txt"):
    engine = get_unbound_2d_grid(
        data,
        transformer=lambda c: int(c) if c.isnumeric() else c,
        filter=lambda c: c.isnumeric() or c == "*",
    )

    w, h = engine.size()
    gears = defaultdict(set)
    for j in range(h):
        n, gs = 0, []
        for i in range(w):
            c = i + j * 1j
            e = engine.get(c)
            if isinstance(e, int):
                n = n * 10 + e
                gs.extend(c + _ for _ in D8 if engine.get(c + _) == "*")
            else:
                while gs:
                    gears[gs.pop()].add(n)
                n = 0
        while gs:
            gears[gs.pop()].add(n)

    return sum(prod(ps) for ps in gears.values() if len(ps) >= 2)


def test():
    assert part_one("test.txt") == 4361
    assert part_two("test.txt") == 467835
