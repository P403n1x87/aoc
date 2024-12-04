# https://adventofcode.com/2024/day/4

from aoctk.data import D4, D8
from aoctk.input import get_bounded_2d_grid as get_data


def solve(g: callable, s: str, data: str) -> int:
    letters = get_data(data)
    return sum(
        all(letters.get(q) == c for q, c in m.items())
        for p, x in letters.items()
        if x == s
        for m in g(p)
    )


def part_one(data="input.txt"):
    return solve(
        lambda p: ({p + n * d: c for n, c in zip(range(1, 4), "MAS")} for d in D8),
        "X",
        data,
    )


def part_two(data="input.txt"):
    P = {-1 + 1j: "M", -1 - 1j: "M", 1 + 1j: "S", 1 - 1j: "S"}
    return solve(
        lambda p: ({z * r + p: c for z, c in P.items()} for r in D4),
        "A",
        data,
    )


def test():
    assert (_ := part_one("test.txt")) == 18, _
    assert (_ := part_two("test.txt")) == 9, _
