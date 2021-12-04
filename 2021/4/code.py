# https://adventofcode.com/2021/day/4

import os
from typing import TextIO


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


class Board(list):
    def __init__(self, data):
        if not data[0]:
            raise EOFError()
        super().__init__(data)

    def check(self):
        for r in self:
            if r == ["*"] * 5:
                return True

        for i in range(5):
            if all(self[j][i] == "*" for j in range(5)):
                return True

        return False

    def mark(self, n):
        for r in self:
            for i, e in enumerate(r):
                if e == n:
                    r[i] = "*"
                    return

    def score(self, n):
        return int(n) * sum(
            int(self[i][j]) if self[i][j] != "*" else 0
            for i in range(5)
            for j in range(5)
        )

    @classmethod
    def read(cls, stream: TextIO):
        return cls([stream.readline().strip().split() for _ in range(5)])


def solve(datafile="input.txt"):
    ns = boards = None
    with open(resolve(datafile)) as f:
        ns = f.readline().strip().split(",")
        assert not f.readline().strip()
        boards = []
        while True:
            try:
                boards.append(Board.read(f))
            except EOFError:
                break
            assert not f.readline().strip()

    bs = []
    for n in ns:
        ws = []
        for i, b in enumerate(boards):
            b.mark(n)
            if b.check():
                bs.append((n, b))
                ws.insert(0, i)
        for i in ws:
            boards.pop(i)
        if not boards:
            break

    (nf, first), (nl, last) = bs[0], bs[-1]

    return first.score(nf), last.score(nl)


def test():
    assert solve("test.txt") == (4512, 1924)


test()
print(solve())
