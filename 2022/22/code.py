# https://adventofcode.com/2022/day/22

from collections import defaultdict

from aoctk.data import Graph, Unbound2DGrid
from aoctk.input import get_groups


def parse(data):
    ps, (ins,) = get_groups(data)

    m = Unbound2DGrid(
        (
            (complex(j, i), c)
            for i, r in enumerate(ps)
            for j, c in enumerate(r)
            if c != " "
        )
    )
    p = map(complex, ins.replace("R", " 1j ").replace("L", " -1j ").split())

    return m, p, complex(ps[0].index(ps[0].strip()))


def solve(wrapping, data="input.txt"):
    m, p, z = parse(data)

    d = 1
    while True:
        s = next(p)
        for _ in range(int(abs(s))):
            if z + d not in m:
                w, e = wrapping(m, z, d)
                if m[w] != "#":
                    z, d = w, e
                continue
            elif m[z + d] == "#":
                break
            z += d
        try:
            d *= next(p)
        except StopIteration:
            break

    return (
        int(z.real + 1) * 4 + int(z.imag + 1) * 1000 + {1: 0, 1j: 1, -1: 2, -1j: 3}[d]
    )


def part_one(data="input.txt"):
    def wrapping(m, z, d):
        w = z
        while w - d in m:
            w -= d
        return w, d

    return solve(wrapping, data)


def part_two(data="input.txt"):
    m, _, _ = parse(data)

    # Determine the face size
    w, h = (_.hi + 1 for _ in m.bounds())
    l = max(w, h) - min(w, h)

    class Faces(Graph):
        def adj(self, n):
            return {
                (n + l * d, d)
                for d in (1j ** k for k in range(4))
                if n + l * d in self.data
            }

        def __iter__(self):
            return iter(self.data)

    fs = Faces(
        {
            complex(i, j)
            for i in range(0, w, l)
            for j in range(0, h, l)
            if complex(i, j) in m
        }
    )

    # Determine the wrapping rules based on how the faces are connected
    # The mapping tells for each face and each direction the destination face
    # and the direction to go in that face.
    wrs, c = defaultdict(dict), 24
    for s in fs:
        for t, d in fs.adj(s):
            wrs[s][d] = (t, d)
            c -= 1
    while c > 0:
        for s in fs:
            r = wrs[s]
            for k in (1j ** _ for _ in range(4)):
                if c <= 0:
                    break
                if k in r and k * 1j in r:
                    (t, phi), (q, psi) = r[k], r[k * 1j]
                    if phi * 1j not in wrs[t]:
                        wrs[t][phi * 1j] = (q, psi * 1j)
                        c -= 1
                    if -psi * 1j not in wrs[q]:
                        wrs[q][-psi * 1j] = (t, -phi * 1j)
                        c -= 1

    def wrapping(m, z, d):
        a = complex(z.real // l, z.imag // l) * l
        b, e = wrs[a][d]
        w = (z - a) - (l - 1) * d + (1 + 1j)
        rot = e / d
        tr = (l + 1) * (1 + 1j) * (1 - rot) / 2
        w = b + w * rot + tr - (1 + 1j)
        return w, e

    return solve(wrapping, data)


def test():
    assert part_one("test.txt") == 6032
    assert part_two("test.txt") == 5031
