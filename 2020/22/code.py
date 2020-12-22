# https://adventofcode.com/2020/day/22

from collections import deque


def read(source):
    def cards():
        while True:
            try:
                l = next(fin)
            except StopIteration:
                break
            if l == "\n":
                break
            yield int(l)

    with open(source) as fin:
        assert next(fin).startswith("Player 1:")
        p1 = list(cards())
        assert next(fin).startswith("Player 2:")
        p2 = list(cards())

        return p1, p2


def solve(source):
    def gid(p):
        return sum(c * (i + 1) for i, c in enumerate(p[::-1]))

    p1, p2 = read(source)

    while p1 and p2:
        c1, c2 = p1.pop(0), p2.pop(0)
        if c1 > c2:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)

    n = gid(p1 or p2)

    def rcombat(p1, p2, subgame):
        (game,) = subgame
        subgame[0] += 1
        # print(f"=== Game {game} ===\n")

        rounds = set()
        while p1 and p2:
            config = (tuple(p1), tuple(p2))
            if config in rounds:
                return True
            rounds.add(config)
            # print(f"-- Round {len(rounds)} (Game {game}) --")
            # print(p1)
            # print(p2)
            c1, c2 = p1.pop(0), p2.pop(0)
            # print(c1)
            # print(c2)
            if c1 <= len(p1) and c2 <= len(p2):
                # print("Playing sub-game...\n")
                winner = rcombat(p1[:c1], p2[:c2], subgame)
                # print(f"Back to game {game}")
            else:
                winner = c1 > c2
            if winner:
                # print(f"P1 wins round {len(rounds)} of game {game}\n")
                p1.append(c1)
                p1.append(c2)
            else:
                # print(f"P2 wins round {len(rounds)} of game {game}\n")
                p2.append(c2)
                p2.append(c1)
        # print(f"{winner and 'P1' or 'P2'} wins game {game}")
        return bool(p1)

    p1, p2 = read(source)
    rcombat(p1, p2, [1])

    return n, gid(p1 or p2)


assert (306, 291) == solve("2020/22/test.txt")
print(solve("2020/22/input.txt"))