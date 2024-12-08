# https://adventofcode.com/2024/day/8

from collections import defaultdict

from aoctk.input import get_bounded_2d_grid as get_data


def part_one(data="input.txt"):
    antennas = get_data(data)
    g = defaultdict(list)
    for loc, f in antennas.items():
        g[f].append(loc)
    ans = set()
    for f, locs in g.items():
        n = len(locs)
        for i in range(n):
            for j in range(i + 1, n):
                a, b = locs[i], locs[j]
                v = b - a
                if antennas.within(b + v):
                    ans.add(b + v)
                if antennas.within(a - v):
                    ans.add(a - v)
    return len(ans)


def part_two(data="input.txt"):
    antennas = get_data(data)
    g = defaultdict(list)
    for loc, f in antennas.items():
        g[f].append(loc)
    ans = set()
    for f, locs in g.items():
        n = len(locs)
        for i in range(n):
            for j in range(i + 1, n):
                a, b = locs[i], locs[j]
                v = b - a
                an = a + v
                while antennas.within(an):
                    ans.add(an)
                    an += v
                an = b - v
                while antennas.within(an):
                    ans.add(an)
                    an -= v
    return len(ans)


def test():
    assert (_ := part_one("test.txt")) == 14, _
    assert (_ := part_two("test.txt")) == 34, _
