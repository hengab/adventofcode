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
    for line in lines:
        ...


logger.info(f"Elapsed time: {time.perf_counter() - start_time} s")
