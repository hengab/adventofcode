#!/usr/bin/env python

import sys
import time
import typing as typ

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
print("--------Part 1--------")

start_time = time.perf_counter()

depth_increases = 0
previous_depth = None
with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]
    for line in lines:
        line = line.strip()
        
        depth = int(line)

        if depth > (previous_depth or sys.maxsize):
            depth_increases = depth_increases + 1
        
        previous_depth = depth

print(f"Increases: {depth_increases}")




print(f"Elapsed time: {time.perf_counter() - start_time} s")
