import sys
from collections.abc import Sequence
from collections import namedtuple
from copy import deepcopy

Command = namedtuple("Command", "count origin target")

def get_boxes(stack_count: int, stack_line: str):
    boxes = []
    for n in range(0, stack_count):
        box_content = stack_line[n*4+1]
        if box_content == " ":
            boxes.append(None)
        else:
            boxes.append(box_content)

    return boxes

def flip_stacks(lines: list[Sequence[str]]):
    lines.reverse()
    stack_count = len(lines[0])
    stacks = []
    for i in range(0, stack_count):
        stacks.append([box for box in [line[i] for line in lines] if box != None])
    return stacks

def parse_command(command: str):
    parts = command.split()

    return Command(int(parts[1]), int(parts[3]), int(parts[5]))

def parse(data: Sequence[str]):
    data = list(data)
    sep_index = data.index("\n")

    stack_number_line = data[sep_index-1]
    stack_numbers = [int(x) for x in stack_number_line.split() if len(x) != 0]
    stack_count = stack_numbers.pop()


    stack_lines = data[0:sep_index-1]
    box_lines = [get_boxes(stack_count, line) for line in stack_lines]

    command_lines = data[sep_index+1:]

    commands = map(parse_command, command_lines)

    return flip_stacks(box_lines), commands

def move(stacks, command: Command, version: int):
    moving_stack = []
    for _ in range(0, command.count):
        box = stacks[command.origin-1].pop()
        moving_stack.append(box)

    if version == 9001:
        moving_stack.reverse()
    stacks[command.target-1] += moving_stack

def get_output(stacks):
    return "".join([stack[-1] for stack in stacks])

def run(data: Sequence[str]):
    stacks, commands = parse(data)

    stacks2 = deepcopy(stacks)

    for command in commands:
        move(stacks, command, 9000)
        move(stacks2, command, 9001)


    print(get_output(stacks))
    print(get_output(stacks2))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            lines= [
                    "    [D]    ",
                    "[N] [C]    ",
                    "[Z] [M] [P]",
                    " 1   2   3 ",
                    "\n",
                    "move 1 from 2 to 1",
                    "move 3 from 1 to 3",
                    "move 2 from 2 to 1",
                    "move 1 from 1 to 2",
                    ]
            run(iter(lines))

    else:
        with open("input/day5.txt", encoding="utf8") as lines:
            run(lines)
