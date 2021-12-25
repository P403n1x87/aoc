# https://adventofcode.com/2021/day/25

import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


def solve(datafile="input.txt"):
    d = {
        complex(i, j): v
        for j, r in enumerate(enumerate(_.strip()) for _ in open(resolve(datafile)))
        for i, v in r
        if v != "."
    }
    e = {p for p, v in d.items() if v == ">"}
    s = {p for p, v in d.items() if v == "v"}
    w = int(max(_.real for _ in d) + 1)
    h = int(max(_.imag for _ in d) + 1)

    for i, _ in enumerate(iter(int, 1)):
        moved = False

        n = set()
        for c in e:
            m = complex((c.real + 1) % w, c.imag)
            if m not in s and m not in e:
                n.add(m)
                moved = True
            else:
                n.add(c)
        e = n

        n = set()
        for c in s:
            m = complex(c.real, (c.imag + 1) % h)
            if m not in s and m not in e:
                n.add(m)
                moved = True
            else:
                n.add(c)
        s = n

        if not moved:
            break

    return i + 1


def test():
    assert solve("test.txt") == 58


test()
print(solve())
