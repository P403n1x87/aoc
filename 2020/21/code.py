# https://adventofcode.com/2020/day/21

from collections import defaultdict, Counter
from functools import reduce


def read(source):
    for _ in open(source):
        ingredients, _, allergens = _[:-2].partition(" (contains ")
        yield set(ingredients.split()), set(allergens.split(", "))


def solve(source):
    als = defaultdict(list)
    all_ingredients = set()
    cins = Counter()
    for ingredients, allergens in read(source):
        cins.update(ingredients)
        all_ingredients |= ingredients
        for a in allergens:
            als[a].append(ingredients)

    pals = {k: reduce(set.__and__, v) for k, v in als.items()}
    nals = all_ingredients - reduce(set.__or__, pals.values())

    n = sum(cins[i] for i in nals)

    upals = {k: v - nals for k, v in pals.items()}

    atoi = {}
    while upals:
        s = None
        for k, v in upals.items():
            if len(v) == 1:
                s = (k, next(iter(v)))
                break
        a, i = s
        atoi[a] = i
        del upals[a]
        for v in upals.values():
            if i in v:
                v.remove(i)

    return n, ",".join(i for _, i in sorted(atoi.items()))


assert 5, "mxmxvkd,sqjhc,fvjkl" == solve("2020/21/test.txt")
print(solve("2020/21/input.txt"))