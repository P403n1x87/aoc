# https://adventofcode.com/2024/day/12

from typing import Generator

from aoctk.data import D4
from aoctk.input import get_bounded_2d_grid as get_grid


class Region(set):
    def area(self) -> int:
        return len(self)

    def perimeter(self) -> int:
        return sum(p + d not in self for p in self for d in D4)

    def sides(self) -> int:
        seen, sides = set(), 0
        while True:  # there might be holes!
            d, n = 1, 1j  # direction and normal

            try:
                p = next(
                    _ for _ in self if (_, d) not in seen and _ + n not in self
                )  # start from a south side
                sides += 1
            except StopIteration:
                break  # nothing more to walk

            while True:  # go around the perimeter
                seen.add((p, d))

                if p + n in self:
                    t, r, c = n, 1j, 0
                elif p + d in self:
                    t, r, c = d, 1, 1
                else:
                    t, r, c = 0, -1j, 0
                if (p := p + t, d := d * r) in seen:
                    break

                n = d * 1j

                sides += r != 1  # if we rotated we have a new side

            sides -= c  # do not double-count side if we went straight last

        return sides


def regions(garden: dict) -> Generator[Region, None, None]:
    while garden:
        p, v = garden.popitem()
        ps, q = {p}, {p}
        while q:
            s = q.pop()
            for d in D4:
                if (n := s + d) not in ps and garden.get(n) == v:
                    q.add(n)
                    ps.add(n)
                    del garden[n]
        yield Region(ps)


def part_one(data="input.txt"):
    return sum(r.area() * r.perimeter() for r in regions(get_grid(data)))


def part_two(data="input.txt"):
    return sum(r.area() * r.sides() for r in regions(get_grid(data)))


def test():
    assert (_ := part_one("test.txt")) == 1930, _
    assert (_ := part_two("test.txt")) == 1206, _
