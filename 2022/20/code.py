# https://adventofcode.com/2022/day/20

from dataclasses import dataclass

from aoctk.input import get_lines


@dataclass
class Link:
    value: int
    next: "Link"
    prev: "Link" = None
    moved: bool = False

    def reset(self):
        n = self.next
        last = n.prev
        while True:
            n.moved = False
            if n is last:
                break
            n = n.next
        self.prev.moved = True

    def at(self, n):
        s = self.prev
        for _ in range(n % self.value):
            s = s.next
        return s.value


def get_list(data, k=1):
    h = Link(0, None)
    n, c, z = h, 0, None
    for v in map(int, get_lines(data)):
        n.next = Link(v * k, None, n)
        if v == 0:
            z = n.next
            z.moved = True
        n = n.next
        c += 1
    n.next = h.next
    h.next.prev = n
    h.value = c
    h.prev = z

    return h


def solve(n=1, k=1, data="input.txt"):
    h = get_list(data, k)
    c, z, order = h.value, h.prev, []
    for it in range(n):
        iorder = iter(order)
        last = order[-1] if order else h.next.prev
        curr = next(iorder) if order else h.next
        while True:
            if it == 0:
                nx = curr.next
                while nx.moved:
                    nx = nx.next
            else:
                try:
                    nx = next(iorder)
                except StopIteration:
                    nx = None

            m = curr
            for _ in range(curr.value % (c - 1)):
                m = m.next

            curr.prev.next = curr.next
            curr.next.prev = curr.prev
            curr.next = m.next
            curr.prev = m
            m.next = curr
            curr.next.prev = curr

            curr.moved = True

            if it == 0:
                order.append(curr)

            if curr is last:
                break

            curr = nx

        h.reset()

    return sum(h.at(1000 * n) for n in range(1, 4))


def part_one(data="input.txt"):
    return solve(1, 1, data)


def part_two(data="input.txt"):
    return solve(10, 811589153, data)


def test():
    assert part_one("test.txt") == 3
    assert part_two("test.txt") == 1623178306
