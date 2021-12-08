# https://adventofcode.com/2021/day/8

import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


def solve(datafile="input.txt"):
    data = [
        tuple(_.split() for _ in line.strip().split(" | ", maxsplit=1))
        for line in open(resolve(datafile))
    ]

    DIGITS = {
        k: str(i)
        for i, k in enumerate(
            [
                (6, 2, 3),
                (2, 2, 2),
                (5, 1, 2),
                (5, 2, 3),
                (4, 2, 4),
                (5, 1, 3),
                (6, 1, 3),
                (3, 2, 2),
                (7, 2, 4),
                (6, 2, 4),
            ]
        )
    }

    def key(digit, one, four):
        return (len(digit), len(digit & one), len(digit & four))

    def decode(patterns, digits):
        ps = [frozenset(_) for _ in patterns]

        (one,) = [_ for _ in ps if len(_) == 2]
        (four,) = [_ for _ in ps if len(_) == 4]

        return int("".join(DIGITS[key(frozenset(_), one, four)] for _ in digits))

    return (
        sum(len(d) in {2, 3, 4, 7} for _, e in data for d in e),
        sum(decode(*e) for e in data),
    )


def test():
    assert solve("test.txt") == (26, 61229)


test()
print(solve())
