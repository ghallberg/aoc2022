import sys
from dataclasses import dataclass

INPUT_FILE = "input/day7.txt"
TEST_FILE = "input/day7test.txt"

DISK_SIZE = 70000000
UPDATE_SIZE = 30000000

@dataclass
class Folder:
    name: str
    parent: str
    children: dict[str: 'Folder']
    files: dict[str: int]

def gather_sizes(folder: Folder) -> list[int]:
    child_sizes = [gather_sizes(child) for child in folder.children.values()]
    biggest_child_sizes = [max(sizes) for sizes in child_sizes]

    total_file_size = sum([size for size in folder.files.values()])

    my_size = total_file_size + sum(biggest_child_sizes)

    return sum(child_sizes, [my_size])

def parse(output: list[str]):
    root_dir = Folder(name="/", parent=None, children={}, files={})
    cwd = root_dir
    for row in output[1:]:
        tokens = row.split()

        if tokens[0] == "$":
            if tokens[1] == "cd":
                target = tokens[2]
                if target == "..":
                    if cwd.parent != None:
                        cwd = cwd.parent
                else:
                    cwd = cwd.children[target]

        elif tokens[0] == "dir":
            child_name = tokens[1]
            if not cwd.children.get(child_name):
                cwd.children[child_name] = Folder(name = child_name, parent=cwd, children={}, files={})
        else:
            size, filename = tokens
            cwd.files[filename] = int(size)

    return root_dir

def run(data: list[str]):
    root = parse(data)
    sizes = gather_sizes(root)
    print(sum([size for size in sizes if size <= 100000]))
    root_size = max(sizes)
    free_space = DISK_SIZE - root_size
    needed_space = UPDATE_SIZE - free_space

    print(min([size for size in sizes if size >= needed_space]))



if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        input_file = TEST_FILE
    else:
        input_file = INPUT_FILE

    with open(input_file, encoding="utf8") as lines:
        run(list(lines))
