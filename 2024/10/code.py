# https://adventofcode.com/2024/day/10

from aoctk.data import D4
from aoctk.input import get_bounded_2d_grid as get_data


def solve(data, sf):
    m = get_data(data, transformer=int)
    return sum(sf(m, th, set()) for th in (p for p, v in m.items() if v == 0))


def part_one(data="input.txt"):
    def step(m: dict, p: complex, ns: set) -> int:
        if (v := m[p]) == 9:
            ns.add(p)
        else:
            for q in (q for q in (p + _ for _ in D4) if m.get(q) == v + 1):
                step(m, q, ns)
        return len(ns)

    return solve(data, step)


def part_two(data="input.txt"):
    def step(m: dict, p: complex, ns: set) -> int:
        return (
            1
            if (v := m[p]) == 9
            else sum(
                step(m, q, ns)
                for q in (q for q in (p + _ for _ in D4) if m.get(q) == v + 1)
            )
        )

    return solve(data, step)


def test():
    assert (_ := part_one("test.txt")) == 36, _
    assert (_ := part_two("test.txt")) == 81, _
