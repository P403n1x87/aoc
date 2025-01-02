# https://adventofcode.com/2024/day/23

from collections import defaultdict

from aoctk.input import get_lines


def part_one(data="input.txt"):
    nw = defaultdict(set)
    for a, b in (_.split("-") for _ in get_lines(data)):
        nw[a].add(b)
        nw[b].add(a)

    gs: set[tuple[str]] = set()
    for a in nw:
        for b in nw[a]:
            for c in nw[b] & nw[a]:
                gs.add(tuple(sorted((a, b, c))))
    return sum(any(_.startswith("t") for _ in g) for g in gs)


def part_two(data="input.txt"):
    nw = defaultdict(set)
    for a, b in (_.split("-") for _ in get_lines(data)):
        nw[a].add(b)
        nw[b].add(a)

    gs = set()
    for c in (_ for _ in nw if _.startswith("t")):
        g, q = {c}, {c}
        while q:
            for e in nw[q.pop()] - g:
                if g <= nw[e]:
                    g.add(e)
                    q.add(e)
        gs.add(tuple(sorted(g)))

    return ",".join(max(gs, key=len))  # maximal clique


def test():
    assert (_ := part_one("test.txt")) == 7, _
    assert (_ := part_two("test.txt")) == "co,de,ka,ta", _
