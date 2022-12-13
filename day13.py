import sys
from more_itertools import chunked
from itertools import zip_longest
from functools import cmp_to_key
from typing import Union


IterativeList = Union[list['IterativeList'], Union[list[int], int]]


INPUT_FILE = "input/day13.txt"
TEST_FILES = ["input/day13test.txt"]
NIY = "501: NIY"

def build_list(inputs, cur_list) -> tuple[IterativeList, str]:
    if len(inputs) == 0:
        return cur_list, []

    head, *tail = inputs

    if head == ',':
        return build_list(tail, cur_list)

    elif head == ']':
        return cur_list, tail

    elif head == '[':
        sub_list, rest = build_list(tail, [])
        cur_list.append(sub_list)
        return build_list(rest, cur_list)

    else:
        while len(tail) != 0 and (peek := tail[0]) not in [",", "[", "]"]:
            head = head+peek
            tail = tail[1:]

        return build_list(tail, cur_list + [int(head)])


def list_from(str_list):
    return build_list(str_list.strip()[1:-1], [])[0]


def parse(data: list[str]) -> list[tuple[IterativeList, IterativeList]]:
    return [list_from(data[0]), list_from(data[1])]

def smaller(left, right):
    left_int = type(left) is int
    right_int = type(right) is int

    if left_int and right_int:
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None

    elif left_int:
        return smaller([left], right)

    elif right_int:
        return smaller(left, [right])

    else:
        if len(left) == len(right) == 0:
            return None

        elif len(left) ==  0:
            return True

        elif len(right) == 0:
            return False

        else:
            if (val := smaller(left[0], right[0])) is not None:
                return val
            return smaller(left[1:], right[1:])


def run(data: list[str]) -> tuple[str, str]:
    pairs = [parse(chunk) for chunk in list(chunked(data, 3))]

    correct = [smaller(packet0, packet1) for packet0, packet1 in pairs]

    part1 = sum([i for i, good in enumerate(correct, 1) if good])

    packets = sum(pairs,[[[2]], [[6]]])

    cmp= lambda l, r: -int(smaller(l,r))
    key = cmp_to_key(cmp)
    packs = list(sorted(packets, key=key))

    part2 = (packs.index([[2]]) + 1) * (packs.index([[6]]) + 1)


    return str(part1), str(part2)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        input_file = TEST_FILES[0]
    elif len(sys.argv) == 3:
        input_file = TEST_FILES[int(sys.argv[2])]
    else:
        input_file = INPUT_FILE

    with open(input_file, encoding="utf8") as lines:
        part1, part2 = run(list(lines))
        print("\nPART 1:\n")
        print(part1)
        print("\nPART 2:\n")
        print(part2)
