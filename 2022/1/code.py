# https://adventofcode.com/2022/day/1

from pathlib import Path


def resolve(name="input.txt") -> Path:
    return Path(__file__).parent / name


def solve(n, datafile="input.txt"):
    return sum(
        sorted(
            sum(int(_) for _ in g.split("\n"))
            for g in resolve(datafile).read_text().strip().split("\n\n")
        )[-n:]
    )


def test():
    assert solve(1, "test.txt") == 24000
    assert solve(3, "test.txt") == 45000


test()
print(solve(1))
print(solve(3))
