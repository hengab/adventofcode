#!/usr/bin/env python

import sys
import time
import typing as typ

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
print("--------Part 1--------")

start_time = time.perf_counter()

bag_content = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def score_game(game: str) -> int:
    game: int = int(line.split(":")[0].split()[1])
    sets: typ.List[str] = line.split(":")[1].split(";")
    for cube_set in sets:
        colors = cube_set.split(",")
        for color in colors:
            count = int(color.split()[0])
            color_name = color.split()[1]

            if count > bag_content[color_name]:
                return 0

    return game


with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]
    score = 0
    for line in lines:
        line = line.strip()
        score += score_game(line)

    print(score)


print(f"Elapsed time: {time.perf_counter() - start_time} s")
