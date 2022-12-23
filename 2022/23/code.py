# https://adventofcode.com/2022/day/23

from collections import defaultdict
from itertools import count

from aoctk.data import D8
from aoctk.input import get_unbound_2d_grid

R = (-1j, 1j, -1, 1)


def part_one(data="input.txt", n=10):
    o, g = 0, get_unbound_2d_grid(data, filter=lambda _: _ == "#")
    for r in range(1, n + 1) if n is not None else count(1):
        u = defaultdict(list)
        for e in g:
            if not any(g.get(e + d) for d in D8):
                u[e].append(e)
                continue
            for i in range(len(R)):
                d = R[(o + i) % len(R)]
                if not any(
                    g.get(e + _) for _ in (d * (1 + 1j * k) for k in range(-1, 2))
                ):
                    u[e + d].append(e)
                    break
            else:
                u[e].append(e)

        ng = g.__class__()
        for k, v in u.items():
            if len(v) == 1:
                ng[k] = "#"
            else:
                for w in v:
                    ng[w] = "#"

        if g == ng:
            break

        g, o = ng, (o + 1) % len(R)

    return (
        sum(complex(i, j) not in g for i, j in g.iter_bounds()) if n is not None else r
    )


def part_two(data="input.txt"):
    return part_one(data, None)


def test():
    assert part_one("test.txt") == 110
    assert part_two("test.txt") == 20
