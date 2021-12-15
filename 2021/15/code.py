# https://adventofcode.com/2021/day/15

import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


class Cave(dict):
    def __init__(self, data, repeat=1):
        super().__init__(data)
        self.repeat = repeat
        self.goal = (
            complex(max(_.real for _ in self) + 1, max(_.imag for _ in self) + 1)
            * repeat
            - 1
            - 1j
        )
        self._size = complex(
            max(_.real for _ in self) + 1, max(_.imag for _ in self) + 1
        )
        self.size = self._size * repeat

    def __getitem__(self, z):
        if z.real < 0 or z.imag < 0:
            raise KeyError(z)
        fr, fi = int(z.real / self._size.real), int(z.imag / self._size.imag)
        if fr >= self.repeat or fi >= self.repeat:
            raise KeyError(z)
        cr, ci = int(z.real) % int(self._size.real), int(z.imag) % int(self._size.imag)
        return ((super().__getitem__(complex(cr, ci)) - 1 + fr + fi) % 9) + 1

    def __contains__(self, z: object) -> bool:
        return 0 <= z.real < self.size.real and 0 <= z.imag < self.size.imag

    def a_star(self):
        s = {0}  # TODO[perf]: use min-heap instead
        g, f = {0: 0}, {0: abs(self.goal)}

        while s:
            if (v := min(s, key=lambda v: f[v])) == self.goal:
                return g[v]
            s.remove(v)
            for e in (_ for _ in (1j ** k for k in range(4)) if v + _ in self):
                alt = g[v] + self[v + e]
                if alt < g.get(v + e, 1e9):
                    g[v + e] = alt
                    f[v + e] = alt + abs(v + e - self.goal)
                    s.add(v + e)


def solve(repeat=1, datafile="input.txt"):
    return Cave(
        {
            complex(i, j): int(v)
            for j, r in enumerate(
                enumerate((int(_) for _ in line.strip()))
                for line in open(resolve(datafile))
            )
            for i, v in r
        },
        repeat,
    ).a_star()


def test():
    assert solve(1, "test.txt") == 40
    assert solve(5, "test.txt") == 315


test()
print(solve())
print(solve(5))
