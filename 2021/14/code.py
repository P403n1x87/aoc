# https://adventofcode.com/2021/day/14

import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


def solve(n, datafile="input.txt"):
    with open(resolve(datafile)) as f:
        ps, t = {}, f.readline().strip()

        for k in (a + b for a, b in zip(t, t[1:])):
            ps[k] = ps.setdefault(k, 0) + 1

        assert not f.readline().strip()

        rs = {
            p: frozenset([p[0] + s, s + p[1]])
            for p, _, s in (_.strip().partition(" -> ") for _ in f)
        }

        for _ in range(n):
            nps = {}
            for p, c in ps.items():
                for s in rs[p]:
                    nps[s] = nps.setdefault(s, 0) + c
            ps = nps

        es = {}
        for p, c in ps.items():
            for e in p:
                es[e] = es.setdefault(e, 0) + c

        es[t[0]] += 1
        es[t[-1]] += 1

        return (max(es.values()) - min(es.values())) >> 1


def test():
    assert solve(10, "test.txt") == 1588
    assert solve(40, "test.txt") == 2188189693529


test()
print(solve(10))
print(solve(40))
