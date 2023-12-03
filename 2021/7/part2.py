#!/usr/bin/env python

import sys
import time
import typing as typ

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
print("--------Part 2--------")

start_time = time.perf_counter()


# with open(input_file_name) as fh:
#     lines = [line.strip() for line in fh.readlines()]
#     for line in lines:
#         position_costs = {}
#         sub_positions = [int(p) for p in line.split(",")]
#         for position in range(min(sub_positions), max(sub_positions)):
#             cost = sum([sum([c for c in range(abs(p - position) + 1)]) for p in sub_positions])
#             position_costs[position] = cost

#         print(position_costs)

#         min_cost_position = min(position_costs, key=position_costs.get)
#         print(f"Position: {min_cost_position} - Cost: {position_costs[min_cost_position]}")

with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]
    for line in lines:
        position_costs = {}
        sub_positions = [int(p) for p in line.split(",")]
        sub_position_frequencies = {
            i: sub_positions.count(i) for i in set(sub_positions)
        }

        for position in range(min(sub_positions), max(sub_positions)):
            cost = sum(
                [sum([c for c in range(abs(p - position) + 1)]) * freq for p, freq in sub_position_frequencies.items()]
            )
            position_costs[position] = cost

        print(position_costs)

        min_cost_position = min(position_costs, key=position_costs.get)
        print(
            f"Position: {min_cost_position} - Cost: {position_costs[min_cost_position]}"
        )


print(f"Elapsed time: {time.perf_counter() - start_time} s")
