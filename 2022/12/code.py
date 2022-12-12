# https://adventofcode.com/2022/day/12

from aoctk.data import Graph
from aoctk.input import get_unbound_2d_grid


class HeightMap(Graph):
    def __init__(self, data):
        self.nodes = get_unbound_2d_grid(data, lambda _: ord(_) - ord("a"))

        (self.start,) = (n for n, v in self.nodes.items() if v == ord("S") - ord("a"))
        (self.end,) = (n for n, v in self.nodes.items() if v == ord("E") - ord("a"))

        self.nodes[self.start] = 0
        self.nodes[self.end] = ord("z") - ord("a")

    def adj(self, n):
        return (
            n + w
            for w in (1j ** i for i in range(4))
            if n + w in self.nodes and self.nodes[n + w] - self.nodes[n] <= 1
        )

    def steps(self):
        return self.dijkstra(self.start, self.end)

    def trail(self):
        return min(
            self.dijkstra(_, self.end)
            for _ in (n for n, v in self.nodes.items() if v == 0)
        )


def part_one(data="input.txt"):
    return HeightMap(data).steps()


def part_two(data="input.txt"):
    return HeightMap(data).trail()


def test():
    assert part_one("test.txt") == 31
    assert part_two("test.txt") == 29
