# https://adventofcode.com/2022/day/11

from aoctk.func import prod
from aoctk.input import get_groups


class Monkey:
    barrel = []
    magic = 1

    def __init__(self, d: tuple) -> None:
        self.items = list(map(int, d[1].partition(":")[-1].split(",")))
        self.op = eval(f"lambda old: {d[2].partition('= ')[-1]}")
        self.div = int(d[3].partition("by ")[-1])
        self.throw = tuple(int(_.partition("monkey")[-1]) for _ in d[4:])

        self.count = 0

        self.__class__.magic = self.magic * self.div
        self.barrel.append(self)

    def __call__(self, divisor: int) -> None:
        self.count += len(self.items)
        while self.items:
            w = self.op(self.items.pop()) // divisor
            self.barrel[self.throw[bool(w % self.div)]].items.append(w % self.magic)

    @classmethod
    def business(cls, rounds: int, divisor: int, data: str) -> int:
        for g in get_groups(data):
            cls(g)
        for _ in range(rounds):
            for m in cls.barrel:
                m(divisor)
        try:
            return prod(sorted(m.count for m in cls.barrel)[-2:])
        finally:
            cls.barrel.clear()
            cls.magic = 1


def part_one(data="input.txt"):
    return Monkey.business(20, 3, data)


def part_two(data="input.txt"):
    return Monkey.business(10000, 1, data)


def test():
    assert part_one("test.txt") == 10605
    assert part_two("test.txt") == 2713310158
