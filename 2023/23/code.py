# https://adventofcode.com/2023/day/23

from collections import defaultdict
from dataclasses import dataclass

from aoctk.data import D4, M4, Graph
from aoctk.input import get_bounded_2d_grid as b2dg


@dataclass(unsafe_hash=True)
class Node:
    p: complex
    d: complex

    def __eq__(self, other: "Node") -> bool:
        return self.p == other.p


class Map(Graph):
    def adj(self, n: Node) -> list[Node]:
        s = self.data[n.p]
        return (
            [Node(n.p + s, s)]
            if s
            else [
                Node(n.p + d, d)
                for d in D4
                if d != -n.d and self.data.get(n.p + d, -d) + d
            ]
        )


def part_one(data="input.txt"):
    m = b2dg(data, filter=lambda x: x != "#", transformer=lambda _: M4.get(_, 0))
    w, h = m.size
    return Map(m).longest(Node(1, 1j), Node(complex(w, h - 1), 1j))


class Path:
    def __init__(self, p: complex, h: tuple[complex, ...]) -> None:
        self.p = p
        self.h = h

    def __eq__(self, other: "Node") -> bool:
        return self.p == other.p

    def __hash__(self) -> int:
        return hash(self.p)


class PMap(Graph):
    def __init__(self, data):
        super().__init__(data)
        self.w = defaultdict(dict)
        self.a = {}
        self.n = {}

    def weight(self, n: Path, m: Path) -> int:
        return self.w[m.p][n.p]

    def adj(self, n: Path) -> list[Path]:
        try:
            a = self.a[p := n.p]
        except KeyError:
            self.n.setdefault(p, 1 << len(self.n))
            for d in (d for d in D4 if self.data.get(p + d) is not None):
                w, seen = 1, {p, q := p + d}
                while (
                    len(
                        e := [
                            q + _
                            for _ in D4
                            if self.data.get(q + _) is not None and q + _ not in seen
                        ]
                    )
                    == 1
                ):
                    seen.add(q := e[0])
                    w += 1
                self.a.setdefault(p, []).append(q)
                self.n.setdefault(q, 1 << len(self.n))
                self.w[p][q] = w
            a = self.a[p]
        # PERF: Pass a bitmask instead of a set
        return [Path(_, n.h | self.n[_]) for _ in a if n.h & self.n[_] == 0]


def part_two(data="input.txt"):
    m = b2dg(data, filter=lambda x: x != "#", transformer=lambda _: 0)
    w, h = m.size
    return PMap(m).longest(Path(1, 1), Path(complex(w, h - 1), set()))


def test():
    assert (_ := part_one("test.txt")) == 94, _
    assert (_ := part_two("test.txt")) == 154, _
