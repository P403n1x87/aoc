# https://adventofcode.com/2022/day/8

from functools import reduce
from itertools import count, takewhile

from aoctk.input import get_unbound_2d_grid


def apply(f, trees):
    w, h = trees.size()
    return (f(complex(i, j), trees) for i in range(1, w - 1) for j in range(1, h - 1))


def part_one(data="input.txt"):
    trees = get_unbound_2d_grid(data)
    w, h = trees.size()

    return (
        sum(
            apply(
                lambda z, trees: any(
                    max(
                        trees[_]
                        for _ in (
                            takewhile(
                                lambda w: w in trees,
                                (z + d * k for k in count(1)),
                            )
                        )
                    )
                    < trees[z]
                    for d in (1j ** k for k in range(4))
                ),
                trees,
            )
        )
        + ((w + h - 2) << 1)
    )


def part_two(data="input.txt"):
    trees = get_unbound_2d_grid(data)

    def take(h, i):
        for _ in i:
            if _ not in trees:
                break
            yield 1
            if trees[_] >= h:
                break

    return max(
        apply(
            lambda z, trees: reduce(
                lambda a, b: a * b,
                (
                    sum(
                        take(
                            trees[z],
                            (z + d * k for k in count(1)),
                        )
                    )
                    for d in (1j ** k for k in range(4))
                ),
            ),
            trees,
        )
    )


def test():
    assert part_one("test.txt") == 21
    assert part_two("test.txt") == 8
