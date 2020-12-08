# Problem: https://adventofcode.com/2020/day/1

from typing import Optional


h = set(int(_) for _ in open("input.txt"))


def solve(s: set, n: int, t: int = 2020) -> Optional[int]:
    """O(len(s)^(n-1)) worst case"""
    if t < 0 or n < 1:
        return None

    if n == 1 and t in s:
        return t

    for a in s:
        if r := solve(s, n - 1, t - a):
            return a * r

    return None


print(f"Part 1: {solve(h, 2) or ':('}")
print(f"Part 2: {solve(h, 3) or ':('}")
