# https://adventofcode.com/2020/day/16

from functools import reduce


def read(
    source: str,
) -> tuple[dict[str, list[tuple[int, int]]], tuple[int], list[tuple[int]]]:
    rules = {}
    ticket = None
    nearby = []
    with open(source) as fin:
        while True:
            _ = next(fin)
            if _ == "\n":
                break

            name, _, ranges = _.partition(": ")
            rules[name] = [
                tuple(int(v) for v in r.split("-")) for r in ranges.split(" or ")
            ]

        assert next(fin).startswith("your ticket:")
        ticket = tuple(int(v) for v in next(fin).split(","))

        assert next(fin) == "\n"
        assert next(fin).startswith("nearby tickets:")
        nearby = [tuple(int(v) for v in _.split(",")) for _ in fin]

    return rules, ticket, nearby


def solve(source: str) -> tuple[int, int]:
    def validate(rules: tuple[dict[str, list[tuple[int, int]]]], value: int) -> bool:
        return any(any(a <= value <= b for a, b in rule) for rule in rules.values())

    rules, ticket, nearby = read(source)

    valid_nearby = [n for n in nearby if all(validate(rules, v) for v in n)]
    index_map = {
        name: set(
            i
            for i in range(len(ticket))
            if all(any(a <= t[i] <= b for a, b in rule) for t in valid_nearby)
        )
        for name, rule in rules.items()
    }

    field_map = {}
    while index_map:
        for name, s in index_map.items():
            if len(s) == 1:
                n = next(iter(s))
                field_map[n] = name
                break
        del index_map[name]
        for s in index_map.values():
            if n in s:
                s.remove(n)

    return sum(v for t in nearby for v in t if not validate(rules, v)), reduce(
        int.__mul__,
        (ticket[i] for i, name in field_map.items() if name.startswith("departure")),
        1,
    )


assert 71, 1 == solve("test.txt")
print(solve("input.txt"))