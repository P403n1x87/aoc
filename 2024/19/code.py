# https://adventofcode.com/2024/day/19

import re
from functools import cache

from aoctk.input import get_groups
from aoctk.search import Trie


def part_one(data="input.txt"):
    (ts,), ps = get_groups(data)
    tp = re.compile(f"({ts.replace(', ', '|')})+")
    return sum(bool(tp.fullmatch(p)) for p in ps)


def part_two(data="input.txt"):
    (ts,), ps = get_groups(data)
    t = Trie(ws := ts.split(", "))
    m = max(map(len, ws))

    @cache
    def c(p: str, i: int = 0) -> int:
        return (
            sum(
                c(p, j + 1)
                for j in range(i, min(i + m, len(p)))
                if t.search(p[i : j + 1])
            )
            if i < len(p)
            else 1
        )

    return sum(c(p) for p in ps)


def test():
    assert (_ := part_one("test.txt")) == 6, _
    assert (_ := part_two("test.txt")) == 16, _
