# https://adventofcode.com/2025/day/6

import re

from aoctk.data import pivot
from aoctk.input import get_lines

# split at white spaces
SPLITTER = re.compile(r"\s+")


def part_one(data="input.txt"):
    *qs, rops = get_lines(data)
    ops = SPLITTER.split(rops.strip())
    ps = pivot([SPLITTER.split(p.strip()) for p in qs])
    return sum(eval(op.join(ns)) for op, ns in zip(ops, ps))


def part_two(data="input.txt"):
    *qs, ops = get_lines(data)
    i = a = 0
    while i < len(ops):
        j = i + 1
        while j < len(ops) and ops[j] == " ":
            j += 1

        a += eval(
            ops[i].join(
                (
                    n
                    for n in ("".join(q[k] for q in qs) for k in range(i, j))
                    if n.strip()
                )
            )
        )

        i = j

    return a


def test():
    assert (_ := part_one("test.txt")) == 4277556, _
    assert (_ := part_two("test.txt")) == 3263827, _
