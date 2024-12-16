# https://adventofcode.com/2024/day/16


from aoctk.data import Graph
from aoctk.input import get_bounded_2d_grid


class Node:
    def __init__(self, p, d, t):
        self.p = p
        self.d = d
        self.t = t

    def __eq__(self, other):
        return self.p == other.p

    def __hash__(self) -> int:
        return hash((self.p, self.d, self.t))


class Map(Graph):
    def weight(self, n: Node) -> int:
        return 1 + n.t * 1000

    def adj(self, n: Node) -> list[Node]:
        return [
            Node(n.p + n.d * r, n.d * r, r != 1)
            for r in (1, -1j, 1j)
            if self.data.get(n.p + n.d * r) != "#"
        ]


def part_one(data="input.txt"):
    m = get_bounded_2d_grid(data)
    (s,) = {p for p, v in m.items() if v == "S"}
    (e,) = {p for p, v in m.items() if v == "E"}
    return Map(m).dijkstra(Node(s, 1, 0), Node(e, 0, 0))


def part_two(data="input.txt"):
    m = get_bounded_2d_grid(data)
    (s,) = {p for p, v in m.items() if v == "S"}
    (e,) = {p for p, v in m.items() if v == "E"}
    return len(
        {_.p for ps in Map(m).shortest_paths(Node(s, 1, 0), Node(e, 0, 0)) for _ in ps}
    )


def test():
    assert (_ := part_one("test.txt")) == 7036, _
    assert (_ := part_two("test.txt")) == 45, _
