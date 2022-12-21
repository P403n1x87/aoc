# https://adventofcode.com/2022/day/19

from functools import cache
from math import prod
from multiprocessing import Pool

from aoctk.data import Vector as V
from aoctk.input import get_lines as gl


class Blueprint:
    MATERIALS = {r: i for i, r in enumerate(("ore", "clay", "obsidian", "geode"))}
    GEODE = V.e(3, 4)

    def __init__(self, spec):
        costs = (
            spec.partition(": ")[-1]
            .replace("Each ", "")
            .replace(" robot costs ", ":")
            .replace(" and ", ",")
            .rstrip(".")
            .split(". ")
        )

        self.cost = [None] * len(self.MATERIALS)

        for robot, reqs in (_.split(":") for _ in costs):
            ms = {m: int(v) for v, m in (_.split() for _ in reqs.split(","))}
            self.cost[self.MATERIALS[robot]] = V(
                *(ms.get(m, 0) for m in self.MATERIALS)
            )

        self.cost = tuple(self.cost)
        self.max_cost = tuple(max(cost[r] for cost in self.cost) for r in range(3))
        self.max = 0

    @cache
    def geodes(self, t=24, rs=V(0, 0, 0, 0), bs=V(1, 0, 0, 0)):
        if t == 2:
            v = rs[-1] + bs[-1] * 2 + all(r >= c for r, c in zip(rs, self.cost[-1]))
            self.max = max(self.max, v)
            return v

        if rs[-1] + bs[-1] * t + t * (t - 1) / 2 <= self.max:
            return rs[-1]

        if all(r >= c for r, c in zip(rs, self.cost[-1])):
            return self.geodes(t - 1, rs - self.cost[-1] + bs, bs + self.GEODE)

        buildable = [
            all(r >= c for r, c in zip(rs, cs)) and b < m and r + b * t < m * t
            for cs, m, r, b in zip(self.cost, self.max_cost, rs, bs)
        ]
        return (
            max(
                max(
                    self.geodes(
                        t - 1,
                        rs - self.cost[r] + bs,
                        bs + V.e(r, 4),
                    )
                    for r, b in list(enumerate(buildable))[::-1]
                    if b
                ),
                self.geodes(t - 1, rs + bs, bs),
            )
            if any(buildable)
            else self.geodes(t - 1, rs + bs, bs)
        )


def po(arg):
    i, bp = arg
    return (i + 1) * Blueprint(bp).geodes(t=24)


def part_one(data="input.txt"):
    with Pool() as p:
        return sum((p.map(po, enumerate(gl(data)))))


def pt(bp):
    return Blueprint(bp).geodes(t=32)


def part_two(data="input.txt"):
    with Pool() as p:
        return prod(p.map(pt, (bp for _, bp in zip(range(3), gl(data)))))


def test():
    assert part_one("test.txt") == 33
    assert part_two("test.txt") == 56 * 62
