# https://adventofcode.com/2022/day/15

from dataclasses import dataclass

from aoctk.data import Range, weighted_union_size
from aoctk.input import get_lines
from aoctk.metric import manhattan2d as md


@dataclass
class Sensor:
    pos: complex
    beacon: complex
    distance: int

    def __init__(self, desc):
        self.pos, self.beacon = eval(
            desc.replace("Sensor at x=", "complex(")
            .replace("y=", "")
            .replace(": closest beacon is at x=", "), complex(")
            + ")"
        )
        self.distance = md(self.beacon, self.pos)


def get_intervals(y, sensors):
    beacons = tuple({int(_.beacon.real) for _ in sensors if _.beacon.imag == y})
    intervals = []

    for s in sensors:
        left = s.distance - int(abs(s.pos.imag - y))
        if left >= 0:
            intervals.extend(
                Range(int(s.pos.real - left), int(s.pos.real + left)).split(*beacons)
            )

    return Range.weighted_union(intervals)


def part_one(data="input.txt", y=2000000):
    return weighted_union_size(get_intervals(y, [Sensor(_) for _ in get_lines(data)]))


def part_two(data="input.txt", y=2000000, lo=0, hi=4000000):
    sensors = [Sensor(_) for _ in get_lines(data)]
    beacons = {_.beacon for _ in sensors}
    v_max = hi - lo + 1

    for cy in (
        _ for p in zip(range(y - 1, lo - 1, -1), range(y + 1, hi + 1)) for _ in p
    ):
        intervals = get_intervals(cy, sensors)
        for i, _ in intervals:
            i.clip(lo, hi)

        if weighted_union_size(intervals) < v_max:
            (x,) = set(range(lo, hi + 1)) - set.union(
                *(set(i) for i, w in intervals if w > 0)
            )
            if complex(x, cy) not in beacons:
                return x * 4000000 + cy


def test():
    assert part_one("test.txt", 10) == 26
    assert part_two("test.txt", 10, 0, 20) == 56000011
