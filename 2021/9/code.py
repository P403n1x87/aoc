# https://adventofcode.com/2021/day/9

import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


class HeightMap(dict):
    def h(self, z):
        return self[z.real].get(z.imag, 9) if z.real in self else 9

    def basin(self, z):
        q = {z}
        seen = set()
        while q:
            w = q.pop()
            seen.add(w)
            for e in (1, -1, 1j, -1j):
                p = w + e
                if p not in seen and self.h(p) < 9:
                    q.add(p)
        return len(seen)

    def __iter__(self):
        return (complex(i, j) for i in range(len(self)) for j in range(len(self[0])))


def solve(datafile="input.txt"):
    m = HeightMap(
        enumerate(
            dict(enumerate((int(_) for _ in line.strip())))
            for line in open(resolve(datafile))
        )
    )

    ls = [p for p in m if m.h(p) < min(m.h(p + e) for e in (1, -1, 1j, -1j))]

    return (
        sum(1 + m.h(p) for p in ls),
        eval("*".join([str(_) for _ in sorted([m.basin(p) for p in ls])[-3:]])),
    )


def test():
    assert solve("test.txt") == (15, 1134)


test()
print(solve())
