# https://adventofcode.com/2022/day/16

from functools import cache, cached_property

from aoctk.data import Graph
from aoctk.input import get_lines


class Pipes(Graph):
    def __init__(self, data):
        self.data = {
            n: (int(r), cs.split(", "))
            for n, r, cs in (
                line[6:]
                .replace(" has flow rate=", ";")
                .replace(" tunnels lead to valves ", "")
                .replace(" tunnel leads to valve ", "")
                .split(";")
                for line in data
            )
        }
        self._paths = {}

    def adj(self, n):
        return self.data[n][1]

    def weight(self, n):
        return self.data[n][0]

    @cached_property
    def valves(self):
        return set(self.data)

    @cache
    def pressure(self, n: str = "AA", t: int = 30, vs: set = frozenset()):
        if t <= 0 or vs == self.valves:
            return 0

        s = max(self.pressure(m, t - 1, vs) for m in self.adj(n))

        return (
            s
            if n in vs or not self.weight(n)
            else max(
                s,
                self.weight(n) * (t - 1) + self.pressure(n, t - 1, frozenset((n, *vs))),
            )
        )

    @cache
    def paths(self, n: str = "AA", t: int = 26, p: int = 0, vs: set = frozenset()):
        if t <= 0 or vs == self.valves:
            if p > 0:
                self._paths[vs] = max(p, self._paths.get(vs, 0))
            return self._paths

        for m in self.adj(n):
            self.paths(m, t - 1, p, vs)

        if n not in vs and self.weight(n):
            self.paths(n, t - 1, p + self.weight(n) * (t - 1), frozenset((n, *vs)))

        return self._paths


def part_one(data="input.txt"):
    return Pipes(get_lines(data)).pressure()


def part_two(data="input.txt"):
    ps = Pipes(get_lines(data)).paths()
    return max(p + q for vs, p in ps.items() for ws, q in ps.items() if not vs & ws)


def test():
    assert part_one("test.txt") == 1651
    assert part_two("test.txt") == 1707
