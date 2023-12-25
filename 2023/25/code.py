# https://adventofcode.com/2023/day/25

import random
from math import prod

from aoctk.input import get_lines


class Edge:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return (
            self.a == other.a
            and self.b == other.b
            or self.a == other.b
            and self.b == other.a
        )

    def copy(self):
        return Edge(self.a, self.b)

    @property
    def vertices(self):
        return {self.a, self.b}


def karger(edges):
    vs = {v for e in edges for v in e.vertices}
    while len(vs) != 2:
        a, b = (e := random.choice(edges)).vertices
        edges = [_ for _ in edges if _ != e]
        v = a | b
        for e in edges:
            if e.a in {a, b}:
                e.a = v
            elif e.b in {a, b}:
                e.b = v
        vs.remove(a)
        vs.remove(b)
        vs.add(v)
    return len(edges), prod(len(_) for _ in edges[0].vertices)


def part_one(data="input.txt"):
    es = [
        Edge(frozenset([a]), frozenset([n]))
        for a, bs in (line.split(": ") for line in get_lines(data))
        for n in bs.split()
    ]
    while True:
        cut, s = karger([_.copy() for _ in es])
        if cut == 3:
            return s


def part_two(data="input.txt"):
    pass


def test():
    assert (_ := part_one("test.txt")) == 54, _
    assert (_ := part_two("test.txt")) is None, _
