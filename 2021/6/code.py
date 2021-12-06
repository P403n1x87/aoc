# https://adventofcode.com/2021/day/6

import os


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


def solve_dp(days, datafile="input.txt"):
    dp = {}
    for d in range(7, days + 7):
        dp[d] = 1 + sum(
            dp.get(_, 1) for _ in (d - (7 * k + 9) for k in range(int((d - 7) / 7) + 1))
        )

    return sum(
        dp[days + (6 - int(_))]
        for _ in open(resolve(datafile)).read().strip().split(",")
    )


def solve(days, datafile="input.txt"):
    state = [0] * 9

    for _ in open(resolve(datafile)).read().strip().split(","):
        state[int(_)] += 1

    for _ in range(days):
        state[(_ + 7) % 9] += state[_ % 9]

    return sum(state)


def test():
    assert solve_dp(80, "test.txt") == 5934
    assert solve_dp(256, "test.txt") == 26984457539

    assert solve(80, "test.txt") == 5934
    assert solve(256, "test.txt") == 26984457539


test()
print(solve(80))
print(solve(256))
