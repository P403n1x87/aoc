# https://adventofcode.com/2024/day/20


from aoctk.data import Graph
from aoctk.input import get_bounded_2d_grid as get_track
from aoctk.metric import manhattan2d as m2d


class Track(Graph):
    def adj(self, p):
        return self.data.adj(p)


def solve(data, ps, m):
    (ph,) = Track(r := get_track(data)).shortest_paths(r.find("S"), r.find("E"))

    def ways(p, q):
        if p == q:
            return

        def ws(ph, q):
            if (p := ph[-1]) == q:
                yield ph
                return
            if (dr := q.real - p.real) != 0:
                yield from ws([*ph, p + dr / abs(dr)], q)
            if (di := q.imag - p.imag) != 0:
                yield from ws([*ph, p + 1j * di / abs(di)], q)

        yield from ws([p], q)

    return sum(
        r.get(w[1]) == "#" and not (j + 1 < len(ph) and w[-1] == ph[j + 1])
        for d in range(2, m + 1)
        for i, p in enumerate(ph[: -ps - d])
        for j in (
            j for j, q in enumerate(ph[i + d + ps :], i + d + ps) if m2d(p, q) == d
        )
        for w in ways(p, ph[j])
    )


def part_one(data="input.txt", ps=100, m=2):
    return solve(data, ps, m)


def part_two(data="input.txt", ps=100, m=20):
    return solve(data, ps, m)


def test():
    assert (_ := part_one("test.txt")) == 0, _
    assert (_ := part_one("test.txt", 64)) == 1, _
    assert (_ := part_one("test.txt", 20)) == 5, _
    assert (_ := part_one("test.txt", 2)) == 44, _
    assert (_ := part_two("test.txt", 76, 6)) == 3, _

    assert (_ := part_two("test.txt")) is None, _
