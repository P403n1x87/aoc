# https://adventofcode.com/2022/day/9

from aoctk.input import get_tuples


def solve(n: int, data: str) -> int:
    ks = [0] * n
    v = {0}

    def update(h, t):
        d = h - t
        return (
            t
            if abs(d) < 1.5
            else t
            + complex(
                int(d.real / (abs(d.real) - 0.1)), int(d.imag / (abs(d.imag) - 0.1))
            )
        )

    for d, s in get_tuples(data):
        w = {"U": 1j, "D": -1j, "R": 1, "L": -1}[d]
        for _ in range(int(s)):
            ks[0] = ks[0] + w
            for i in range(1, n):
                ks[i] = update(ks[i - 1], ks[i])
            v.add(ks[-1])

    return len(v)


def part_one(data="input.txt"):
    return solve(2, data)


def part_two(data="input.txt"):
    return solve(10, data)


def test():
    assert part_one("test.txt") == 13
    assert part_two("test2.txt") == 36
