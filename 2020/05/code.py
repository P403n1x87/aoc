from functools import reduce
from typing import Callable


def encode(seat: str) -> int:
    def binarize(hi: str) -> Callable[[int, str], int]:
        return lambda x, y: (x << 1) | (y == hi)

    return (reduce(binarize("B"), seat[:7], 0) << 3) | reduce(
        binarize("R"), seat[7:10], 0
    )


seats = sorted(encode(_) for _ in open("input.txt"))

a, b = seats[0], seats[-1]

print(b)  # part 1

l, h = 0, len(seats)
while l <= h:
    i = (h + l) >> 1
    if seats[i] > a + i:
        h = i - 1
    else:
        l = i + 1

print(a + i + 1)  # part 2
