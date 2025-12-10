# https://adventofcode.com/2025/day/10

from aoctk.data import Graph
from aoctk.input import get_tuples


class Machine(Graph):
    def __init__(self, data: tuple[str, list[str], str]) -> None:
        super().__init__(data)

        lights, *buttons, jolts = data

        self.end = int(lights[1:-1][::-1].replace(".", "0").replace("#", "1"), 2)
        self.buttons = [sum(1 << int(b) for b in _[1:-1].split(",")) for _ in buttons]
        self.jolts = {int(j) for j in jolts[1:-1].split(",")}

    def adj(self, n: int) -> list[int]:
        return [n ^ b for b in self.buttons]

    def configure(self) -> int:
        return self.dijkstra(0, self.end)


def part_one(data="input.txt"):
    return sum(Machine(machine_data).configure() for machine_data in get_tuples(data))


def part_two(data="input.txt"):
    pass


def test():
    assert (_ := part_one("test.txt")) == 7, _
    assert (_ := part_two("test.txt")) is None, _
