#!/usr/bin/env python

import sys
import time
import typing as typ

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
print("--------Part 2--------")

start_time = time.perf_counter()

bag_content = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def score_game(game: str) -> int:
    game: int = int(line.split(":")[0].split()[1])
    sets: typ.List[str] = line.split(":")[1].split(";")
    minimum_cubes_needed: typ.Dict[str, int] = {}
    for cube_set in sets:
        colors = cube_set.split(",")
        for color in colors:
            count = int(color.split()[0])
            color_name = color.split()[1]

            minimum_cubes_needed[color_name] = max(
                minimum_cubes_needed.get(color_name, 0), count
            )

    score = 1
    print(minimum_cubes_needed)
    for color_name, cube_count in minimum_cubes_needed.items():
        score *= cube_count

    print(f"{minimum_cubes_needed} - {score}")
    return score


with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]
    score = 0
    for line in lines:
        line = line.strip()
        score += score_game(line)

    print(score)


print(f"Elapsed time: {time.perf_counter() - start_time} s")
