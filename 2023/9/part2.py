#!/usr/bin/env python

import sys
import time
import typing as typ
import logging

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

logger = logging.getLogger(__name__)

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
logger.info("--------Part 2--------")

start_time = time.perf_counter()


with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]

prepended_values = []
extension_values = []
for line in lines:
    logger.debug("-----------------------")
    first_level = [int(c.strip()) for c in line.split()]
    levels = [first_level]
    logger.debug(levels[0])

    current_level = first_level
    while not all(v == 0 for v in current_level):
        next_level = []
        for i in range(len(current_level) - 1):
            next_level.append(current_level[i + 1] - current_level[i])

        logger.debug(f"next_level: {next_level}")
        levels.append(next_level)
        current_level = next_level
    
    logger.debug(f"Extending {levels}")
    for i in range(len(levels) -2, -1, -1):
        levels[i].insert(0, levels[i][0] - levels[i+1][0])
        levels[i].append(levels[i][-1] + levels[i+1][-1])
        logger.debug(levels[i])


    logger.debug(f"Result {levels[0]}")
    prepended_values.append(levels[0][0])
    extension_values.append(levels[0][-1])

# logger.info(f"Result {sum(extension_values)} - {extension_values}")
logger.info(f"Result {sum(prepended_values)} -- {prepended_values}")
logger.info(f"Elapsed time: {time.perf_counter() - start_time} s")
