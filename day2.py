import sys
POINTS = {"r": 1, "p": 2, "s": 3, "me": 6, "=": 3, "you": 0}

RESULTS = {"r": {"r": "=", "p": "you", "s": "me"},
           "p": {"r": "me", "p": "=", "s": "you"},
           "s": {"r": "you", "p": "me", "s": "="}}

WANTED_RESULT = {"X": "you", "Y": "=", "Z": "me"}

INV_RESULTS = {"r": {"me": "p", "=": "r", "you": "s"},
               "s": {"me": "r", "=": "s", "you": "p"},
               "p": {"me": "s", "=": "p", "you": "r"}}

TRANSLATION = {"A": "r", "B": "p", "C": "s", "X": "r", "Y": "p", "Z": "s"}

def translate(me, you):
    t_me = TRANSLATION[me]

    return t_me

def round_score(me, result):
    return POINTS[me] + POINTS[result]


def run(strat):
    total_score1 = 0
    total_score2 = 0

    for line in strat:
        you, me = line.strip().split(" ")
        t_you = TRANSLATION[you]
        t_me1 = TRANSLATION[me]
        result1 = RESULTS[t_me1][t_you]

        result2 = WANTED_RESULT[me]
        t_me2 = INV_RESULTS[t_you][result2]



        total_score1 = total_score1 + round_score(t_me1, result1)
        total_score2 = total_score2 + round_score(t_me2, result2)

    print("Part 1:", total_score1)
    print("Part 2:", total_score2)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            strat = ["A Y", "B X", "C Z"]
            run(strat)

    else:
        with open("input/day2.txt", encoding="utf8") as strat:
            run(strat)
