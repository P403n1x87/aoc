# https://adventofcode.com/2020/day/3

from functools import reduce

LANDSCAPE = [[l == "#" for l in _[:-1]] for _ in open("input.txt")]


SLOPES = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
H, W = len(LANDSCAPE), len(LANDSCAPE[0])

print(
    reduce(
        int.__mul__,
        (sum(LANDSCAPE[i * sy][(i * sx) % W] for i in range(H // sy)) for sy, sx in SLOPES),
        1
    )
)