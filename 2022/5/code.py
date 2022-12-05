# https://adventofcode.com/2022/day/5

from aoctk.input import get_groups


def solve(d, data):
    raw_stacks, instrs = get_groups(data)

    m = [s[1::4] for s in raw_stacks[:-1]]
    stacks = [
        [m[j][i] for j in range(len(m)) if m[j][i] != " "][::-1]
        for i in range(len(m[0]))
    ]

    for n, a, b in (
        map(int, i[5:].replace("from ", "").replace("to ", "").split()) for i in instrs
    ):
        stacks[b - 1].extend(stacks[a - 1][-n:][::d])
        stacks[a - 1][-n:] = []

    return "".join((s[-1] for s in stacks))


def part_one(data="input.txt"):
    return solve(-1, data)


def part_two(data="input.txt"):
    return solve(1, data)


def test():
    assert part_one("test.txt") == "CMZ"
    assert part_two("test.txt") == "MCD"
