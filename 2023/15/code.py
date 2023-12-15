# https://adventofcode.com/2023/day/15

from collections import defaultdict
from functools import reduce

from aoctk.input import get_lines


def HASH(label: str) -> int:
    return reduce(lambda a, c: ((a + ord(c)) * 17) % 256, label, 0)


def part_one(data="input.txt"):
    return sum(HASH(i) for i in next(get_lines(data)).split(","))


def part_two(data="input.txt"):
    instrs, bs, fs = next(get_lines(data)).split(","), defaultdict(list), {}
    for i in instrs:
        label, f = i[0 : -(1 + ("=" in i))], i[-1]
        box = HASH(label) + 1
        if f == "-":
            try:
                bs[box].remove(label)
                del fs[label]
            except ValueError:
                pass
        else:
            if label not in bs[box]:
                bs[box].append(label)
            fs[label] = int(f)

    return sum(sum(fs[l] * i * b for i, l in enumerate(ls, 1)) for b, ls in bs.items())


def test():
    assert part_one("test.txt") == 1320
    assert part_two("test.txt") == 145
