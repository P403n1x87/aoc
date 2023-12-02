# https://adventofcode.com/2023/day/2

from math import prod

from aoctk.input import get_lines


def game(line: str) -> tuple[int, list[dict[str, int]]]:
    ident, _, hands = line[5:].partition(": ")
    return int(ident), [
        {c: int(n) for n, _, c in (pair.partition(" ") for pair in hand.split(", "))}
        for hand in hands.split("; ")
    ]


def part_one(data="input.txt"):
    return sum(
        ident
        for ident, hands in (game(line) for line in get_lines(data))
        if all(
            h.get(c, 0) <= n
            for c, n in {"red": 12, "green": 13, "blue": 14}.items()
            for h in hands
        )
    )


def part_two(data="input.txt"):
    return sum(
        prod(max(h.get(c, 0) for h in hands) for c in {"red", "green", "blue"})
        for _, hands in (game(line) for line in get_lines(data))
    )


def test():
    assert part_one("test.txt") == 8
    assert part_two("test.txt") == 2286
