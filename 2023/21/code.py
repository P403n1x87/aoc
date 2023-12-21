# https://adventofcode.com/2023/day/21

from functools import reduce
from itertools import accumulate
from math import prod

from aoctk.data import D4
from aoctk.input import get_bounded_2d_grid as b2dg


def walk(g: dict, s: int, p: set[complex]) -> set[complex]:
    return reduce(
        lambda ps, _: {q + d for q in ps for d in D4 if g.wrap(q + d) in g},
        range(s),
        p,
    )


def part_one(data="input.txt", s: int = 64) -> int:
    g = b2dg(data, filter=lambda x: x != "#")
    return len(walk(g, s, {g.find("S")}))


def part_two(data="input.txt"):
    # After w >> 1 steps we are at the boundary. It then takes w steps to
    # reach the other end. If we are to find a solution, we expect the pattern
    # to just repeat. Since the problem is 2D, we expect the solution to be
    # quadratic. So we compute the smallest 3 points and use them to solve for
    # the quadratic equation.
    g = b2dg(data, filter=lambda x: x != "#")
    w, _ = g.size
    (_, p1, p2, p3) = (
        len(_)
        for _ in accumulate(
            [(w >> 1), w, w],
            lambda a, s: walk(g, s, a),
            initial={g.find("S")},
        )
    )
    n = (26501365 - (w >> 1)) // w  # 202300
    return int(
        sum(
            prod(_)
            for _ in zip(
                [p1, 2 * p2 - (p3 + 3 * p1) / 2, (p1 - 2 * p2 + p3) / 2], [1, n, n**2]
            )
        )
    )


def test():
    assert part_one("test.txt", 6) == 16
    assert part_one("test.txt", 100) == 6536
