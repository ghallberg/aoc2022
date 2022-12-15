import sys
import re
from typing import NamedTuple, Union

DAY_NO = "15"

INPUT_FILE = f"input/day{DAY_NO}.txt"
TEST_FILES = [f"input/day{DAY_NO}test.txt"]
NIY = "501: NIY"


class Pos(NamedTuple):
    x: int
    y: int


class Sensor(NamedTuple):
    pos: Pos
    beacon: Pos
    range: int


def taxi_dist(start: Pos, end: Pos) -> int:
    x_dist = abs(start.x-end.x)
    y_dist = abs(start.y-end.y)

    return x_dist + y_dist


def row_reach(row_no: int, s: Sensor) -> Union[tuple[int, int], None]:
    y_dist = abs(s.pos.y - row_no)
    x_reach = s.range - y_dist
    if x_reach < 0:
        return None
    return (s.pos.x - x_reach), (s.pos.x + x_reach)


def parse_sensor(data: str) -> Sensor:
    pattern = "^.*x=(-?\\d*), y=(-?\\d*):.*x=(-?\\d*), y=(-?\\d*)$"
    s_x, s_y, b_x, b_y = [int(v) for v in re.match(pattern, data).group(1, 2, 3, 4)]
    s = Pos(s_x, s_y)
    b = Pos(b_x, b_y)
    return Sensor(s, b, taxi_dist(s, b))


def parse(data: list[str]):
    sensors: list[Sensor] = [parse_sensor(line) for line in data]

    min_x = min([min(s.x, b.x) for s, b, _ in sensors])
    max_x = max([max(s.x, b.x) for s, b, _ in sensors])

    min_y = min([min(s.y, b.y) for s, b, _ in sensors])
    max_y = max([max(s.y, b.y) for s, b, _ in sensors])

    return sensors, Pos(min_x, min_y), Pos(max_x, max_y)


def int_in(num, range):
    return range[0] <= num <= range[1]


def merge_ranges(left: tuple[int, int], right: tuple[int, int]
                 ) -> list[tuple[int, int]]:
    start_in = int_in(right[0], left)

    if start_in:
        if int_in(right[1], left):
            return [left]
        else:
            return [(left[0], right[1])]

    return [left, right]


def range_len(range):
    return abs(range[0]-range[1]) + 1


def merge_range_list(ranges: list[tuple[int,int]]):
    if len(ranges) == 1:
        return ranges

    first, second, *rest = ranges
    new_start = merge_ranges(first, second)
    if len(new_start) == 1:
        return merge_range_list(new_start + rest)

    rest = merge_range_list([new_start[1]] + rest)
    return [new_start[0]] + rest


def run(data: list[str]) -> tuple[str, str]:
    sensors, min_pos, max_pos = parse(data)

    row = 2000000

    ranges = [range for range in [row_reach(row, s) for s in sensors] if range is not None]
    ranges = sorted(ranges, key=lambda r: r[0])
    print(ranges)

    merged = merge_range_list(ranges)
    print(merged)

    beacons = set([s.beacon for s in sensors if s.beacon.y == row])
    print(beacons)
    beacon_count = len(beacons)

    print(beacon_count)


    part1 = sum([range_len(r) for r in merged]) - beacon_count
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
