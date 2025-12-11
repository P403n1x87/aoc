import heapq
import typing as t
from collections import defaultdict, deque
from dataclasses import dataclass
from functools import cached_property
from itertools import chain, pairwise, product
from pathlib import Path

from aoctk.metric import manhattan2d as m2d

D4 = tuple(1j**i for i in range(4))
D8 = tuple(complex(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i or j)


def wrap(p: complex, w: int, h: int) -> complex:
    return complex(int(p.real) % w, int(p.imag) % h)


def pivot(matrix: t.List[t.List[t.Any]]) -> t.List[t.List[t.Any]]:
    return [list(row) for row in zip(*matrix)]


@dataclass
class Range:
    lo: int
    hi: int

    def __contains__(self, other: t.Union["Range", int]) -> bool:
        if isinstance(other, Range):
            return self.lo <= other.lo and other.hi <= self.hi
        return self.lo <= other <= self.hi

    def overlaps(self, other: "Range") -> bool:
        return self.hi >= other.lo and other.hi >= self.lo

    def __and__(self, other: "Range") -> t.Optional["Range"]:
        return (
            Range(max(self.lo, other.lo), min(self.hi, other.hi))
            if self.hi >= other.lo and other.hi >= self.lo
            else None
        )

    def __len__(self) -> int:
        return self.hi - self.lo + 1

    def __iter__(self):
        return iter(range(self.lo, self.hi + 1))

    def clip(self, lo: int, hi: int) -> None:
        """Clip the range to the given bounds."""
        self.lo = max(self.lo, lo)
        self.hi = min(self.hi, hi)

    def split(self, *xs: int) -> t.Generator["Range", None, None]:
        """Split the range at the given points.

        The points themselves are not included in the ranges.
        """
        a = self.lo
        for x in sorted(_ for _ in xs if self.lo <= _ <= self.hi):
            yield Range(a, x - 1)
            a = x + 1
        yield Range(a, self.hi)

    def __bool__(self) -> bool:
        return self.lo <= self.hi

    def shift(self, d: int) -> "Range":
        """Shift the range by the given amount."""
        return type(self)(self.lo + d, self.hi + d)

    def disjoint_union(self, other: "Range") -> t.List["Range"]:
        """List of ranges that describe the disjoint union of the given ranges."""
        o = self & other
        if o is None:
            return [self, other]
        lo = min(self.lo, other.lo)
        hi = max(self.hi, other.hi)
        parts = [o]
        if lo < o.lo:
            parts.append(Range(lo, o.lo - 1))
        if o.hi < hi:
            parts.append(Range(o.hi + 1, hi))
        return parts

    @classmethod
    def weighted_union(
        cls, ranges: t.Iterable["Range"]
    ) -> t.List[t.Tuple["Range", int]]:
        """List of ranges with weight that describe the union of the given ranges.

        The weight is the number of times the range is included in the union.
        """
        wranges = []
        for r in ranges:
            for s, w in list(wranges):
                rs = r & s
                if rs is not None:
                    wranges.append((rs, -1 * w))
            wranges.append((r, 1))
        return wranges

    @classmethod
    def parse(cls, s: str, sep="-") -> "Range":
        lo, hi = map(int, s.split(sep))
        return cls(lo, hi)


def weighted_union_size(weighted_ranges: t.Iterable[t.Tuple[Range, int]]) -> int:
    """Helper for computing the size of a weighted union of ranges."""
    return sum(len(r) * w * bool(r) for r, w in weighted_ranges)


class Unbound2DGrid(dict):
    def size(self):
        return (
            int(
                max(k.real for k in self.keys()) - min(k.real for k in self.keys()) + 1
            ),
            int(
                max(k.imag for k in self.keys()) - min(k.imag for k in self.keys()) + 1
            ),
        )

    def bounds(self):
        return (
            Range(
                int(min(k.real for k in self.keys())),
                int(max(k.real for k in self.keys())),
            ),
            Range(
                int(min(k.imag for k in self.keys())),
                int(max(k.imag for k in self.keys())),
            ),
        )

    def print(self, reverse=False):
        xr, yr = self.bounds()
        for y in range(yr.hi, yr.lo - 1, -1) if reverse else range(yr.lo, yr.hi + 1):
            for x in range(xr.lo, xr.hi + 1):
                print(self.get(x + y * 1j, " "), end="")
            print()

    def iter_bounds(self):
        """Iterate  over all points within the bounds of the grid."""
        return iter(product(*self.bounds()))

    def find(self, value):
        """Find the first point with the given value."""
        return next(k for k, v in self.items() if v == value)

    def n4(self, p):
        return (p + d for d in D4)

    def adj(self, p, value="#"):
        return [n for n in self.n4(p) if self.get(n) != value]

    def remove(self, ps: t.Iterable[complex]) -> None:
        for p in ps:
            del self[p]

    @classmethod
    def from_group(
        cls,
        group: t.Iterable[t.Iterable[str]],
        transformer: t.Callable[[str], t.Any] = lambda _: _,
        filter: t.Callable[[t.Any], bool] = lambda _: _ != ".",
    ) -> "Unbound2DGrid":
        rows = list(group)
        grid = cls(
            (
                (complex(j, i), transformer(c))
                for i, r in enumerate(rows)
                for j, c in enumerate(r)
                if filter(c)
            )
        )
        grid.bounds = (Range(0, len(rows[0]) - 1), Range(0, len(rows) - 1))
        return grid

    @classmethod
    def within(cls, p: complex, bounds: t.Tuple[Range, Range]) -> bool:
        bx, by = bounds
        return p.real in bx and p.imag in by


class Bounded2DGrid(Unbound2DGrid):
    @cached_property
    def size(self):
        return super().size()

    @cached_property
    def bounds(self):
        return super().bounds()

    def within(self, p: complex) -> bool:
        return super().within(p, self.bounds)

    def wrap(self, p: complex) -> complex:
        return wrap(p, *self.size)

    def print(self, reverse=False):
        xr, yr = self.bounds
        for y in range(yr.hi, yr.lo - 1, -1) if reverse else range(yr.lo, yr.hi + 1):
            for x in range(xr.lo, xr.hi + 1):
                print(self.get(x + y * 1j, " "), end="")
            print()

    def adj(self, p, value="#"):
        return [n for n in self.n4(p) if self.within(p) and self.get(n) != value]


class Graph:
    def __init__(self, data):
        self.data = data

    @dataclass
    class WeightedNode:
        weight: int
        node: object

        def __lt__(self, other):
            return self.weight < other.weight

        def __eq__(self, other):
            return self.__dict__ == other.__dict__

        def __hash__(self):
            return hash((self.weight, self.node))

    def adj(self, n):
        raise NotImplementedError()

    def weight(self, n, m=None):
        return 1

    def dijkstra(self, start, end):
        seen, q = set(), [self.WeightedNode(0, start)]
        heapq.heapify(q)

        while q:
            wn = heapq.heappop(q)
            if wn.node == end:
                return wn.weight
            if wn.node in seen:
                continue
            seen.add(wn.node)
            for a in self.adj(wn.node):
                heapq.heappush(
                    q, self.WeightedNode(wn.weight + self.weight(a, wn.node), a)
                )

        return float("inf")

    def shortest_paths(self, start: object, end: object) -> list[list[object]]:
        q = [self.WeightedNode(0, start)]
        heapq.heapify(q)

        prev, dist = defaultdict(set), {start: 0}

        # Run Dijkstra's algorithm and keep track of the previous nodes
        while q:
            wn = heapq.heappop(q)
            for a in self.adj(wn.node):
                if (
                    w := dist.get(wn.node, float("inf")) + self.weight(a, wn.node)
                ) <= dist.get(a, float("inf")):
                    dist[a] = w
                    prev[a].add(wn.node)
                    heapq.heappush(q, self.WeightedNode(w, a))

        # Unravel the previous nodes to get the paths with DFS
        paths, ends = [], {n for n in prev if n == end}
        q = [(e, []) for e in ends if dist[e] == min(dist[e] for e in ends)]
        while q:
            n, p = q.pop()
            np = [n, *p]
            if n == start:
                paths.append(np)
            for _ in prev[n]:
                q.append((_, np))

        return paths

    def longest(self, start, end):
        seen, q = {}, deque([self.WeightedNode(0, start)])
        while q:
            wn = q.popleft()
            if wn.weight > seen.setdefault(wn.node, wn.weight):
                seen[wn.node] = wn.weight
            for a in self.adj(wn.node):
                q.append(self.WeightedNode(wn.weight + self.weight(a, wn.node), a))

        return seen[end]

    def paths(self, start, end):
        q = [[start]]
        paths = []

        while q:
            p = q.pop()
            for a in self.adj(p[-1]):
                if a in p:
                    continue
                if a == end:
                    paths.append([*p, a])
                else:
                    q.append([*p, a])

        return paths

    def dot(self, output: Path) -> None:
        with output.open("w") as f:
            print("digraph input {", file=f)
            for n, ls in self.data.items():
                for t in ls:
                    print(f"  {n} -> {t};", file=f)
            print("}", file=f)

    def inverse(self) -> "Graph":
        g = {}

        for n in self.data:
            for a in self.adj(n):
                g.setdefault(a, set()).add(n)

        return type(self)(g)

    def reachable_from(self, n) -> set:
        r, q = {n}, [n]
        while q:
            for a in self.adj(q.pop()):
                if a in r:
                    continue
                r.add(a)
                q.append(a)
        return r

    def subgraph(self, nodes: set) -> "Graph":
        return type(self)(
            {
                k: {_ for _ in v if _ in nodes}
                for k, v in self.data.items()
                if k in nodes
            }
        )

    def brachistochrone(self, start, end, heuristic=lambda n, e: 0):
        """Return the minimum time to travel from start to end.

        The heuristic is used to speed up the search by giving an estimate of
        the distance from the current node to the end node (e.g. Manhattan).
        """
        seen, q, min_t = set(), [self.WeightedNode(0, start)], float("inf")
        heapq.heapify(q)

        while q:
            wn = heapq.heappop(q)
            if wn.node == end:
                min_t = min(min_t, wn.weight)
                continue
            if wn in seen or wn.weight + heuristic(wn.node, end) >= min_t:
                continue
            seen.add(wn)
            for _ in self.adj(wn.weight, wn.node):
                heapq.heappush(q, self.WeightedNode(wn.weight + 1, _))

        return min_t


class Vector:
    def __init__(self, *args):
        self._c = args

    def __abs__(self):
        return sum(_**2 for _ in self._c) ** 0.5

    def __add__(self, other):
        return Vector(*(a + b for a, b in zip(self._c, other._c)))

    def __radd__(self, other):
        if other != 0:
            raise ValueError("Vector can only be added another vector or 0")
        return self

    def __sub__(self, other):
        return Vector(*(a - b for a, b in zip(self._c, other._c)))

    def __eq__(self, other: object) -> bool:
        return self._c == other._c

    def within(self, bounds):
        return all(c in r for c, r in zip(self._c, bounds))

    @classmethod
    def e(cls, i, n):
        return cls(*(_ == i for _ in range(n)))

    def __mul__(self, other):
        return Vector(*(a * other for a in self._c))

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if not other:
            raise ZeroDivisionError()
        return Vector(*(a / other for a in self._c))

    def __getitem__(self, i):
        return self._c[i]

    def __hash__(self) -> int:
        return hash(self._c)

    def __repr__(self) -> str:
        return f"Vector{self._c}"

    def __len__(self) -> int:
        return len(self._c)

    def __matmul__(self, other) -> float:
        return sum(a * b for a, b in zip(self._c, other._c))

    def round(self, n: int = 0) -> "Vector":
        return Vector(*(round(_, n) for _ in self._c))

    def x(self, other):
        """Cross product of two vectors. Only defined for 3D vectors."""
        assert len(self) == len(other) == 3
        return Vector(
            self[1] * other[2] - self[2] * other[1],
            self[2] * other[0] - self[0] * other[2],
            self[0] * other[1] - self[1] * other[0],
        )


class bij(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(set(self.keys())) != len(set(self.values())):
            raise ValueError("Not a bijection")
        self.inv = {v: k for k, v in self.items()}

    @property
    def range(self):
        return self.values()

    @property
    def domain(self):
        return self.keys()


M4 = bij({">": 1, "<": -1, "v": 1j, "^": -1j})


class Path2D(list):
    def __reversed__(self):
        return type(self)(self[::-1])

    def area(self):
        """Implement the shoelace formula. The sign gives the orientation."""
        return (
            int(
                sum(
                    (a.conjugate() * b).imag
                    for a, b in pairwise(chain(self, [self[0]]))
                )
            )
            / 2
        )

    def orientation(self) -> int:
        """Return the orientation of the path."""
        return 2 * (self.area() > 0) - 1

    def pick(self):
        """Use Pick's Theorem to compute the number of points inside the path."""
        return int(abs(self.area()) + 1 - (len(self) / 2))

    def interior(self):
        """Get all the points in the interior of the path."""
        # Get all the inside points close to the path considering the orientation
        o, spath, inside = self.orientation(), set(self), set()
        for p, q in pairwise(chain(self, [self[0]])):
            n = (q - p) * 1j * o
            inside |= {p + n, q + n} - spath

        # Get all the inside points connected to the already found ones
        q = deque(inside)
        while q and (p := q.popleft()):
            for d in D4:
                if (np := p + d) not in inside and np not in spath:
                    inside.add(np)
                    q.append(np)

        return inside

    def contour(self) -> set:
        """Get all the points in the immediate outside of the path."""
        # Get all the outside points close to the path considering the
        # orientation
        o, spath, outside = self.orientation(), set(self), set()
        for p, q in pairwise(chain(self, [self[0]])):
            n = (p - q) * 1j * o
            outside |= {p + n, q + n} - spath

        return outside

    def __len__(self):
        return sum(m2d(p, q) for p, q in pairwise(chain(self, [self[0]])))

    @classmethod
    def from_vertices(cls, vertices: t.Iterable[complex]) -> "Path2D":
        vs = [(v - u) for u, v in pairwise((*vertices, vertices[0]))]
        path = [p := vertices[0]]
        for v in vs:
            try:
                u = v / (m := abs(v))
            except ZeroDivisionError:
                continue
            for _ in range(int(m)):
                p += u
                path.append(p)
        path.pop()

        return cls(path)
