# https://adventofcode.com/2022/day/25

from functools import reduce

from aoctk.data import bij
from aoctk.input import get_lines as gl

SNAFU = bij({"-": -1, "=": -2})


def part_one(data="input.txt"):
    s = sum(
        reduce(lambda a, d: a * 5 + d, n)
        for n in ((int(SNAFU.get(c, c)) for c in _) for _ in gl(data))
    )
    sn = ""
    while s:
        sn += SNAFU.inv.get(r := (_ := s % 5) - 5 * (c := _ > 2), str(r))
        s = s // 5 + c
    return sn[::-1]


def part_two(data="input.txt"):
    return "⭐🎄"


def test():
    assert part_one("test.txt") == "2=-1=0"
    assert part_two("test.txt") == "⭐🎄"
