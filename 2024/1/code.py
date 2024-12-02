# https://adventofcode.com/2024/day/1

from collections import Counter

from aoctk.input import get_tuples


def part_one(data="input.txt"):
    return sum(
        abs(a - b)
        for a, b in zip(
            *(
                sorted(_)
                for _ in list(zip(*get_tuples(data, sep="   ", transformer=int)))
            )
        )
    )


def part_two(data="input.txt"):
    a, b = list(zip(*get_tuples(data, sep="   ", transformer=int)))
    c = Counter(b)
    return sum(_ * c.get(_, 0) for _ in a)


def test():
    assert (_ := part_one("test.txt")) == 11, _
    assert (_ := part_two("test.txt")) == 31, _
