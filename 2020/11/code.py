from dataclasses import dataclass


def init(source):
    ca = ["." + _[:-1] + "." for _ in open(source)]
    n = len(ca[0])
    return ["." * n] + ca + ["." * n]


@dataclass
class State:
    changed: bool = False
    occupied: int = 0


def adj(ca, i, j, s):
    if ca[i][j] == "L" and all(
        ca[i + x][j + y] != "#" for x in [-1, 0, 1] for y in [-1, 0, 1]
    ):
        s.changed = True
        s.occupied += 1
        return "#"
    if (
        ca[i][j] == "#"
        and sum(ca[i + x][j + y] == "#" for x in [-1, 0, 1] for y in [-1, 0, 1]) >= 5
    ):
        s.changed = True
        s.occupied -= 1
        return "L"

    return ca[i][j]


def size(ca):
    return len(ca), len(ca[0])


def coord(p, m):
    return p // m, p % m


def direct(ca, i, j, d):  # NOTE: Could be optimised slightly
    n, m = size(ca)
    ds = [
        (1, m - j),
        (-1, j),
        (m, n - i),
        (-m, i),
        (m + 1, min(m - j, n - i)),
        (-m - 1, min(j, i)),
        (m - 1, min(n - i, j)),
        (-m + 1, min(m - j, i)),
    ]
    p = i * m + j
    s, e = ds[d]
    return (
        [
            ca[y][x]
            for y, x in [coord(p + s * k, m) for k in range(1, e)]
            if ca[y][x] != "."
        ]
        + ["_"]
    )[0]


def ray(ca, i, j, s):
    if ca[i][j] == "L" and all(direct(ca, i, j, d) != "#" for d in range(8)):
        s.changed = True
        s.occupied += 1
        return "#"
    if ca[i][j] == "#" and sum(direct(ca, i, j, d) == "#" for d in range(8)) >= 5:
        s.changed = True
        s.occupied -= 1
        return "L"

    return ca[i][j]


def solve(source, rule):
    ca = init(source)

    n, m = len(ca), len(ca[0])
    s = State()

    while True:
        s.changed = False

        ca = (
            ["." * m]
            + [
                "." + "".join([rule(ca, i, j, s) for j in range(1, m - 1)]) + "."
                for i in range(1, n - 1)
            ]
            + ["." * m]
        )
        if not s.changed:
            break

    return s.occupied


assert 37 == solve("test.txt", adj)
print(solve("input.txt", adj))

assert 26 == solve("test.txt", ray)
print(solve("input.txt", ray))