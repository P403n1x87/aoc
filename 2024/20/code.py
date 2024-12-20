# https://adventofcode.com/2024/day/20


from aoctk.data import Graph
from aoctk.input import get_bounded_2d_grid as get_track
from aoctk.metric import manhattan2d as m2d


class Track(Graph):
    def adj(self, p):
        return self.data.adj(p)


def solve(data, save, max_cheat):
    (ph,) = Track(r := get_track(data)).shortest_paths(r.find("S"), r.find("E"))
    return sum(
        1
        for i, p in enumerate(ph[: -save - 2])
        for j, q in enumerate(ph[i + 2 + save :], i + 2 + save)
        if (md := m2d(p, q)) <= max_cheat and j - i >= save + md
    )


def part_one(data="input.txt", save=100, max_cheat=2):
    return solve(data, save, max_cheat)


def part_two(data="input.txt", save=100, max_cheat=20):
    return solve(data, save, max_cheat)


def test():
    assert (_ := part_one("test.txt")) == 0, _
    assert (_ := part_one("test.txt", 64)) == 1, _
    assert (_ := part_one("test.txt", 20)) == 5, _
    assert (_ := part_one("test.txt", 2)) == 44, _
    assert (_ := part_two("test.txt", 76, 6)) == 1, _
