# https://adventofcode.com/2022/day/24

import heapq
from collections import defaultdict
from math import lcm

from aoctk.data import M4, Graph
from aoctk.input import get_unbound_2d_grid
from aoctk.metric import manhattan2d as md


class Valley(Graph):
    def __init__(self, grid):
        self.grid = grid

        self.states = {}
        self.w, self.h = (_.hi - 1 for _ in grid.bounds())
        self.period, self.min_t = lcm(self.w, self.h), float("inf")
        self.entry, self.exit = 1, complex(self.w, self.h + 1)
        self.time_offset = 0
        self.reversed = 1

        # Precompute all possible blizzard. We might not need them all but
        # hey, life's easier this way.
        s = defaultdict(list)
        for z, d in self.grid.items():
            if d != "#":
                s[z].append(M4[d])
        self.states[0] = s

        wrap = lambda n, m: ((int(n) - 1) % m) + 1
        for t in range(1, self.period):
            n = defaultdict(list)
            for z, bs in s.items():
                for b in bs:
                    w = z + b
                    w = complex(wrap(w.real, self.w), wrap(w.imag, self.h))
                    n[w].append(b)
            s = self.states[t] = n

        # Add walls around entry and exit
        for _ in range(3):
            self.grid[complex(_, -1)] = "#"
            self.grid[complex(self.w + 1 - _, self.h + 2)] = "#"

    def adj(self, t, z):
        bs = self.states[(t + 1 + self.time_offset) % self.period]
        for d in (1j, 1, -1j, -1):
            w = z + d * self.reversed
            if self.grid.get(w) != "#" and w not in bs:
                yield w
        if z not in bs:
            yield z

    def cross(self):
        seen, q = set(), [self.WeightedNode(0, self.entry)]
        heapq.heapify(q)

        while q:
            wn = heapq.heappop(q)
            if wn.node == self.exit:
                self.min_t = min(self.min_t, wn.weight)
                continue
            if wn in seen or wn.weight + md(wn.node, self.exit) >= self.min_t:
                continue
            seen.add(wn)
            for z in self.adj(wn.weight, wn.node):
                heapq.heappush(q, self.WeightedNode(wn.weight + 1, z))

        try:
            return self.min_t
        finally:
            self.reversed = -self.reversed
            self.time_offset += self.min_t
            self.entry, self.exit, self.min_t = self.exit, self.entry, float("inf")


def part_one(data="input.txt"):
    return Valley(get_unbound_2d_grid(data, filter=lambda _: _ != ".")).cross()


def part_two(data="input.txt"):
    v = Valley(get_unbound_2d_grid(data, filter=lambda _: _ != "."))
    return sum(v.cross() for _ in range(3))


def test():
    assert part_one("test.txt") == 18
    assert part_two("test.txt") == 54
