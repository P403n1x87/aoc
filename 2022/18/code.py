# https://adventofcode.com/2022/day/18

from functools import cached_property

from aoctk.data import Graph, Range
from aoctk.data import Vector as V
from aoctk.input import get_tuples


class Droplet(Graph):
    DIRS = (V(-1, 0, 0), V(1, 0, 0), V(0, -1, 0), V(0, 1, 0), V(0, 0, -1), V(0, 0, 1))

    def __init__(self, data):
        self.data = data

    def adj(self, n):
        return {_ for _ in (n + d for d in self.DIRS) if _ in self.data}

    def surface(self, pockets=False):
        s = 6 * len(self.data) - sum(len(self.adj(n)) for n in self.data)
        return s - sum(p.surface() for p in self.pockets()) if pockets else s

    @cached_property
    def bounds(self):
        return tuple(
            Range(min(_[i] for _ in self.data), max(_[i] for _ in self.data))
            for i in range(3)
        )

    def pockets(self):
        ps = []
        for n in self.data:
            for v in (n + d for d in self.DIRS):
                if not (
                    v in self.data
                    or not v.within(self.bounds)
                    or any(v in _.data for _ in ps)
                ):
                    q, p = {v}, {v}
                    while q and p:
                        m = q.pop()
                        for _ in (m + d for d in self.DIRS):
                            if _ not in self.data and _ not in p:
                                if not _.within(self.bounds):
                                    p.clear()
                                    break
                                p.add(_)
                                q.add(_)
                    if p:
                        ps.append(Droplet(p))
        return ps


def part_one(data="input.txt"):
    return Droplet({V(*map(int, _)) for _ in get_tuples(data, sep=",")}).surface(False)


def part_two(data="input.txt"):
    return Droplet({V(*map(int, _)) for _ in get_tuples(data, sep=",")}).surface(True)


def test():
    assert part_one("test.txt") == 64
    assert part_two("test.txt") == 58
