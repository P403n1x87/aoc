# https://adventofcode.com/2021/day/5

import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


def solve(diag, datafile="input.txt"):
    ps = {}

    for a, b in (
        tuple(complex(*(int(_) for _ in (p.split(",", maxsplit=1)))) for p in _)
        for _ in (_.strip().split(" -> ", maxsplit=1) for _ in open(resolve(datafile)))
    ):
        z = b - a
        n = complex(
            int(z.real / abs(z.real)) if z.real else 0,
            int(z.imag / abs(z.imag)) if z.imag else 0,
        )
        if not diag and abs(n) > 1:
            continue

        while True:
            ps[a] = ps.setdefault(a, 0) + 1
            if a == b:
                break
            a += n

    return sum(_ > 1 for _ in ps.values())


def test():
    assert solve(False, "test.txt") == 5
    assert solve(True, "test.txt") == 12


test()
print(solve(False))
print(solve(True))
