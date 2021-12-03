# https://adventofcode.com/2021/day/3

import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


def solve1(datafile="input.txt"):
    data = [_.strip() for _ in open(resolve(datafile))]
    N = len(data)
    B = len(data[0])
    d = e = 0
    for _ in [sum(data[i][j] == "1" for i in range(N)) > (N >> 1) for j in range(B)]:
        d = (d << 1) + _
        e = (e << 1) + (not _)

    return d * e


def solve2(datafile="input.txt"):
    data = [_.strip() for _ in open(resolve(datafile))]
    B = len(data[0])

    def decode(op):
        current = data

        for j in range(B):
            d = str(int(op(sum(_[j] == "0" for _ in current), (len(current) >> 1))))
            current = [_ for _ in current if _[j] == d]
            if len(current) == 1:
                break

        return int("".join([str(int(_)) for _ in current[0]]), 2)

    return decode(lambda a, b: a <= b) * decode(lambda a, b: a > b)


def test():
    assert solve1("test.txt") == 198
    assert solve2("test.txt") == 230


test()
print(solve1())
print(solve2())
