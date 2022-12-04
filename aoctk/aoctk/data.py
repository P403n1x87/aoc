from dataclasses import dataclass


@dataclass
class Range:
    lo: int
    hi: int

    def __contains__(self, other: "Range") -> bool:
        return self.lo <= other.lo and other.hi <= self.hi

    def overlaps(self, other: "Range") -> bool:
        return self.hi >= other.lo and other.hi >= self.lo
