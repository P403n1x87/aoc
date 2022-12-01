# https://adventofcode.com/2022/day/1

from aoctk.input import get_groups


def solve(n, data="input.txt"):
    return sum(sorted(sum(_) for _ in get_groups(data, int))[-n:])


def test():
    assert solve(1, "test.txt") == 24000
    assert solve(3, "test.txt") == 45000


test()
print(solve(1))
print(solve(3))
