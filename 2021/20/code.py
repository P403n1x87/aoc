# https://adventofcode.com/2021/day/20

import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


class Image:

    DIRS = [complex(i, j) for j in range(-1, 2) for i in range(-1, 2)]

    def __init__(self, data, bg=0):
        self.data = data
        self.bg = bg
        self.bounds = (
            complex(min(_.real for _ in self.data), min(_.imag for _ in self.data)),
            complex(max(_.real for _ in self.data), max(_.imag for _ in self.data)),
        )

    def n(self, z):
        a = 0
        for _ in (self.data.get(z + e, self.bg) for e in self.DIRS):
            a = (a << 1) + _
        return a

    def enhance(self, algo):
        tl, br = self.bounds

        self.data = {
            z: algo[self.n(z)]
            for z in (
                complex(i, j)
                for j in range(int(tl.imag) - 1, int(br.imag) + 2)
                for i in range(int(tl.real) - 1, int(br.real) + 2)
            )
        }
        self.bg = algo[-1 * self.bg]
        self.bounds = tl + self.DIRS[0], br + self.DIRS[-1]


def solve(datafile="input.txt"):
    with open(resolve(datafile)) as f:
        algo = [_ == "#" for _ in f.readline().strip()]
        assert not f.readline().strip()
        img = Image(
            {
                complex(i, j): p == "#"
                for j, r in enumerate(enumerate(_.strip()) for _ in f)
                for i, p in r
            }
        )

        for _ in range(2):
            img.enhance(algo)
        p1 = sum(img.data.values())
        for _ in range(48):
            img.enhance(algo)

        return p1, sum(img.data.values())


def test():
    assert solve("test.txt") == (35, 3351)


test()
print(solve())
