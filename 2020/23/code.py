# https://adventofcode.com/2020/day/23

from typing import Generator


class Circle:
    def __init__(self, array: list) -> None:
        self.current = array[0]
        self.map = {c: n for c, n in zip(array, array[1:] + [array[0]])}

    def pop(self) -> int:
        n = self.map[self.current]
        self.map[self.current] = self.map[n]
        return n

    def pick(self, n: int = 3) -> list[int]:
        return [self.pop() for _ in range(n)]

    def insert(self, dest: int, array: list[int]) -> None:
        l = len(self.map) + 1
        while dest in array or not dest:
            dest = (dest - 1) % l
        self.map.update(
            {c: n for c, n in zip([dest] + array, array + [self.map[dest]])}
        )

    def move(self, n: int = 3) -> None:
        self.insert(self.current - 1, self.pick(n))
        self.current = self.map[self.current]

    def state(self, small=True) -> int:
        def _gen() -> Generator[int, None, None]:
            s = 1
            while (s := self.map[s]) != 1:
                yield s

        return (
            small
            and int("".join(str(_) for _ in _gen()))
            or self.map[1] * self.map[self.map[1]]
        )


def read(source: str, pad: int = 9) -> Circle:
    return Circle(
        [int(_) for _ in open(source).readline()[:-1]] + list(range(10, pad + 1))
    )


def solve(source: str, pad: int = 9, moves: int = 100) -> int:
    cups = read(source, pad)
    for _ in range(moves):
        cups.move()
    return cups.state(pad == 9 and moves == 100)


assert 67384529 == solve("2020/23/test.txt")
print(solve("2020/23/input.txt"))
assert 149245887792 == solve("2020/23/test.txt", 1_000_000, 10_000_000)
print(solve("2020/23/input.txt", 1_000_000, 10_000_000))