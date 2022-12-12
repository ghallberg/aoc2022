import sys
from typing import NamedTuple
from queue import PriorityQueue


INPUT_FILE = "input/day12.txt"
TEST_FILES = ["input/day12test.txt"]
NIY = "401: NIY"


class Pos(NamedTuple):
    x: int
    y: int


class PrioItem(NamedTuple):
    prio: int
    pos: Pos


def parse(map: list[str]) -> tuple[Pos, Pos, list[list[int]]]:
    start_pos = Pos(0, 0)
    end_pos = Pos(0, 0)
    new_map: list[list[int]] = []
    for x, line in enumerate(map):
        new_map.append([])
        for y, char in enumerate(line.strip()):
            if char == "S":
                start_pos = Pos(x, y)
                height = ord("a")
            elif char == "E":
                end_pos = Pos(x, y)
                height = ord("z")
            else:
                height = ord(char)

            new_map[x].append(height)
    return start_pos, end_pos, new_map


def neighbours(pos: Pos) -> list[Pos]:
    x, y = pos
    return [Pos(x+1, y), Pos(x-1, y), Pos(x, y+1), Pos(x, y-1)]


def on_map(pos, map):
    return 0 <= pos.x < len(map) and 0 <= pos.y < len(map[pos.x])


def climbable(pos, map, target):
    cur_height = map[pos.x][pos.y]
    target_height = map[target.x][target.y]
    return target_height <= cur_height + 1


def reachable(pos: Pos, map: list[list[int]], target: Pos) -> bool:
    return on_map(target, map) and climbable(pos, map, target)


def run(data: list[str]) -> tuple[str, str]:
    start_pos, end_pos, map = parse(data)
    seen: list[Pos] = []
    queue: PriorityQueue[PrioItem] = PriorityQueue()

    cur_pos: Pos = start_pos
    dist: int = 0

    while cur_pos != end_pos:
        for item in neighbours(cur_pos):
            if (item not in seen) and (reachable(cur_pos, map, item)):
                queue.put(PrioItem(dist+1, item))

        seen.append(cur_pos)
        print(seen)
        dist, cur_pos = queue.get()

    part1 = dist
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
