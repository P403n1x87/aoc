# https://adventofcode.com/2025/day/11

from aoctk.data import Graph
from aoctk.input import get_tuples


class Network(Graph):
    def adj(self, n):
        return self.data.get(n, [])


def part_one(data="input.txt"):
    return len(
        Network({k: set(v.split()) for k, v in get_tuples(data, sep=": ")}).paths(
            "you", "out"
        )
    )


def part_two(data="input.txt"):
    n = Network({k: set(v.split()) for k, v in get_tuples(data, sep=": ")})
    m = n.inverse()
    sn = n.subgraph(n.reachable_from("fft") & m.reachable_from("dac"))
    return (
        len(m.paths("fft", "svr"))
        * len(sn.paths("fft", "dac"))
        * len(n.paths("dac", "out"))
    )


def test():
    assert (_ := part_one("test.txt")) == 5, _
    assert (_ := part_two("test2.txt")) == 2, _
