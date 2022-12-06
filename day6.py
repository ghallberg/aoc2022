import sys
from collections.abc import Sequence


def get_marker(datastream: str, length):
    window = []

    for i, c in enumerate(datastream):
        window = window[-(length-1):]
        window.append(c)

        if len(set(window)) == length:
            return i+1

def run(data: Sequence[str]):
    start_index = get_marker(data[0], 4)
    message_index = get_marker(data[0], 14)
    print(start_index)
    print(message_index)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            lines= [
                    "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
                   ]
            run(lines)

    else:
        with open("input/day6.txt", encoding="utf8") as lines:
            run(list(lines))
