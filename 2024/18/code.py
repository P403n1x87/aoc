# https://adventofcode.com/2024/day/18

from aoctk.data import D4, Graph
from aoctk.data import Bounded2DGrid as BG
from aoctk.input import get_tuples
from aoctk.search import bisect as b


class Memory(Graph):
    def adj(self, p):
        return [
            p + d for d in D4 if self.data.within(p + d) and self.data.get(p + d) != "#"
        ]


def s(bs: list[complex], d: int, n: int) -> int:
    return Memory(BG({p: "#" for _, p in zip(range(n), bs)})).dijkstra(0, (1 + 1j) * d)


def part_one(data="input.txt", d=70, n=1024):
    return s((complex(*_) for _ in get_tuples(data, ",", int)), d, n)


def part_two(data="input.txt", d=70, n=1024):
    bs = [complex(*_) for _ in get_tuples(data, ",", int)]
    return bs[n - 1 + b(list(range(n, len(bs))), lambda m: s(bs, d, m) < float("inf"))]


def test():
    assert (_ := part_one("test.txt", 6, 12)) == 22, _
    assert (_ := part_two("test.txt", 6, 12)) == 6 + 1j, _
