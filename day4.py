import sys
from collections.abc import Sequence
from functools import reduce

def parse(str_input: str):
    range_pair = str_input.split(',')
    range_pair = [sr.split('-') for sr in str_input.split(',')]
    return [(int(x), int(y)) for x, y in range_pair]

def r_size(r):
    return r[1]-r[0]

def either_contains(ranges):
    bigger, smaller = sorted(ranges, key=r_size, reverse=True)
    return bigger[0] <= smaller[0] and bigger[1] >= smaller[1]

def overlap(ranges):
    r1,r2 = ranges
    r1_range = range(r1[0], r1[1]+1)
    r2_range = range(r2[0], r2[1]+1)
    return any([end in r2_range for end in r1]) or any([end in r1_range for end in r2])


def run(str_inputs: Sequence[str]):
    range_pairs = list(map(parse, str_inputs))
    print(len(list(filter(either_contains, range_pairs))))
    print(len(list(filter(overlap, range_pairs))))



if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            lines= [
                    "2-4,6-8",
                    "2-3,4-5",
                    "5-7,7-9",
                    "2-8,3-7",
                    "6-6,4-6",
                    "2-6,4-8",
                    ]
            run(lines)

    else:
        with open("input/day4.txt", encoding="utf8") as lines:
            run(lines)
