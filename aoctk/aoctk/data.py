import heapq
import typing as t
from dataclasses import dataclass


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


class Graph:
    def __init__(self, data):
        self.data = data

    @dataclass
    class WeightedNode:
        weight: int
        node: object

        def __lt__(self, other):
            return self.weight < other.weight

    def adj(self, n):
        raise NotImplementedError()

    def weight(self, n):
        raise NotImplementedError()

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
            for t in self.adj(wn.node):
                heapq.heappush(q, self.WeightedNode(wn.weight + 1, t))

        return float("inf")


class Vector:
    def __init__(self, *args):
        self._c = args

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
