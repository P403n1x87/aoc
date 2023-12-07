# https://adventofcode.com/2023/day/7

from collections import Counter

from aoctk.input import get_lines

TYPES = [
    {1: 5},  # High Card
    {2: 1, 1: 3},  # One Pair
    {2: 2, 1: 1},  # Two Pairs
    {3: 1, 1: 2},  # Three of a Kind
    {3: 1, 2: 1},  # Full House
    {4: 1, 1: 1},  # Four of a Kind
    {5: 1},  # Five of a Kind
]
LABELS = "23456789TJQKA"
LABEL = {f: v for v, f in enumerate(LABELS)}
JLABEL = {f: v for v, f in enumerate("J23456789TQKA")}


def _value(hand: str, hand_desc: Counter, label: dict) -> int:
    s = TYPES.index(hand_desc)
    for c in hand:
        s = s * len(LABELS) + label[c]
    return s


def value(hand: str) -> int:
    return _value(hand, Counter(Counter(hand).values()), LABEL)


def jvalue(hand: str) -> int:
    c = Counter(hand)
    js = c.pop("J", 0)

    if js == 0:
        return _value(hand, Counter(c.values()), JLABEL)
    if js >= 4:
        return _value(hand, Counter({5: 1}), JLABEL)

    return max(
        _value(hand, h, JLABEL)
        for h in (
            Counter({k: v + js * (k == j) for k, v in c.items()}.values()) for j in c
        )
    )


def poker(data: str, key: callable) -> int:
    return sum(
        b * r
        for r, b in enumerate(
            (
                int(_[1])
                for _ in sorted(
                    (_.split() for _ in get_lines(data)), key=lambda _: key(_[0])
                )
            ),
            1,
        )
    )


def part_one(data="input.txt"):
    return poker(data, value)


def part_two(data="input.txt"):
    return poker(data, jvalue)


def test():
    assert part_one("test.txt") == 6440
    assert part_two("test.txt") == 5905
