# https://adventofcode.com/2020/day/10

from functools import cache


def solve(source: str) -> tuple[int, int]:
    s = set(int(_) for _ in open(source))
    jolts = sorted(s)
    jolts.insert(0, 0)
    jolts.append(jolts[-1] + 3)

    counts = {}
    for (a, b) in zip(jolts, jolts[1:]):
        d = b - a
        counts[d] = counts.setdefault(d, 0) + 1

    m = max(s)

    @cache
    def dfs(i: int = 0) -> int:
        if i == m:
            return 1
        return sum(dfs(j) for j in range(i + 1, i + 4) if j in s)

    return counts[1] * counts[3], dfs()


assert (35, 8) == solve("test.txt")

print(solve("input.txt"))