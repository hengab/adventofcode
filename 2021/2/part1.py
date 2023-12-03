#!/usr/bin/env python

import sys
import time
import typing as typ

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
print("--------Part 1--------")

start_time = time.perf_counter()


position = (0, 0)
with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]
    for line in lines:
        line = line.strip()
        direction, amount = line.split()

        if direction == "forward":
            position = (position[0] + int(amount), position[1])
        elif direction == "down":
            position = (position[0], position[1] - int(amount))
        elif direction == "up":
            position = (position[0], position[1] + int(amount))
        else:
            raise Exception(f"Undespected direction {direction}")

print(f"Result {position[0] * position[1] * -1}")
print(f"Elapsed time: {time.perf_counter() - start_time} s")
