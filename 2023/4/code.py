# https://adventofcode.com/2023/day/4

from collections import defaultdict

from aoctk.input import get_lines


def card(spec):
    w, _, o = spec.partition(": ")[-1].partition(" | ")
    return len({int(_) for _ in w.split()} & {int(_) for _ in o.split()})


def part_one(data="input.txt"):
    return sum(1 << (s - 1) for s in (card(_) for _ in get_lines(data)) if s)


def part_two(data="input.txt"):
    W = defaultdict(int)
    for n, c in enumerate(card(_) for _ in get_lines(data)):
        W[n] += 1
        for m in range(1, c + 1):
            W[n + m] += W[n]
    return sum(W.values())


def test():
    assert part_one("test.txt") == 13
    assert part_two("test.txt") == 30
