# https://adventofcode.com/2021/day/13

import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


class Page(set):
    @classmethod
    def read(cls, stream):
        p = cls()
        for _ in (_.strip() for _ in stream):
            if not _:
                break
            p.add(complex(*(int(n) for n in _.split(",", maxsplit=1))))
        return p

    def fold(self, z):
        n = z / abs(z)
        for k in [_ for _ in self if (n.conjugate() * _).real > abs(z)]:
            self.remove(k)
            self.add(k - 2 * (n * (n.conjugate() * k).real - z))

    def print(self):
        for j in range(max(int(_.imag) for _ in self) + 1):
            for i in range(max(int(_.real) for _ in self) + 1):
                print(("#" if complex(i, j) in self else " ") * 2, end="")
            print()


def solve(datafile="input.txt"):
    with open(resolve(datafile)) as f:
        p, e = Page.read(f), None
        for a, _, v in (_.strip().partition("=") for _ in f):
            p.fold(int(v) * (1 if a[-1] == "x" else 1j))
            e = e or len(p)
        p.print()
        return e


def test():
    assert solve("test.txt") == 17


test()
print(solve())
