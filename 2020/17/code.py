# https://adventofcode.com/2020/day/17

from itertools import product


def read(source: str, dim: int = 3) -> set[tuple[int, ...]]:
    return {
        (i, j, *([0] * (dim - 2)))
        for i, _ in enumerate(open(source))
        for j, c in enumerate(_)
        if c == "#"
    }


def rule(pocket: set[tuple[int, ...]], c: tuple[int, ...]) -> bool:
    n = sum(e in pocket for e in product(*(range(a - 1, a + 2) for a in c)))
    return n == 3 or c in pocket and n == 4


def solve(source: str, dim: int = 3) -> int:
    pocket = read(source, dim)

    for _ in range(6):
        pocket = {
            c
            for c in product(
                *(
                    range(a - 1, b + 2)
                    for a, b in tuple(
                        (min(c), max(c))
                        for c in ({c[i] for c in pocket} for i in range(dim))
                    )
                )
            )
            if rule(pocket, c)
        }

    return len(pocket)


assert 112 == solve("test.txt", 3)
assert 848 == solve("test.txt", 4)
print(solve("input.txt", 3), solve("input.txt", 4))