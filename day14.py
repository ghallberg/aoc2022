import sys
from itertools import pairwise
from typing import NamedTuple
from math import inf

DAY_NO = "14"

INPUT_FILE = f"input/day{DAY_NO}.txt"
TEST_FILES = [f"input/day{DAY_NO}test.txt"]
NIY = "501: NIY"

class Pos(NamedTuple):
    x: int
    y: int

def parse(paths: list[str]):
    max_x = 0
    max_y = 0

    min_x = inf
    min_y = inf

    blocked = set()

    for path in paths:
        str_paths = [coord.strip().split(',') for coord in path.split(" -> ")]
        paths: list[Pos] = [Pos(int(x), int(y)) for x,y in str_paths]


        for start, end in pairwise(paths):
            if start.x == end.x:
                low_y, high_y = sorted((start.y, end.y))
                blocked.update([Pos(start.x, y) for y in range(low_y, high_y+1)])
                if high_y > max_y:
                    max_y = high_y
                if low_y < min_y:
                   min_y = low_y

            elif start.y == end.y:
                low_x, high_x = sorted((start.x, end.x))
                blocked.update([Pos(x, start.y) for x in range(low_x, high_x+1)])
                if high_x > max_x:
                    max_x = high_x
                if low_x < min_x:
                   min_x = low_x

            else:
                raise ValueError("Path isn't a horizontal or vertical", start, end)


    return blocked, Pos(min_x, min_y), Pos(max_x, max_y)

def draw_map(blocked, sand, path, sand_spout, min_pos, max_pos):
    for y in range(0, max_pos.y+1):
        #line = f"{str(y)} "
        line = ""
        for x in range(min_pos.x, max_pos.x+1):
            if Pos(x,y) in blocked:
                line += "#"
            elif Pos(x,y) in sand:
                line += "o"
            elif Pos(x,y) in path:
                line += "~"
            elif Pos(x,y) == sand_spout:
                line += "+"
            else:
                line +="."

        print(line)

def next_pos(cur_pos, blocked):
    cur_x,cur_y = cur_pos

    next_y = cur_y + 1

    pos_pos = [Pos(cur_x, next_y), Pos(cur_x - 1, next_y), Pos(cur_x + 1, next_y), cur_pos]

    return next(x for x in pos_pos if x not in blocked)


def pour_sand(rock, sand_spout, abyss):
    sand = set()

    cur_pos = sand_spout
    path = []

    while True:
        new_pos = next_pos(cur_pos, sand.union(rock))
        path.append(new_pos)
        if new_pos == cur_pos:
            sand.add(cur_pos)
            cur_pos = sand_spout
            path = []
        elif new_pos.x >= abyss.x or new_pos.y >= abyss.y:
            return sand, path
        else:
            cur_pos = new_pos




def run(data: list[str]) -> tuple[str, str]:
    rock, min_pos, max_pos = parse(data)

    sand_spout = Pos(500,0)

    sand, path = pour_sand(rock, sand_spout, max_pos)

    draw_map(rock, sand, path, sand_spout, min_pos, max_pos)


    part1 = len(sand)

    part2 = NIY


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
