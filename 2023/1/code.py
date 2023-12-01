# https://adventofcode.com/2023/day/1

import re

from aoctk.input import get_lines


def solve(data, p, rp, lookup={}):
    return sum(
        int(
            "".join(
                lookup.get(_, _)
                for _ in (
                    q.search(s).group(0) for q, s in ((p, line), (rp, line[::-1]))
                )
            )
        )
        for line in get_lines(data)
    )


def part_one(data="input.txt"):
    PATTERN = re.compile(r"\d")

    return solve(data, PATTERN, PATTERN)


def part_two(data="input.txt"):
    NS = r"one|two|three|four|five|six|seven|eight|nine"
    LU = {n: str(v) for v, n in enumerate(NS.split("|"), 1)}
    LU.update({k[::-1]: v for k, v in LU.items()})

    return solve(data, re.compile(r"\d|" + NS), re.compile(r"\d|" + NS[::-1]), LU)


def test():
    assert part_one("test1.txt") == 142
    assert part_two("test2.txt") == 281
