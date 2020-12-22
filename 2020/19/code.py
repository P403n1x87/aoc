# https://adventofcode.com/2020/day/19

from collections import deque


def read(source):
    rules = {}
    with open(source) as fin:
        while True:
            l = next(fin)[:-1]
            if not l:
                break
            n, _, children = l.partition(": ")
            rules[n] = (
                children[1:-1]
                if children[0] == '"'
                else [tuple(_.split()) for _ in children.split(" | ")]
            )
        return rules, [_[:-1] for _ in fin]


def match(rules, s, root="0"):
    r = rules[root]

    if isinstance(r, str):
        res = len(s) >= 1 and r == s[0]
        if res:
            yield s[1:]
        return

    def composite(rule, s):
        tails = deque([s])
        for c in rule:
            next_tails = deque()
            while tails:
                tail = tails.popleft()
                for tail in match(rules, tail, c):
                    next_tails.append(tail)
            tails = next_tails
        yield from iter(tails)

    for c in r:
        yield from composite(c, s)


def validate(rules, s):
    return "" in list(match(rules, s))


def solve(source):
    rules, strings = read(source)

    n = sum(validate(rules, s) for s in strings)

    # patch
    rules["8"] = [("42",), ("42", "8")]
    rules["11"] = [("42", "31"), ("42", "11", "31")]

    m = sum(validate(rules, s) for s in strings)

    return n, m


assert 2, 2 == solve("2020/19/test.txt")
print(solve("2020/19/input.txt"))
