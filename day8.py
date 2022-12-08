import sys
from dataclasses import dataclass
from itertools import product

INPUT_FILE = "input/day8.txt"
TEST_FILE = "input/day8test.txt"

# 30373
# 25512
# 65332
# 33549
# 35390


def parse(grid: list[list[str]]) -> list[list[int]]:
    return [[int(s) for s in row.strip()] for row in grid]

def columns(grid: list[list[int]]) -> list[list[int]]:
    return [[row[i] for row in grid] for i in range(0,len(grid))]

def hidden_by(tree: int, row: list[int]) -> bool:
    return any([other >= tree for other in row])

def hidden_in(i:int, row: list[int]) -> bool:
    tree = row[i]
    before = row[:i]
    after = row[i+1:]
    hidden = hidden_by(tree, before) and hidden_by(tree, after)

    return hidden

def hidden_at(x,y, row, column):
    return hidden_in(y, row) and hidden_in(x, column)

def score_towards(height: int, view: list[int]):
    for i, other in enumerate(view):
        if other >= height:
            return i+1

    return len(view)



def scenic_in(i:int, row: list[int]) -> bool:
    height = row[i]
    before = list(reversed(row[:i]))
    after = row[i+1:]

    score = score_towards(height, before) * score_towards(height, after)

    return score

def scenic_score(x: int, y: int, row: list[int], column: list[int]) -> int:
    return scenic_in(y, row) * scenic_in(x, column)

def run(data: list[str]):
    grid = parse(data)
    transposition = columns(grid)

    hidden_count = 0
    max_scenic = 0
    for x,y in product(range(1, len(grid)-1), repeat=2):
        if hidden_at(x,y, grid[x], transposition[y]):
            hidden_count+=1
        scenic = scenic_score(x,y, grid[x], transposition[y])
        if scenic > max_scenic:
            max_scenic = scenic

    num_trees = len(grid) * len(transposition)

    print("VISIBLE TREES:", num_trees - hidden_count)
    print("MAX SCENIC:", max_scenic)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        input_file = TEST_FILE
    else:
        input_file = INPUT_FILE

    with open(input_file, encoding="utf8") as lines:
        run(list(lines))
