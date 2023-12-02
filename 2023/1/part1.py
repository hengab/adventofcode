#!/usr/bin/env python

import os
import sys
import time
import typing as typ

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
print("--------Part 1--------")

start_time = time.perf_counter()


def find_first_digit(input: str) -> str:
    for c in input:
        if c.isdigit():
            return c


with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]
    calibration_values = []
    for line in lines:
        line = line.strip()
        first_digit = find_first_digit(line)
        last_digit = find_first_digit(line[::-1])

        calibration_value = int(f"{first_digit}{last_digit}")
        calibration_values.append(calibration_value)

    print(sum(calibration_values))


print(f"Elapsed time: {time.perf_counter() - start_time} s")
