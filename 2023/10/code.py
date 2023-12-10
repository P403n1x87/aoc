# https://adventofcode.com/2023/day/10

from collections import deque

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
    r, s = 0, grid.find("S")  # rotation: +1 CW, -1 CCW
    for d in D4:
        p, path = s, []
        while d:
            path.append(p)
            if grid[p := p + d] == "S":
                break
            r += (d.conjugate() * (d := D.get(grid[p], {}).get(d, 0))).imag
        else:
            continue
        break
    return path, r / abs(r), grid


def part_one(data="input.txt"):
    return len(loop(data)[0]) >> 1


def part_two(data="input.txt"):
    path, r, island = loop(data)
    d = path[1] - path[0]
    spath, inside = set(path), set()

    # Get all the inside points close to the path considering the rotation
    for p in path[1:]:
        if p + (n := d * 1j * r) not in spath:
            inside.add(p + n)
        d = D[island[p]][d]
        if island[p] not in ("-", "|"):  # Corners have two directions
            if p + (n := d * 1j * r) not in spath:
                inside.add(p + n)

    # Get all the inside points connected to the already found ones
    q = deque(inside)
    while q and (p := q.popleft()):
        for d in D4:
            if (np := p + d) not in inside and np not in spath:
                inside.add(np)
                q.append(np)

    return len(inside)


def test():
    assert part_one("test.txt") == 8
    assert part_two("test2.txt") == 10
