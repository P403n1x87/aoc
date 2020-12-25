# https://adventofcode.com/2020/day/24

from functools import reduce
from typing import Generator


E, SE = 5 + 0j, 3 + 4j
SW, W, NW = SE - E, -E, -SE
NE = -SW

DIRS = [E, SE, SW, W, NW, NE]
TR = [("se", 1), ("sw", 2), ("nw", 4), ("ne", 5), ("e", 0), ("w", 3)]


def read(source: str) -> Generator[complex, None, None]:
    def identify(desc: str) -> complex:
        for d, i in TR:
            desc = desc.replace(d, str(i))
        return reduce(complex.__add__, (DIRS[int(_)] for _ in desc))

    for _ in open(source):
        yield identify(_[:-1])


def solve(source: str) -> tuple[int, int]:
    b = set()
    for t in read(source):
        try:
            b.remove(t)
        except KeyError:
            b.add(t)
    n = len(b)

    def a(t: complex) -> set[complex]:
        return {t + d for d in DIRS}

    def bw(b: set[complex]) -> Generator[complex, None, None]:
        for t in b:
            yield t
            yield from a(t) - b

    for _ in range(100):
        b = {t for t in bw(b) if t in b and 0 < len(a(t) & b) < 3 or len(a(t) & b) == 2}

    return n, len(b)


assert (10, 2208) == solve("2020/24/test.txt")
print(solve("2020/24/input.txt"))