# https://adventofcode.com/2024/day/9

from aoctk.input import get_lines


def S(a, b):
    return ((b - 1) * b - (a - 1) * a) >> 1


def part_one(data="input.txt"):
    (data,) = get_lines(data)
    files = list(int(_) for _ in data[::2])
    spaces = list(int(_) for _ in data[1::2])
    p = s = i = 0
    while files and spaces:
        f = files.pop(0)
        s += S(p, p + f) * i
        p += f
        i += 1
        b = spaces.pop(0)
        while b and files:
            if files[-1] == 0:
                files.pop()
                continue
            j = i + len(files) - 1
            s += p * j
            p += 1
            b -= 1
            files[-1] -= 1
    return s


def part_two(data="input.txt"):
    (d,) = get_lines(data)
    data = [int(_) for _ in d]
    spaces = []
    f = data[0]
    files = [(0, 0, f)]
    i = 1
    p = f
    for b, f in zip(data[1::2], data[2::2]):
        spaces.append((p, b))
        p += b
        files.append((p, i, f))
        p += f
        i += 1

    s = 0
    while spaces and files:
        fd = files.pop()
        for j, (p, b) in enumerate(spaces):
            q, i, f = fd
            if p > q:
                p = q
                break
            if b >= fd[-1]:
                if b == f:
                    spaces.pop(j)
                else:
                    spaces[j] = (p + f, b - f)
                break
        s += S(p, p + f) * i
    return s + sum(S(p, p + f) * i for p, i, f in files)


def test():
    assert (_ := part_one("test.txt")) == 1928, _
    assert (_ := part_two("test.txt")) == 2858, _
