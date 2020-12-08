# https://adventofcode.com/2020/day/4


from typing import Generator, Optional


FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
FIELD_RULES = {
    "byr": lambda v: len(v) == 4 and 1920 <= int(v) <= 2002,
    "iyr": lambda v: len(v) == 4 and 2010 <= int(v) <= 2020,
    "eyr": lambda v: len(v) == 4 and 2020 <= int(v) <= 2030,
    "hgt": lambda v: 150 <= int(v[:-2]) <= 193
    if v.endswith("cm")
    else (59 <= int(v[:-2]) <= 76 if v.endswith("in") else False),
    "hcl": lambda v: v[0] == "#"
    and len(v) == 7
    and set(v[1:]) <= set("0123456789abcdef"),
    "ecl": lambda v: v in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
    "pid": lambda v: len(v) == 9 and all(_.isdigit() for _ in v),
    "cid": lambda v: True,
}


def passports(source: str) -> Generator[dict, None, None]:
    fields = {}
    for line in open(source):
        if line == "\n":
            yield fields
            fields = {}
        fields.update(dict(d.split(":", maxsplit=1) for d in line.split()))
    if fields:
        yield fields


def validate(p: dict, rules: Optional[dict] = None) -> bool:
    if set(p) >= FIELDS:
        if rules:
            for f, v in p.items():
                if not rules[f](v):
                    return False
        return True

    return False


assert 2 == sum(validate(p, FIELD_RULES) for p in passports("test.txt"))

assert 4 == sum(validate(p, FIELD_RULES) for p in passports("valid.txt"))
assert 0 == sum(validate(p, FIELD_RULES) for p in passports("invalid.txt"))

print(sum(validate(p) for p in passports("input.txt")))
print(sum(validate(p, FIELD_RULES) for p in passports("input.txt")))