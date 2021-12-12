# https://adventofcode.com/2021/day/12

import os
from collections import defaultdict


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


def graph(stream):
    g = defaultdict(list)
    for _ in stream:
        a, _, b = _.strip().partition("-")
        if b != "start":
            g[a].append(b)
        if a != "start":
            g[b].append(a)
    return g


def solve(datafile="input.txt"):
    g = graph(open(resolve(datafile)))

    def dfs(n="start", seen=set()):
        if n == "end":
            return 1
        if n[0].islower():
            seen.add(n)

        try:
            return sum(dfs(_, seen) for _ in g[n] if _ not in seen)
        finally:
            if n[0].islower():
                seen.remove(n)

    def dfs2(n="start", seen={}, s=False):
        if n == "end":
            return 1

        if n[0].islower():
            seen[n] = seen.setdefault(n, 0) + 1

        try:
            a = 0
            for _ in g[n]:
                ss = seen.setdefault(_, 0)
                if ss and s:
                    continue
                a += dfs2(_, seen, s or ss)
            return a
        finally:
            if n[0].islower():
                seen[n] -= 1

    return dfs(), dfs2()


def test():
    assert solve("test.txt") == (10, 36)


test()
print(solve())
