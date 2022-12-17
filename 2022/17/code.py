# https://adventofcode.com/2022/day/17

import typing as t
from itertools import cycle

from aoctk.input import get_lines


class Rock:
    def __init__(self, desc):
        self.rs = desc

        self.l = min(_.real for _ in self.rs)
        self.r = max(_.real for _ in self.rs)
        self.b = min(_.imag for _ in self.rs)
        self.t = max(_.imag for _ in self.rs)

        self.tr = 0

    @property
    def top(self) -> int:
        return self.tr.imag + self.t + 1

    def reset(self, y: int) -> None:
        self.tr = complex(2 - self.l, 3 - self.b + y)

    def shift(self, d: complex, g: t.Set[complex]) -> None:
        if not (
            self.l + self.tr.real + d < 0
            or self.r + self.tr.real + d >= 7
            or self.project(d) & g
        ):
            self.tr += d

    def project(self, s: complex) -> t.Set[complex]:
        return {_ + self.tr + s for _ in self.rs}

    def pull(self) -> None:
        self.tr -= 1j


class Chamber:
    __rocks__ = [
        Rock(set(range(4))),  # -
        Rock({1j ** i for i in range(4)} | {0}),  # +
        Rock(set(range(3)) | {2 + 1j, 2 + 2j}),  # L
        Rock({i * 1j for i in range(4)}),  # |
        Rock({complex(i, j) for i in range(2) for j in range(2)}),  # #
    ]

    def __init__(self, jets: str) -> None:
        self.g = {i - 1j for i in range(7)}
        self.rocks = cycle(self.__rocks__)
        self.jets = cycle([{"<": -1, ">": 1}[_] for _ in jets])
        self.y = 0

    def step(self) -> int:
        r = next(self.rocks)
        r.reset(self.y)
        r.shift(next(self.jets), self.g)
        while not r.project(-1j) & self.g:
            r.pull()
            r.shift(next(self.jets), self.g)
        self.g |= r.project(0)
        y, self.y = self.y, max(self.y, r.top)

        return int(self.y - y)

    def simulate(self, r: int) -> int:
        if r < 3000:
            for _ in range(r):
                self.step()
            return int(self.y)

        ds = []

        def get_cycle(ds):
            s = "".join(str(_) for _ in ds)
            needle = s[len(s) // 3 * 2 :]
            cycle = len(s) - s.index(needle) - len(needle)
            if cycle:
                for i in range(len(s)):
                    if s[i : i + cycle] == s[i + cycle : i + cycle << 1]:
                        return i, cycle

        while True:
            for _ in range(len(self.__rocks__)):
                ds.append(self.step())
            cycle = get_cycle(ds)
            if cycle is not None:
                break

        i, n = cycle
        return (
            sum(ds[:i])
            + (r - i) // n * sum(ds[i : i + n])
            + sum(ds[i : i + (r - i) % n])
        )


def part_one(data="input.txt"):
    return Chamber(next(get_lines(data))).simulate(2022)


def part_two(data="input.txt"):
    return Chamber(next(get_lines(data))).simulate(1000000000000)


def test():
    assert part_one("test.txt") == 3068
    assert part_two("test.txt") == 1514285714288
