#!/usr/bin/env python

import sys
import time
import typing as typ
from collections import Counter

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
print("--------Part 2--------")

start_time = time.perf_counter()

bits: typ.List[typ.List[str]] = []
oxygen_generator_rating_candidates: typ.List[str] = []
co2_scrubber_rating_candidates: typ.List[str] = []

with open(input_file_name) as input_file:
    for line in input_file.readlines():
        line = line.strip()
        
        oxygen_generator_rating_candidates.append(line)
        co2_scrubber_rating_candidates.append(line)
        if len(bits) < len(line):
            for i in range(len(line) - len(bits)):
                bits.append([])

        for i in range(len(bits)):
            bits[i].append(line[i])

for i in range(len(bits)):    
    # most_common = Counter("".join(bits[i])).most_common()[0][0]
    # least_common = "0" if int(most_common) == 1 else "1"
    
    if len(oxygen_generator_rating_candidates) > 1:
        commonality = Counter("".join([c[i] for c in oxygen_generator_rating_candidates]))
        # print(commonality)
        most_common = "0" if commonality["0"] > commonality["1"] else "1"
        oxygen_generator_rating_candidates = [v for v in oxygen_generator_rating_candidates if v[i] == most_common]
        # print(i, most_common, oxygen_generator_rating_candidates)
    
    if len(co2_scrubber_rating_candidates) > 1:
        commonality = Counter("".join([c[i] for c in co2_scrubber_rating_candidates]))
        # print(commonality)

        least_common = "1" if commonality["1"] < commonality["0"] else "0"
        co2_scrubber_rating_candidates = [v for v in co2_scrubber_rating_candidates if v[i] == least_common]
        # print(i, least_common, co2_scrubber_rating_candidates)
    
print(oxygen_generator_rating_candidates)
print(co2_scrubber_rating_candidates)
print(f"Result {int(''.join(oxygen_generator_rating_candidates), 2) * int(''.join(co2_scrubber_rating_candidates), 2)}")

print(f"Elapsed time: {time.perf_counter() - start_time} s")
