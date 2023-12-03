#!/usr/bin/env python

import sys
import time
import typing as typ
from collections import deque

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
print("--------Part 2--------")

start_time = time.perf_counter()


depth_increases = 0
previous_depths = deque(maxlen=4)
with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]
    for line in lines:
        line = line.strip()
        
        depth = int(line)
        previous_depths.append([])

        for d in previous_depths:
            d.append(depth)
        # Start measuring once we have four deques
        if len(previous_depths) > 3:
            # print(f"Comparing {sum(previous_depths[0][0:3])} < {sum(previous_depths[1])} ({sum(previous_depths[0][0:3]) < sum(previous_depths[1])})")
            if sum(previous_depths[0][0:3]) < sum(previous_depths[1]):
                depth_increases = depth_increases + 1
        

print(f"Increases: {depth_increases}")

print(f"Elapsed time: {time.perf_counter() - start_time} s")
