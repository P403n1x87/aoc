# https://adventofcode.com/2023/day/19

from collections import defaultdict, deque
from itertools import dropwhile
from math import prod

from aoctk.data import Range
from aoctk.data import weighted_union_size as wusize
from aoctk.func import iterate
from aoctk.input import get_groups as gs


class BaseWorkflow:
    def __init__(self, spec):
        name, _, rs = spec[:-1].partition("{")
        self.name = name
        self.rules = [
            self.rule(c, t)
            for c, t in (
                (c, t) if t else (None, c)
                for c, _, t in (r.partition(":") for r in rs.split(","))
            )
        ]

    @classmethod
    def rule(cls, c, t):
        return c, t

    def __call__(self, part):
        raise NotImplementedError()


def part_one(data="input.txt"):
    class Workflow(BaseWorkflow):
        @classmethod
        def rule(cls, c, t):
            return compile(c or str(True), __file__, "eval"), t

        def __call__(self, part):
            return next(dropwhile(lambda r: not eval(r[0], {}, part), self.rules))[1]

    rw, rp = gs(data)
    ws = {w.name: w for w in (Workflow(w) for w in rw)}
    ps = [eval(f"dict({p[1:-1]})") for p in rp]

    return sum(
        sum(p.values())
        for p in (
            p
            for p in ps
            if (
                next(
                    dropwhile(
                        lambda t: t not in {"A", "R"}, iterate(lambda t: ws[t](p), "in")
                    )
                )
                == "A"
            )
        )
    )


def part_two(data="input.txt"):
    class Part:
        I = {q: i for i, q in enumerate("xmas")}

        def __init__(self, ranges):
            self.ranges = ranges

        def slice(self, how):
            rs, crs = list(self.ranges), list(self.ranges)
            q, s, *ds = how
            n, i = int("".join(ds)), self.I[q]
            r = rs[i]
            rs[i], crs[i] = (
                (r & Range(1, n - 1), r & Range(n, 4000))
                if s == "<"
                else (r & Range(n + 1, 4000), r & Range(1, n))
            )
            return Part(rs), Part(crs)

        def __and__(self, other):
            return Part([r & o for r, o in zip(self.ranges, other.ranges)]) or None

        def __bool__(self):
            return all(r is not None for r in self.ranges)

        def __len__(self):
            return prod(len(r) for r in self.ranges)

    class Workflow(BaseWorkflow):
        def __call__(self, parts):
            r = defaultdict(list)
            for c, t in self.rules:
                new_parts = []
                for part in parts:
                    if c is None:
                        r[t].append(part)
                        continue
                    k, p = part.slice(c)
                    if k:
                        r[t].append(k)
                    if p:
                        new_parts.append(p)
                parts = new_parts
            r.pop("R", None)
            return r

    ws = {w.name: w for w in (Workflow(w) for w in next(gs(data)))}

    q, a = deque([{"in": [Part([Range(1, 4000)] * 4)]}]), []
    while q:
        for w, ps in q.popleft().items():
            a.extend((s := ws[w](ps)).pop("A", []))
            if s:
                q.append(s)

    return wusize(Range.weighted_union(a))


def test():
    assert part_one("test.txt") == 19114
    assert part_two("test.txt") == 167409079868000
