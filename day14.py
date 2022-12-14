import sys
from itertools import pairwise
from typing import NamedTuple
from math import inf

DAY_NO = "14"

INPUT_FILE = f"input/day{DAY_NO}.txt"
TEST_FILES = [f"input/day{DAY_NO}test.txt", "input/tigge14.txt"]
NIY = "501: NIY"

class Pos(NamedTuple):
    x: int
    y: int

def parse(paths: list[str]):
    blocked = set()

    for path in paths:
        str_paths = [coord.strip().split(',') for coord in path.split(" -> ")]
        paths: list[Pos] = [Pos(int(x), int(y)) for x,y in str_paths]


        for start, end in pairwise(paths):
            if start.x == end.x:

                low_y, high_y = sorted((start.y, end.y))

                blocked.update([Pos(start.x, y) for y in range(low_y, high_y+1)])


            elif start.y == end.y:
                low_x, high_x = sorted((start.x, end.x))
                blocked.update([Pos(x, start.y) for x in range(low_x, high_x+1)])

            else:
                raise ValueError("Path isn't a horizontal or vertical", start, end)


    return blocked

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

def blocked(pos, stuff, floor):
    return pos in stuff or pos.y >= floor


def next_pos(cur_pos, stuff, floor = inf):
    cur_x, cur_y = cur_pos

    next_y = cur_y + 1

    candidates = [Pos(cur_x, next_y), Pos(cur_x - 1, next_y), Pos(cur_x + 1, next_y), cur_pos]

    return next(pos for pos in candidates if not blocked(pos, stuff, floor))


def pour_sand(rock, sand_spout, end, abyss = True):
    sand = set()
    path = []
    cur_pos = sand_spout

    if abyss:
        floor = inf
    else:
        floor = end +2

    while True:
        stuff = sand.union(rock)
        new_pos = next_pos(cur_pos, stuff, floor)
        if new_pos == cur_pos:
            # LANDED
            sand.add(cur_pos)

            if cur_pos == sand_spout:
                # BLOCKED
                return sand, []

            cur_pos = path.pop()

        elif abyss and new_pos.y >= end:
            return sand, path

        else:
            path.append(cur_pos)
            cur_pos = new_pos



def run(data: list[str]) -> tuple[str, str]:
    rock = parse(data)

    sand_spout = Pos(500,0)

    max_y = max([pos.y for pos in rock])
    min_y = min([pos.y for pos in rock])
    max_x = max([pos.x for pos in rock])
    min_x = min([pos.x for pos in rock])

    sand, path = pour_sand(rock, sand_spout, max_y)

    draw_map(rock, sand, path, sand_spout, Pos(min_x, min_y), Pos(max_x, max_y))

    part1 = len(sand)

    sand, path = pour_sand(rock, sand_spout, max_y, abyss = False)

    max_y = max([pos.y for pos in rock.union(sand)])
    min_y = min([pos.y for pos in rock.union(sand)])
    max_x = max([pos.x for pos in rock.union(sand)])
    min_x = min([pos.x for pos in rock.union(sand)])

    draw_map(rock, sand, path, sand_spout, Pos(min_x, min_y), Pos(max_x, max_y))

    part2 = len(sand)

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
