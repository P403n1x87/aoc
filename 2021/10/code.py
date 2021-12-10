# https://adventofcode.com/2021/day/10

import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


def solve(datafile="input.txt"):
    DELIMS = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
        "(": -3,
        "[": -57,
        "{": -1197,
        "<": -25137,
    }
    RDELIMS = {-3: 1, -57: 2, -1197: 3, -25137: 4}

    def score(line):
        stack = []
        for _ in line:
            d = DELIMS[_]
            if d < 0:
                stack.insert(0, d)
            else:
                if d + stack.pop(0):
                    return complex(0, d)

        return complex(int("".join([str(RDELIMS[v]) for v in stack]), 5), 0)

    ls = [_ for _ in (score(_.strip()) for _ in open(resolve(datafile))) if _]
    ss = sorted([_.real for _ in ls if _.real])

    return (int(sum(_.imag for _ in ls)), int(ss[len(ss) >> 1]))


def test():
    assert solve("test.txt") == (26397, 288957)


test()
print(solve())
