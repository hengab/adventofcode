#!/usr/bin/env python

import sys
import time
import typing as typ
import logging

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

logger = logging.getLogger(__name__)

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
logger.info("--------Part 1--------")

start_time = time.perf_counter()


with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]

times = lines[0].removeprefix("Time:").strip().split()
record_distances = lines[1].removeprefix("Distance:").strip().split()

ways_to_win = []

for race in range(len(times)):
    race_time = int(times[race])
    record_distance = int(record_distances[race])
    hold = 0
    distance = 0

    while distance <= record_distance:
        hold += 1
        distance = (race_time - hold) * hold

    logger.debug(f"Min: {distance} - {hold}")
    min_hold = hold

    hold = race_time
    distance = 0
    while distance <= record_distance:
        hold -= 1
        distance = (race_time - hold) * hold

    max_hold = hold
    logger.debug(f"Max: {distance} - {hold}")

    ways_to_win.append(max_hold - min_hold + 1)

logger.info(ways_to_win)
result = 1
for value in ways_to_win:
    result *= value

logger.info(result)
logger.info(f"Elapsed time: {time.perf_counter() - start_time} s")
