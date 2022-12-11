import sys
from more_itertools import chunked
from collections import namedtuple
from functools import partial
from copy import deepcopy
import math

INPUT_FILE = "input/day11.txt"
TEST_FILES = [ "input/day11test.txt"]
NIY = "401: NIY"

Monkey = namedtuple("Monkey", "number items, op, test, yes, no")

def parse_op(line: str):
    def squared(val):
        return val ** 2

    def add(x, y):
        return x+y

    def mul(x, y):
        return x*y

    tokens = line.split()

    op = tokens[4]
    y = tokens[5].strip()

    if op == "*":
        if y == "old":
            return squared
        else:
            return partial(mul, y=int(y))

    if op == "+":
        if y == "old":
            return partial(mul, y=2)
        else:
            return partial(add, y=int(y))

    return fun

def parse(chunk: list[str]) -> Monkey:
    number = int(chunk[0].split()[-1].strip(":\n"))
    items = [int(list_no.strip(",\n")) for list_no in chunk[1].split()[2:]]
    op = parse_op(chunk[2])
    test = int(chunk[3].split()[-1])
    yes = int(chunk[4].split()[-1])
    no = int(chunk[5].split()[-1])

    return Monkey(number=number, items=items, op=op, test=test, yes=yes, no=no)

def run(data: list[str]) -> (str,str):
    def inspections_in_rounds(monkeys, relief, rounds):
        no_monkey_inspections = [0]*len(monkeys)
        fac = math.prod([monkey.test for monkey in monkeys]) # Tack Tigge

        for round in range(0,rounds):
            for monkey in monkeys:
                for item in monkey.items:
                    no_monkey_inspections[monkey.number] +=1
                    inspect_worry = monkey.op(item)
                    if relief:
                        bored_worry = inspect_worry//3
                    else:
                        bored_worry = inspect_worry%fac
                    if bored_worry % monkey.test == 0:
                        monkeys[monkey.yes].items.append(bored_worry)
                    else:
                        monkeys[monkey.no].items.append(bored_worry)
                monkey.items.clear()
        return no_monkey_inspections

    monkeys = [parse(chunk) for chunk in chunked(data, 7)]

    part1_inspections = inspections_in_rounds(deepcopy(monkeys), True, 20)
    no2, no1 = sorted(part1_inspections)[-2:]
    part1 = no2*no1

    part2_inspections = inspections_in_rounds(deepcopy(monkeys), False, 10000)
    no2, no1 = sorted(part2_inspections)[-2:]
    part2 = no2*no1

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

