#!/usr/bin/env python

import sys
import time
import typing as typ

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
print("--------Part 1--------")

start_time = time.perf_counter()


with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]
    fish: typ.List[int] = 0
    for line in lines:
        fish = [int(f) for f in line.split(",")]

        print(f"Initial state: {fish}")
        for day in range(80):
            for lantern_fish in range(len(fish)):
                if fish[lantern_fish] == 0:
                    fish.append(8)
                fish[lantern_fish] = (
                    6 if fish[lantern_fish] == 0 else fish[lantern_fish] - 1
                )
            print(f"After {day+1:02} day{':  ' if day==0 else 's: '}{fish}")

        print(f"No of fish: {len(fish)}")

print(f"Elapsed time: {time.perf_counter() - start_time} s")
