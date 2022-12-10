import sys
from more_itertools import ichunked

INPUT_FILE = "input/day10.txt"
TEST_FILES = [ "input/day10test.txt", "input/day10test2.txt"]

operation_CYCLES = {"noop": 1,
                    "addx": 2}

def parse(line):
    command = line.strip().split()

    operation = command[0]
    if operation == "noop":
        return [0]
    elif operation == "addx":
        return [0,int(command[1])]

def should_draw_pos(cycle, sprite_pos):
    draw_pos = (cycle-1) % 40
    return draw_pos in range(sprite_pos-1, sprite_pos+2)

def get_screen(screen) -> None:
    scan_lines = ichunked(screen,40)
    str_lines = ["".join(scan_line) for scan_line in scan_lines]
    return "\n".join(str_lines)


def run(data: list[str]):
    ops = sum([parse(line) for line in data],[])

    sprite_pos = 1

    interesting_values = []
    screen = []

    for cycle, op in enumerate(ops, 1):
        if should_draw_pos(cycle, sprite_pos):
            screen.append("#")
        else:
            screen.append(".")

        if (cycle - 20) % 40 == 0:
            interesting_values.append(sprite_pos * cycle)

        sprite_pos += op

    print("\nPART 1:\n")
    print(sum(interesting_values))
    print("\nPART 2:\n")
    print(get_screen(screen))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        input_file = TEST_FILES[0]
    elif len(sys.argv) == 3:
        input_file = TEST_FILES[int(sys.argv[2])]
    else:
        input_file = INPUT_FILE

    with open(input_file, encoding="utf8") as lines:
        run(list(lines))
