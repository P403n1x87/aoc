# https://adventofcode.com/2021/day/23

import heapq
import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


def rooms(stream):
    stream.readline()
    stream.readline()
    rs = [[] for _ in range(4)]
    for line in stream:
        if line.startswith("  ##"):
            break
        for i in range(4):
            rs[i].insert(0, ord(line[3 + 2 * i]) - ord("A"))
    return rs


def adj(s, c):
    rs, h = eval(s)

    for r in range(4):
        if rs[r] and set(rs[r]) != {r}:
            a = rs[r].pop()
            for dirs in (range(r + 1, -1, -1), range(r + 2, 7)):
                for p in dirs:
                    if h[p] is not None:
                        break
                    h[p] = a
                    d = abs(2 * (r - p) + 3) + (p % 6 != 0) + c - 1 - len(rs[r])
                    if not (a == 3 and d >= 6):
                        yield (str((rs, h)), d * 10 ** a)
                    h[p] = None
            rs[r].append(a)

    for p in range(7):
        if h[p] is not None and len(rs[h[p]]) < c and all(_ == h[p] for _ in rs[h[p]]):
            r = h[p]
            if all(_ is None for _ in h[p + 1 : r + 2] + h[r + 2 : p]):
                h[p] = None
                d = abs(2 * (r - p) + 3) + (p % 6 != 0) + c - 1 - len(rs[r])
                rs[r].append(r)
                yield (str((rs, h)), d * 10 ** r)
                h[p] = rs[r].pop()


def dijkstra(s):
    rs, _ = eval(s)
    rc, seen, q = len(rs[0]), set(), [(0, s)]
    f = str(([[i] * rc for i in range(4)], [None] * 7))
    heapq.heapify(q)

    while q:
        d, s = heapq.heappop(q)
        if s == f:
            return d
        if s in seen:
            continue
        seen.add(s)
        for t, c in adj(s, rc):
            heapq.heappush(q, (d + c, t))


def solve(datafile="input.txt"):
    with open(resolve(datafile)) as f:
        return dijkstra(str((rooms(f), [None] * 7)))


def test():
    assert solve("test.txt") == 12521
    assert solve("test2.txt") == 44169


test()
print(solve("input.txt"))
print(solve("input2.txt"))
