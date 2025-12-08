# https://adventofcode.com/2025/day/8

from math import prod

from aoctk.data import Vector as V
from aoctk.input import get_tuples


def part_one(data="input.txt", n=1000):
    vs = [V(*_) for _ in get_tuples(data, sep=",", transformer=int)]
    dm = {
        (u := vs[i], v := vs[j]): abs(u - v)
        for i in range(len(vs))
        for j in range(i + 1, len(vs))
    }

    cs = {}
    for (u, v), _ in zip(sorted(dm, key=lambda x: dm[x]), range(n)):
        for p in (s := cs.get(u, set()) | cs.get(v, set()) | {u, v}):
            cs[p] = s

    return prod(
        sorted([len(_) for _ in set(frozenset(_) for _ in cs.values())], reverse=True)[
            :3
        ]
    )


def part_two(data="input.txt"):
    vs = [V(*_) for _ in get_tuples(data, sep=",", transformer=int)]
    dm = {
        (u := vs[i], v := vs[j]): abs(u - v)
        for i in range(len(vs))
        for j in range(i + 1, len(vs))
    }

    cs = {}
    for u, v in sorted(dm, key=lambda x: dm[x]):
        if len(s := cs.get(u, set()) | cs.get(v, set()) | {u, v}) >= len(vs):
            break
        for p in s:
            cs[p] = s

    return u[0] * v[0]


def test():
    assert (_ := part_one("test.txt", 10)) == 40, _
    assert (_ := part_two("test.txt")) == 25272, _
