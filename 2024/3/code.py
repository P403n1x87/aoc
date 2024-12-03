# https://adventofcode.com/2024/day/3

import re
from math import prod

from aoctk.input import get_lines

MUL_RE = re.compile(r"mul\((\d+),(\d+)\)")
DONT_RE = re.compile(r"don't\(\).*?(do\(\)|$)")


def solve(instr: str) -> int:
    # NOTE: The input is a single instruction line
    return sum(prod(int(_) for _ in m) for m in MUL_RE.findall(instr))


def part_one(data="input.txt"):
    return solve("".join(get_lines(data)))


def part_two(data="input.txt"):
    return solve(DONT_RE.sub("", "".join(get_lines(data))))


def test():
    assert (_ := part_one("test.txt")) == 161, _
    assert (_ := part_two("test2.txt")) == 48, _
