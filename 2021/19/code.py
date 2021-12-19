# https://adventofcode.com/2021/day/19

import os
from collections import defaultdict
from functools import cached_property


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


class Vec(tuple):
    def d(self, other):
        return sum((a - b) ** 2 for a, b in zip(self, other))

    def dot(self, other):
        return sum(a * b for a, b in zip(self, other))

    def __sub__(self, other):
        return Vec([a - b for a, b in zip(self, other)])

    def __add__(self, other):
        return Vec([a + b for a, b in zip(self, other)])

    def __mul__(self, other):
        return Vec([a * other for a in self])


class Mat(list):
    def __call__(self, v):
        return Vec([_.dot(v) for _ in self])


class Scanner(list):
    @classmethod
    def read(cls, stream):
        s = cls()
        s.aligned, s.pos = False, Vec([0, 0, 0])
        for _ in (_.strip() for _ in stream):
            if not _:
                break
            if _.startswith("---"):
                continue
            s.append(Vec([float(c) for c in _.split(",")]))
        if not s:
            raise IOError()
        return s

    @cached_property
    def dists(self):
        ds = defaultdict(list)
        for i in range(len(self)):
            for j in range(i + 1, len(self)):
                ds[self[i].d(self[j])].append((self[i], self[j]))
        return ds

    def overlap(self, other):
        sds = self.dists
        ods = other.dists

        c = [_ for _ in sds.keys() if _ in ods.keys()]
        if len(c) < 66:  # 12 * 11 / 2
            return []
        return [(sds[_][0], ods[_][0]) for _ in c if len(sds[_]) == len(ods[_]) == 1]

    def m(self, other):
        return sum(abs(a - b) for a, b in zip(self.pos, other.pos))

    def align(self, other):
        if other.aligned:
            return other

        if not (o := self.overlap(other)):
            return other

        for (sra, srb), (ora, orb) in o:
            sv = sra - srb
            if len(set(sv)) == 3:
                ov = ora - orb
                a = Mat(
                    [
                        Vec(
                            [
                                int(sv[i] / ov[j]) if abs(sv[i] / ov[j]) == 1 else 0
                                for j in range(3)
                            ]
                        )
                        for i in range(3)
                    ]
                )
                t = ((sra + srb) - a(ora + orb)) * 0.5

                al = Scanner((t + a(b) for b in other))
                if len(set(self) & set(al)) >= 12:
                    al.aligned = True
                    al.pos = t
                    return al


def solve(datafile="input.txt"):
    ss = []
    with open(resolve(datafile)) as f:
        while True:
            try:
                ss.append(Scanner.read(f))
            except IOError:
                break

    g = defaultdict(set)
    for i in range(len(ss)):
        for j in range(i + 1, len(ss)):
            if ss[i].overlap(ss[j]):
                g[i].add(j)
                g[j].add(i)

    os = {0}
    ss[0].aligned = True
    while os:
        n = os.pop()
        for i in g[n]:
            if not ss[i].aligned:
                ss[i] = ss[n].align(ss[i])
                os.add(i)

    assert all(_.aligned for _ in ss)

    return (
        len({_ for s in ss for _ in s}),
        int(max(ss[i].m(ss[j]) for i in range(len(ss)) for j in range(len(ss)))),
    )


def test():
    assert solve("test.txt") == (79, 3621)


test()
print(solve())
