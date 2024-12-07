# https://adventofcode.com/2024/day/7

from aoctk.input import get_lines


def operate(target: int, numbers: list[int], ops: callable) -> bool:
    if len(numbers) == 1:
        return numbers[0] == target

    if numbers[0] > target:
        return False

    a, n, *rest = numbers
    return any(operate(target, [m, *rest], ops) for m in ops(a, n))


def solve(data: str, ops: callable) -> int:
    return sum(
        int(target) * operate(int(target), [int(n) for n in ns.split(" ")], ops)
        for target, _, ns in (op.partition(": ") for op in get_lines(data))
    )


def part_one(data="input.txt"):
    return solve(data, lambda a, n: (a + n, a * n))


def part_two(data="input.txt"):
    return solve(data, lambda a, n: (a + n, a * n, int(str(a) + str(n))))


def test():
    assert (_ := part_one("test.txt")) == 3749, _
    assert (_ := part_two("test.txt")) == 11387, _
