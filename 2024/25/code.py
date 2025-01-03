# https://adventofcode.com/2024/day/25

from aoctk.data import Bounded2DGrid as S
from aoctk.input import get_groups


def part_one(data="input.txt"):
    ks, ls = [], []
    for g in (S.from_group(_) for _ in get_groups(data)):
        is_lock = 0 in g
        d = 1j if is_lock else -1j
        hs = []
        for r in range(5):
            p = r + 6j * (not is_lock)
            while p in g:
                p += d
            hs.append(((p - r).imag - 1) if is_lock else ((r + 6j - p).imag - 1))
        (ls if is_lock else ks).append(tuple(hs))
    return sum(all(sum(_) <= 5 for _ in zip(l, k)) for k in ks for l in ls)


def part_two(data="input.txt"):
    pass


def test():
    assert (_ := part_one("test.txt")) == 3, _
    assert (_ := part_two("test.txt")) is None, _
