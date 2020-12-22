# https://adventofcode.com/2020/day/20

from collections import deque
from functools import reduce
from itertools import product, takewhile
from math import sqrt


MONSTER = [[18], [0, 5, 6, 11, 12, 17, 18, 19], [1, 4, 7, 10, 13, 16]]
"""
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""


class Tile:
    def __init__(self, iden, data):
        def pair(s):
            return (int(s, 2), int(s[::-1], 2))

        self.angle = 0
        self.flipped = 0
        self.iden = int(iden)
        self.data = data
        l = len(data)
        self.borders = (
            pair(data[0]),
            pair("".join(data[i][-1] for i in range(l))),
            pair(data[-1][::-1]),
            pair("".join(data[i][0] for i in range(l))[::-1]),
        )

    def match(self, borders, angle, flipped):
        if borders == (None, None):
            return True

        self.angle = angle
        self.flipped = flipped

        t, l = borders
        if t is None and l == self[3][::-1]:
            return True
        if l is None and t == self[0][::-1]:
            return True
        if borders == (self[0][::-1], self[3][::-1]):
            return True
        return False

    def render(self, borders=False):
        data, n = self.data, len(self.data)
        if self.flipped:
            data = [l[::-1] for l in data]
        if self.angle == 1:
            data = ["".join([l[n - i - 1] for l in data]) for i in range(n)]
        elif self.angle == 2:
            data = ["".join([l[n - i - 1] for i in range(n)]) for l in data[::-1]]
        elif self.angle == 3:
            data = ["".join([l[i] for l in data[::-1]]) for i in range(n)]
        if borders:
            return data
        return [l[1:-1] for l in data[1:-1]]

    def monster(self):
        def check(i, j):
            data = self.render(True)
            return all(
                data[i + r][j + c] == "1" for r, mr in enumerate(MONSTER) for c in mr
            )

        n = len(self.data)
        monsters = sum(check(i, j) for i in range(n - 3) for j in range(n - 20))
        return (
            (
                sum(self.data[i][j] == "1" for i in range(n) for j in range(n))
                - 15 * monsters
            )
            if monsters
            else None
        )

    def __getitem__(self, i):
        d = self.flipped and -1 or 1
        return self.borders[(d * (i + self.angle)) % 4][::d]

    def __repr__(self):
        return f"<T{self.iden}@{self.angle}{'F' if self.flipped else ''}>"


def read(source):
    def tile(stream):
        while True:
            try:
                _, _, n = next(stream)[:-2].partition(" ")
            except StopIteration:
                break
            yield Tile(
                n,
                [
                    _[:-1].translate(str.maketrans(".#", "01"))
                    for _ in takewhile(lambda x: x != "\n", stream)
                ],
            )

    return {t.iden: t for t in tile(open(source))}


def solve(source):
    tiles = read(source)
    n = int(sqrt(len(tiles)))

    ts, ps = set(tiles.values()), deque()

    def current_tiles(ps):
        if not ps:
            return (None, None)
        if len(ps) < n:
            return (None, ps[-1][1])
        if len(ps) % n == 0:
            return (ps[-n][2], None)
        return (ps[-n][2], ps[-1][1])

    def bt():
        if not ts:
            return True

        ct = current_tiles(ps)

        for t, a, f in [
            (_, a, f)
            for f in range(2)
            for a in range(4)
            for _ in ts
            if _.match(ct, a, f)
        ]:
            t.angle, t.flipped = a, f
            ps.append(t)
            ts.remove(t)
            if bt():
                return True
            else:
                ts.add(ps.pop())
        return False

    for t, f, a in product(tiles.values(), range(2), range(4)):
        t.angle, t.flipped = a, f
        ps = deque([t])
        ts.remove(t)
        if bt():
            break
        ts.add(ps.pop())

    corners = ps[0].iden * ps[n - 1].iden * ps[-n].iden * ps[-1].iden

    data = [t.render() for t in ps]
    w = len(data[0])

    image = [
        l[i * w * n : (i + 1) * w * n]
        for i in range(n)
        for l in ["".join([t[i] for t in data]) for i in range(w)]
    ]

    t = Tile(0, image)

    for f, a in product(range(2), range(4)):
        t.flipped, t.angle = f, a
        if m := t.monster():
            return corners, m


assert (20899048083289, 273) == solve("2020/20/test.txt")
print(solve("2020/20/input.txt"))
