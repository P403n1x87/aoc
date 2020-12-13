# https://adventofcode.com/2020/day/12

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Vector:
    x: int
    y: int

    def __mul__(self, other: "Vector") -> "Vector":  # Complex structure
        return Vector(
            self.x * other.x - self.y * other.y, self.x * other.y + self.y * other.x
        )

    def __rmul__(self, other: int) -> "Vector":  # Scaling
        return Vector(self.x * other, self.y * other)

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    @property
    def manhattan(self) -> int:
        return abs(self.x) + abs(self.y)


N, E, S, W = Vector(1, 0), Vector(0, 1), Vector(-1, 0), Vector(0, -1)
POWS = [1, E, -1, W]
assert E * E == S
assert E * E * E == W


class Ship(ABC):
    def __init__(self) -> None:
        self.pos = Vector(0, 0)

    @abstractmethod
    def operate(self, op: str, n: int) -> None:
        pass

    def instruct(self, ins: str) -> None:
        self.operate(ins[0], int(ins[1:]))

    @property
    def distance(self) -> int:
        return self.pos.manhattan


class ShipWithDirection(Ship):
    def __init__(self) -> None:
        super().__init__()
        self.dir = 0

    def operate(self, o: str, n: int) -> None:
        if o == "F":
            self.pos += n * [E, S, W, N][self.dir]
        elif o == "R":
            self.dir = (self.dir + n // 90) & 3
        elif o == "L":
            self.dir = (self.dir - n // 90) & 3
        else:
            self.pos += n * {"N": N, "S": S, "E": E, "W": W}[o]


class ShipWithWaypoint(Ship):
    def __init__(self) -> None:
        super().__init__()
        self.wp = 10 * E + N

    def operate(self, o: str, n: int) -> None:
        if o == "F":
            self.pos += n * self.wp
        elif o == "R":
            self.wp = POWS[n // 90] * self.wp
        elif o == "L":
            self.wp = POWS[4 - n // 90] * self.wp
        else:
            self.wp += n * {"N": N, "S": S, "E": E, "W": W}[o]


def solve(source) -> tuple[int, int]:
    ships = [ShipWithDirection(), ShipWithWaypoint()]
    for _ in open(source):
        for s in ships:
            s.instruct(_)
    return tuple(s.distance for s in ships)


assert (25, 286) == solve("test.txt")
print(solve("input.txt"))