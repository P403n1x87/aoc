import heapq
from dataclasses import dataclass


@dataclass
class Range:
    lo: int
    hi: int

    def __contains__(self, other: "Range") -> bool:
        return self.lo <= other.lo and other.hi <= self.hi

    def overlaps(self, other: "Range") -> bool:
        return self.hi >= other.lo and other.hi >= self.lo


class Unbound2DGrid(dict):
    def size(self):
        return (
            int(
                max(k.real for k in self.keys()) - min(k.real for k in self.keys()) + 1
            ),
            int(
                max(k.imag for k in self.keys()) - min(k.imag for k in self.keys()) + 1
            ),
        )

    def bounds(self):
        return (
            Range(
                int(min(k.real for k in self.keys())),
                int(max(k.real for k in self.keys())),
            ),
            Range(
                int(min(k.imag for k in self.keys())),
                int(max(k.imag for k in self.keys())),
            ),
        )

    def print(self, reverse=False):
        xr, yr = self.bounds()
        for y in range(yr.hi, yr.lo - 1, -1) if reverse else range(yr.lo, yr.hi + 1):
            for x in range(xr.lo, xr.hi + 1):
                print(self.get(x + y * 1j, " "), end="")
            print()


class Graph:
    @dataclass
    class WeightedNode:
        weight: int
        node: object

        def __lt__(self, other):
            return self.weight < other.weight

    def adj(self, n):
        raise NotImplementedError()

    def dijkstra(self, start, end):
        seen, q = set(), [self.WeightedNode(0, start)]
        heapq.heapify(q)

        while q:
            wn = heapq.heappop(q)
            if wn.node == end:
                return wn.weight
            if wn.node in seen:
                continue
            seen.add(wn.node)
            for t in self.adj(wn.node):
                heapq.heappush(q, self.WeightedNode(wn.weight + 1, t))

        return float("inf")
