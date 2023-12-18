# https://adventofcode.com/2023/day/17

from aoctk.data import D4, Graph
from aoctk.input import get_unbound_2d_grid as u2dg


class Node:
    def __init__(self, p, d, s):
        self.p = p
        self.d = d
        self.s = s

    def __eq__(self, other):
        return self.p == other.p

    def __hash__(self) -> int:
        return hash((self.p, self.d, self.s))


class City(Graph):
    def __init__(self, data, a, b):
        super().__init__(data)
        self.a = a
        self.b = b
        self.bds = data.bounds()

    def weight(self, n: Node) -> int:
        return self.data[n.p]

    def adj(self, n: Node) -> list[Node]:
        return (
            (
                [Node(n.p + n.d, n.d, n.s + 1)]
                if self.data.within(n.p + n.d, self.bds)
                else []
            )
            if n.s < self.a
            else [
                _
                for _ in (
                    Node(n.p + t, t, 1 + n.s * (n.d == t))
                    for t in (n.d * r for r in D4)
                    if t != -n.d
                )
                if _.s <= self.b and self.data.within(_.p, self.bds)
            ]
        )


def solve(data, a, b):
    m = u2dg(data, transformer=int)
    bds = m.bounds()
    c = City(m, a, b)
    return min(
        c.dijkstra(Node(0, d, 0), Node(complex(bds[0].hi, bds[1].hi), 0, 0))
        for d in (1, 1j)
    )


def part_one(data="input.txt"):
    return solve(data, 0, 3)


def part_two(data="input.txt"):
    return solve(data, 4, 10)


def test():
    assert part_one("test.txt") == 102
    assert part_two("test.txt") == 94
