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

seeds = lines[0].removeprefix("seeds: ").split()
Source = str
Destination = str
SourceIdStart = int
SourceIdEnd = int
DestinationOffset = int
maps: typ.Dict[Source, typ.Tuple[Destination, typ.Dict[typ.Tuple[SourceIdStart, SourceIdEnd], DestinationOffset]]] = {}

current_map: typ.Dict[typ.Tuple[SourceIdStart, SourceIdEnd], DestinationOffset] = {}
current_source: str = None
for line in lines[1:]:
    logger.debug("--------------")
    logger.debug(f"Line: {line}")
    logger.debug(f"Current source: {current_source}")
    logger.debug(f"Current map: {current_map}")

    if line.find("map:") > -1:
        source, destination = line.removesuffix(" map:").split("-to-")
        current_map = {}
        maps[source] = (destination, current_map)
        current_source = source
    elif line == "":
        current_map = None
    
    else:
        destination_start, source_start, span = line.split()
        current_map[(int(source_start), int(source_start) + int(span))] = int(destination_start) - int(source_start)

    logger.debug("--------------")

values = [int(s) for s in seeds]
source = "seed"

while source != "location":
    for i in range(len(values)):
        new_value = values[i]
        for source_bounds, destination_offset in maps[source][1].items():
            if  source_bounds[0] <= values[i] <= source_bounds[1]:
                new_value = values[i] + destination_offset 
        # new_value = maps[source][1].get(values[i], values[i])
        logger.debug(f"{source} {values[i]} -> {maps[source][0]} {new_value}")
        values[i] = new_value

    source = maps[source][0]

# for i in range(len(values)):
#     values[i] = maps[source][1].get(values[i], values[i])

logger.info(f"Lowest location {min(values)}")

logger.info(f"Elapsed time: {time.perf_counter() - start_time} s")
