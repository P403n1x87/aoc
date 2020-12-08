# https://adventofcode.com/2020/day/2


POLICIES = [
    lambda l, h, c, p: l <= sum(_ == c for _ in p) <= h,
    lambda l, h, c, p: sum(p[i-1] == c for i in (l, h)) == 1
]


def parse(line):
    policy, _, password = line.partition(": ")
    rng, char = policy.split()
    l, h = (int(_) for _ in rng.split("-"))

    return l, h, char, password

print([sum(p(*parse(_)) for _ in open("input.txt")) for p in POLICIES])
