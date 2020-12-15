# https://adventofcode.com/2020/day/15


def solve(source: str, turns: int = 2020) -> int:
    d = {int(n): t for t, n in enumerate(open(source).read().split(","))}
    n = 0
    for t in range(len(d), turns - 1):
        d[n], n = t, t - d.get(n, t)
    return n


assert 0 == solve("test.txt", 10)
assert 436 == solve("test.txt")

print(solve("input.txt"))
print(solve("input.txt", 30_000_000))
