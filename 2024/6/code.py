# https://adventofcode.com/2024/day/6

from aoctk.data import M4
from aoctk.input import get_bounded_2d_grid as get_data


def patrol(grid, p, d):
    ps = {p}
    ds = {(p, d)}
    while True:
        if grid.get(e := p + d) == "#":
            d *= 1j
        else:
            p = e
            if not grid.within(p):
                return ps  # out of the lab
            ps.add(p)
            if (p, d) in ds:
                return None  # loop
            ds.add((p, d))


def part_one(data="input.txt"):
    grid = get_data(data)
    (p,) = {k for k, v in grid.items() if v != "#"}
    return len(patrol(grid, p, M4[grid[p]]))


def part_two(data="input.txt"):
    grid = get_data(data)
    (p,) = {k for k, v in grid.items() if v != "#"}
    d = M4[grid[p]]
    ps = patrol(grid, p, d) - {p}

    c = 0
    for o in ps:
        grid[o] = "#"
        if patrol(grid, p, d) is None:
            c += 1
        del grid[o]
    return c


def test():
    assert (_ := part_one("test.txt")) == 41, _
    assert (_ := part_two("test.txt")) == 6, _
