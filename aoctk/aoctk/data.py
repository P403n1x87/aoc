from dataclasses import dataclass


@dataclass
class Range:
    lo: int
    hi: int

    def __contains__(self, other: "Range") -> bool:
        return self.lo <= other.lo and other.hi <= self.hi

    def overlaps(self, other: "Range") -> bool:
        return self.hi >= other.lo and other.hi >= self.lo


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
