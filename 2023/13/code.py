# https://adventofcode.com/2023/day/13


from itertools import dropwhile, product

from aoctk.data import Unbound2DGrid as U2DG
from aoctk.input import get_groups as gs


def mirror(p: U2DG, a: int, b: int, d: complex, t: int = 0) -> int:
    c, fm = (a + b) / 2 * d, {_ for _ in p if a <= (d.conjugate() * _).real <= b}
    return (
        int((a + b + 1) / 2 * (1 if d == 1 else 100))
        if len({_ - 2 * (d.conjugate() * (_ - c)).real * d for _ in fm} - fm) == t
        else 0
    )


def solve(data: str, t: int) -> int:
    return sum(
        next(
            dropwhile(
                lambda _: _ == 0,
                (
                    mirror(p, c if s > 0 else 0, b - 1 if s > 0 else c, d, t)
                    for (b, d), s in product(zip(p.size(), (1, 1j)), (2, -2))
                    for c in range(
                        b % 2 if s > 0 else b - 1 - (b % 2), b - 1 if s > 0 else 0, s
                    )
                ),
            )
        )
        for p in (U2DG.from_group(g, filter=lambda _: _ != ".") for g in gs(data))
    )


def part_one(data="input.txt"):
    return solve(data, 0)


def part_two(data="input.txt"):
    return solve(data, 1)


def test():
    assert part_one("test.txt") == 405
    assert part_two("test.txt") == 400
