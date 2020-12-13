# https://adventofcode.com/2020/day/9

from collections import deque


def check(n: int, win: deque) -> bool:
    s = set(win)
    for m in s:
        if n - m in s:
            return True
    return False


def solve(source: str, preamble: int = 25) -> tuple[int, int]:
    def find(n: int, full: list) -> int:
        s, j = full[0], 1
        for i in range(len(full) - 1):
            while s < n:
                t = s
                s += full[j]
                if s == n:
                    l = full[i : j + 1]
                    return min(l) + max(l)
                if s > n:
                    s = t  # undo
                    break
                j += 1
            s -= full[i]

    win = deque(maxlen=preamble)
    full = []

    for _ in open(source):
        n = int(_[:-1])
        full.append(n)
        if len(win) == preamble and not check(n, win):
            return n, find(n, full)
        win.append(n)


assert (127, 62) == solve("test.txt", 5)
print(solve("input.txt"))