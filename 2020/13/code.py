# https://adventofcode.com/2020/day/13


def read(source):
    dep, _ = open(source).read().split("\n", maxsplit=1)
    buses = [int(b) if b != "x" else 0 for b in _.split(",")]
    return int(dep), buses


def solve(source):
    dep, buses = read(source)
    w, b = min(((b - (dep % b), b) for b in buses if b), key=lambda x: x[0])

    s, m = 0, 1

    # This only works if bus times are pair-wise coprime
    for a, n in sorted(
        (((b - d) % b, b) for d, b in enumerate(buses) if b),
        key=lambda x: x[1],
        reverse=True,
    ):
        while s % n != a:
            s += m
        m *= n

    return w * b, s


assert 295, 1068781 == solve("test.txt")
print(solve("input.txt"))
