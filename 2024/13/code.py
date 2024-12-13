# https://adventofcode.com/2024/day/13

from aoctk.input import get_groups


def solve(data: str, s: int) -> int:
    cost = 0
    for (a, b), (c, d), (x, y) in (
        (
            (
                int(_)
                for _ in s.partition(": ")[-1]
                .encode()
                .translate(None, b"XY+=")
                .split(b", ")
            )
            for s in _
        )
        for _ in get_groups(data)
    ):
        if det := a * d - b * c:
            x += s
            y += s
            v = ((x * d - y * c), (a * y - b * x))
            if all(_ % det == 0 for _ in v):
                cost += sum(w * z for w, z in zip((3, 1), v)) // det
    return cost


def part_one(data="input.txt"):
    return solve(data, 0)


def part_two(data="input.txt"):
    return solve(data, 10000000000000)


def test():
    assert (_ := part_one("test.txt")) == 480, _
    assert (_ := part_two("test.txt")) == 875318608908, _
