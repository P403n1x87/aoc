# https://adventofcode.com/2023/day/5

import typing as t
from collections import deque

from aoctk.data import Range
from aoctk.input import get_groups

Map = t.List[t.Tuple[Range, int]]


def parse(data) -> t.Tuple[t.List[int], t.List[Map]]:
    (seeds,), *maps = get_groups(data)
    return [int(_) for _ in seeds.partition(": ")[-1].split()], [
        [
            (Range(s, s + w - 1), d)
            for d, s, w in (
                tuple(int(_) for _ in range.split(" ", maxsplit=2)) for range in ranges
            )
        ]
        for _, *ranges in maps
    ]


def min_location(seeds: Range, maps: t.List[Map]) -> int:
    ranges = deque([seeds])

    for m in maps:
        mapped_ranges = deque()
        while ranges and (rn := ranges.pop()):
            for sr, d in m:
                if o := sr & rn:
                    _, *diff = rn.disjoint_union(o)
                    mapped_ranges.append(o.shift(d - sr.lo))
                    ranges.extend(diff)
                    break
            else:
                mapped_ranges.append(rn)
        ranges = mapped_ranges

    return min(_.lo for _ in ranges)


def part_one(data="input.txt"):
    seeds, maps = parse(data)
    return min(min_location(Range(seed, seed), maps) for seed in seeds)


def part_two(data="input.txt"):
    seed_pairs, maps = parse(data)
    return min(
        min_location(seed, maps)
        for seed in (
            Range(s, s + n - 1) for s, n in zip(seed_pairs[::2], seed_pairs[1::2])
        )
    )


def test():
    assert part_one("test.txt") == 35
    assert part_two("test.txt") == 46
