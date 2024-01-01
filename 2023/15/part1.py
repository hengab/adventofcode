#!/usr/bin/env python

import sys
import time
import typing as typ
import logging

logging.basicConfig(format="%(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
logger.info("--------Part 1--------")

start_time = time.perf_counter()


with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]

one_liner = "".join(lines)
steps = one_liner.split(",")

sequence_value = 0
for step in steps:
    current_value = 0
    logger.debug(f"current value {current_value}")
    for c in step:
        ascii_value = ord(c)
        logger.debug(f"ASCII of {c} {ascii_value}")
        current_value += ascii_value
        current_value *= 17
        current_value = current_value % 256
        logger.debug(f"current value {current_value}")
    logger.debug(f"{step} becomes {current_value}")
    sequence_value += current_value

logger.info(f"Value = {sequence_value}")
logger.info(f"Elapsed time: {time.perf_counter() - start_time} s")
