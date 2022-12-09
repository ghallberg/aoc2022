import sys
from dataclasses import dataclass
from itertools import pairwise

INPUT_FILE = "input/day9.txt"
TEST_FILES = [ "input/day9test.txt", "input/day9test2.txt"]

def follow(leader, follower):
    x_diff = leader[0] - follower[0]
    y_diff = leader[1] - follower[1]
    x_pos, y_pos = follower

    if x_diff == 2:
        x_pos += 1
        if y_diff < 0:
            y_pos -= 1
        if y_diff > 0:
            y_pos += 1

    elif x_diff == -2:
        x_pos -= 1
        if y_diff < 0:
            y_pos -= 1
        if y_diff > 0:
            y_pos += 1

    elif y_diff == 2:
        y_pos += 1
        if x_diff < 0:
            x_pos -= 1
        if x_diff > 0:
            x_pos += 1

    elif y_diff == -2:
        y_pos -= 1
        if x_diff < 0:
            x_pos -= 1
        if x_diff > 0:
            x_pos += 1

    return x_pos, y_pos

def do_move(knots: list[tuple[int,int]], direction: str) -> list[tuple[int,int]]:
    if direction == "L":
        knots[0] = (knots[0][0] - 1, knots[0][1])
    elif direction == "R":
        knots[0] = (knots[0][0] + 1, knots[0][1])
    elif direction == "U":
        knots[0] = (knots[0][0], knots[0][1] + 1)
    elif direction == "D":
        knots[0] = (knots[0][0], knots[0][1] - 1)

    return knots[0:1] + [follow(leader, follower) for leader, follower in pairwise(knots)]

def run(data: list[str]):
    moves = "".join([direction*int(steps) for direction, steps in [move.split() for move in data]])

    knots = [(0,0)]*2

    t_pos_set = set()

    for move in moves:
        knots = do_move(knots, move)
        t_pos_set.add(knots[-1])

    tail_spaces = len(t_pos_set)

    print("PART 1:", tail_spaces)

    knots = [(0,0)]*10
    t_pos_set = set()

    for move in moves:
        knots = do_move(knots, move)
        t_pos_set.add(knots[-1])

    tail_spaces = len(t_pos_set)

    print("PART 2:", tail_spaces)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        input_file = TEST_FILES[0]
    elif len(sys.argv) == 3:
        input_file = TEST_FILES[int(sys.argv[2])]
    else:
        input_file = INPUT_FILE

    with open(input_file, encoding="utf8") as lines:
        run(list(lines))
