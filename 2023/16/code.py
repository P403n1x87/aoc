# https://adventofcode.com/2023/day/16

from collections import defaultdict, deque

from aoctk.input import get_unbound_2d_grid as u2dg

E = {
    "/": {1: [-1j], -1: [1j], 1j: [-1], -1j: [1]},
    "\\": {1: [1j], -1: [-1j], 1j: [1], -1j: [-1]},
    "|": {1: [1j, -1j], -1: [1j, -1j], 1j: [1j], -1j: [-1j]},
    "-": {1: [1], -1: [-1], 1j: [1, -1], -1j: [1, -1]},
}


def energise(g: dict, bds: tuple, s: tuple[complex, complex]) -> int:
    bs, e = deque([s]), defaultdict(set)
    while bs:
        b, d = bs.popleft()
        if d not in e[b]:
            e[b].add(d)
            bs.extend(
                [
                    (b + t, t)
                    for t in E.get(g.get(b), {}).get(d, [d])
                    if g.within(b + t, bds)
                ]
            )
    return len(e)


def part_one(data="input.txt"):
    g = u2dg(data)
    return energise(g, g.bounds(), (0, 1))


def part_two(data="input.txt"):
    g = u2dg(data)
    bds = g.bounds()
    w, h = bds[0].hi, bds[1].hi
    return max(
        (
            max(energise(g, bds, (x, 1j)) for x in range(w + 1)),
            max(energise(g, bds, (x + h * 1j, -1j)) for x in range(w + 1)),
            max(energise(g, bds, (y * 1j, 1)) for y in range(h + 1)),
            max(energise(g, bds, (y * 1j + w, -1)) for y in range(h + 1)),
        )
    )


def test():
    assert part_one("test.txt") == 46
    assert part_two("test.txt") == 51
