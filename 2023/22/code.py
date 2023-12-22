# https://adventofcode.com/2023/day/22

from collections import defaultdict, deque

from aoctk.input import get_lines


def stack(data: str) -> tuple[int, dict, dict]:
    bs = []
    for line in get_lines(data):
        a, _, b = line.partition("~")
        *b1, z1 = (int(_) for _ in a.split(","))
        *b2, z2 = (int(_) for _ in b.split(","))
        d = complex(*b2) - (s := complex(*b1))
        n, m, h = d / abs(d) if d else 0, int(abs(d)) + 1, z2 - z1 + 1
        bs.append((z1, {p: h for p in (s + n * i for i in range(m))}))
    bs = sorted(bs, key=lambda _: _[0])

    s, m, g = defaultdict(int), defaultdict(int), {}
    for i, (_, b) in enumerate(bs, 1):
        z = max(s[p] for p in b)
        g[i] = {m[p] for p in b if s[p] == z}
        for p, h in b.items():
            s[p], m[p] = z + h, i

    ig = defaultdict(set)
    for i, s in g.items():
        for j in s:
            ig[j].add(i)

    return len(bs), g, ig


def part_one(data="input.txt"):
    n, g, ig = stack(data)
    return sum(not ig[i] or all(len(g[_]) > 1 for _ in ig[i]) for i in range(1, n + 1))


def part_two(data="input.txt"):
    c, n, g, ig = 0, *stack(data)
    for i in range(1, n + 1):
        fs, q = {i}, deque([i])
        while q:
            q.extend(f := {_ for _ in ig[q.popleft()] if not (g[_] - fs)})
            fs |= f
        c += len(fs) - 1
    return c


def test():
    assert part_one("test.txt") == 5
    assert part_two("test.txt") == 7
