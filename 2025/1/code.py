# https://adventofcode.com/2025/day/1

from aoctk.input import get_lines


def part_one(data="input.txt"):
    a, c = 50, 0
    for line in get_lines(data):
        a += int(line.replace("R", "").replace("L", "-"))
        c += a % 100 == 0
    return c


def part_two(data="input.txt"):
    a, c = 50, 0
    for line in get_lines(data):
        v = int(line.replace("R", "").replace("L", "-"))
        c += (n := abs(v) // 100)
        b = a + v - 100 * n * int(v / abs(v))
        c += b >= 100 or (a > 0 and a * b <= 0)
        a = b % 100
    return c


def test():
    assert (_ := part_one("test.txt")) == 3, _
    assert (_ := part_two("test.txt")) == 6, _
