# https://adventofcode.com/2023/day/10

from itertools import pairwise

from aoctk.data import D4
from aoctk.input import get_unbound_2d_grid

D = {
    "|": {1j: 1j, -1j: -1j},
    "-": {1: 1, -1: -1},
    "7": {1: 1j, -1j: -1},
    "L": {1j: 1, -1: -1j},
    "F": {-1j: 1, -1: 1j},
    "J": {1j: -1, 1: -1j},
}


def loop(data: str) -> tuple[list, int, dict]:
    grid = get_unbound_2d_grid(data, filter=lambda _: _ != ".")
    s = grid.find("S")
    for d in D4:
        p, path = s, []
        while d:
            path.append(p)
            if grid[p := p + d] == "S":
                break
            d = D.get(grid[p], {}).get(d, 0)
        else:
            continue
        break
    path.append(s)
    return path


def part_one(data="input.txt"):
    return len(loop(data)) >> 1


def part_two(data="input.txt"):
    path = loop(data)
    # Shoelace + Pick
    return int(
        (int(abs(sum((a.conjugate() * b).imag for a, b in pairwise(path)))) >> 1)
        + 1
        - (len(path) >> 1)
    )


def test():
    assert part_one("test.txt") == 8
    assert part_two("test2.txt") == 10
