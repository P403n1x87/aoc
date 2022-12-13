# https://adventofcode.com/2022/day/13

from functools import cmp_to_key
from itertools import chain

from aoctk.func import prod
from aoctk.input import get_groups as gg


def c(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a - b

    a = [a] if isinstance(a, int) else a
    b = [b] if isinstance(b, int) else b

    for _ in (c(x, y) for x, y in zip(a, b)):
        if _ != 0:
            return _

    return len(a) - len(b)


def part_one(d="input.txt"):
    return sum(i for i, v in enumerate((c(a, b) for a, b in gg(d, eval)), 1) if v < 0)


def part_two(data="input.txt"):
    ms = [[[2]], [[6]]]
    ps = sorted(chain(ms, (s for g in gg(data, eval) for s in g)), key=cmp_to_key(c))
    return prod(1 + ps.index(_) for _ in ms)


def test():
    assert part_one("test.txt") == 13
    assert part_two("test.txt") == 140
