import sys
from collections.abc import Sequence
from functools import reduce
from more_itertools import ichunked

def to_prio(char: str):
    ord_val = ord(char)
    if ord_val < 97:
        return ord_val-38
    else:
        return ord_val-96

def find_overlap(comps: Sequence[Sequence[str]]):
    sets = [set(comp) for comp in comps]
    return reduce(set.intersection, sets[1:], sets[0]).pop()

def get_groups(bags: Sequence[str]):
    group_start = 0
    while True:
        group_end = group_start+3
        group = bags[group_start:group_start+3]

        if len(group) != 3:
            return

        group_start = group_end
        yield group


def run(bags: Sequence[str]):
    bags = list(bags)
    bags = [bag.strip() for bag in bags]

    comps = [(bag[0:int(len(bag)/2)], bag[int((len(bag)/2)):]) for bag in bags]

    doubles = [find_overlap(pair) for pair in comps]

    prios = [to_prio(double) for double in doubles]

    print(sum(prios))

    groups = ichunked(bags,3)

    badges = [find_overlap(group) for group in groups]

    badge_prios = [to_prio(badge) for badge in badges]

    print(sum(badge_prios))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            rucksacks = ["vJrwpWtwJgWrhcsFMMfFFhFp",
                         "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
                         "PmmdzqPrVvPwwTWBwg",
                         "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
                         "ttgJtRGJQctTZtZT",
                         "CrZsJsPPZsGzwwsLwLmpwMDw"]
            run(rucksacks)

    else:
        with open("input/day3.txt", encoding="utf8") as rucksacks:
            run(rucksacks)
