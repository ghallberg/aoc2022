#! /usr/bin/env python

def calc_cals(cal_counts, num_elves):
    return sum(sorted(cal_counts, reverse=True)[0:num_elves])

def run_day1():
    with open("input/day1.txt", encoding="utf8") as cal_data:
        elves = {}
        elf_count = 1
        cal_sum = 0
        for line in cal_data:
            line = line.strip()
            if line == "":
                elves[elf_count] = cal_sum
                cal_sum = 0
                elf_count = elf_count + 1
            else:
                cal_sum = cal_sum + int(line)

        print(calc_cals(elves.values(), 1))
        print(calc_cals(elves.values(), 3))

if __name__ == '__main__':
    run_day1()
