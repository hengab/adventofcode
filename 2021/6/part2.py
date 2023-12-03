#!/usr/bin/env python

import sys
import time
import typing as typ

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
print("--------Part 2--------")

start_time = time.perf_counter()


with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]
    fish: typ.List[int] = 0
    for line in lines:
        fish = [int(f) for f in line.split(",")]

        fish_frequency = {i:fish.count(i) for i in set(fish)}
        
        for day in range(256):
            new_fish = fish_frequency.get(0, 0)
            fish_frequency = {k-1:v for k,v in fish_frequency.items() if k > 0}
            fish_frequency[8] = new_fish
            fish_frequency[6] = fish_frequency.get(6, 0) + new_fish
            print(f"After {day+1:02} day{':  ' if day==0 else 's: '}{fish_frequency}")

        print(f"No of fish: {sum(fish_frequency.values())}")

print(f"Elapsed time: {time.perf_counter() - start_time} s")
