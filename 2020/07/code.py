from collections import deque
from functools import cache
from typing import Tuple


class Rules:
    def __init__(self, source):
        self.fgraph = {}  # Forward graph
        self.bgraph = {}  # Backward graph
        for _ in open(source):
            self.add_rule(_[:-1])

    def add_rule(self, rule: str) -> None:
        def parse(edge: str) -> Tuple[str, int]:
            count, _, bag = edge.partition(" ")
            bag, _, _ = bag.rpartition(" ")
            return bag, int(count)

        bag, _, edges = rule[:-1].partition(" bags contain ")
        if edges != "no other bags":
            for e in edges.split(", "):
                k, v = parse(e)
                self.bgraph.setdefault(k, {})[bag] = self.fgraph.setdefault(bag, {})[
                    k
                ] = v
        else:
            self.fgraph[bag] = {}

    def find_containers_for(self, bag: str) -> set:  # BFS
        visited = set()
        q = deque({bag})
        container = set()
        while q:
            if (c := q.popleft()) in visited:
                continue
            p = self.bgraph.get(c, {})
            container |= set(p)
            for _ in p:
                q.append(_)
            visited.add(c)
        return container

    @cache
    def weight(self, bag: str) -> int:  # Works only for DAGs
        return sum(w * (1 + self.weight(_)) for _, w in self.fgraph[bag].items())


assert Rules("test.txt").find_containers_for("shiny gold") == {
    "bright white",
    "muted yellow",
    "dark orange",
    "light red",
}
print(len(Rules("input.txt").find_containers_for("shiny gold")))


assert 126 == Rules("test2.txt").weight("shiny gold")
print(Rules("input.txt").weight("shiny gold"))