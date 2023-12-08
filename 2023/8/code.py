# https://adventofcode.com/2023/day/8

import typing as t
from itertools import cycle
from math import lcm

from aoctk.input import get_groups

NodeMap = t.Dict[str, t.Dict[str, str]]


def parse(data: str) -> t.Tuple[str, NodeMap]:
    (ds,), ns = get_groups(data)
    return ds, {
        n: dict(zip("LR", d[1:-1].split(", "))) for n, d in (n.split(" = ") for n in ns)
    }


def steps(n: str, ds: str, nm: NodeMap) -> int:
    for i, d in enumerate(cycle(ds), 1):
        if (n := nm[n][d]).endswith("Z"):
            return i


def part_one(data="input.txt"):
    return steps("AAA", *parse(data))


def part_two(data="input.txt"):
    ds, nm = parse(data)
    return lcm(*(steps(n, ds, nm) for n in (_ for _ in nm if _.endswith("A"))))


def test():
    assert part_one("test.txt") == 2
    assert part_two("test2.txt") == 6
