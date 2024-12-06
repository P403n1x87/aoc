# https://adventofcode.com/2024/day/5

from collections import defaultdict

from aoctk.input import get_groups


def get_rules(rules):
    lr = defaultdict(set)
    rr = defaultdict(set)
    for rule in rules:
        a, b = rule.split("|")
        rr[a].add(b)
        lr[b].add(a)
    return lr, rr


def part_one(data="input.txt"):
    rules, pages = get_groups(data)
    lr, rr = get_rules(rules)

    return sum(
        int(_[len(_) >> 1])
        for _ in (
            ps
            for ps in (_.split(",") for _ in pages)
            if all(
                not s or p not in sr or not sr[p] & s
                for p, ss in {
                    p: (set(ps[:i]), set(ps[i + 1 :])) for i, p in enumerate(ps)
                }.items()
                for s, sr in zip(ss, (rr, lr))
            )
        )
    )


def part_two(data="input.txt"):
    rules, pages = get_groups(data)
    lr, rr = get_rules(rules)

    class Page:
        def __init__(self, s):
            self.s = s

        def __lt__(self, other):
            if self.s in rr:
                return other.s in rr[self.s]
            if other.s in lr:
                return self.s in lr[other.s]

        def __eq__(self, other):
            return self.s == other.s or (self.s not in lr or other.s not in rr)

    return sum(
        int(_[len(_) >> 1])
        for _ in (
            sorted(ps, key=Page)
            for ps in (_.split(",") for _ in pages)
            if not all(
                not s or p not in sr or not sr[p] & s
                for p, ss in {
                    p: (set(ps[:i]), set(ps[i + 1 :])) for i, p in enumerate(ps)
                }.items()
                for s, sr in zip(ss, (rr, lr))
            )
        )
    )


def test():
    assert (_ := part_one("test.txt")) == 143, _
    assert (_ := part_two("test.txt")) == 123, _
