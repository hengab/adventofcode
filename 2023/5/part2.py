#!/usr/bin/env python

import sys
import time
import typing as typ
import logging
import sys

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

logger = logging.getLogger(__name__)

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
logger.info("--------Part 2--------")

start_time = time.perf_counter()


with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]


Source = str
Destination = str
SourceIdStart = int
SourceIdEnd = int
DestinationOffset = int
maps: typ.Dict[
    Source,
    typ.Tuple[
        Destination, typ.List[typ.Tuple[SourceIdStart, SourceIdEnd, DestinationOffset]]
    ],
] = {"location": ("none", [(0, sys.maxsize, 0)])}

seeds = lines[0].removeprefix("seeds: ").split()
seed_ranges: typ.List[typ.Tuple[SourceIdStart, SourceIdEnd]] = []
for i in range(0, len(seeds), 2):
    range_start = int(seeds[i])
    seed_ranges.append((range_start, range_start + int(seeds[i + 1])))


current_map: typ.List[typ.Tuple[SourceIdStart, SourceIdEnd, DestinationOffset]] = []
current_source: str = None
for line in lines[1:]:
    logger.debug("--------------")
    logger.debug(f"Line: {line}")
    logger.debug(f"Current source: {current_source}")
    logger.debug(f"Current map: {current_map}")

    if line.find("map:") > -1:
        source, destination = line.removesuffix(" map:").split("-to-")
        current_map = []
        maps[source] = (destination, current_map)
        current_source = source
    elif line == "":
        current_map = None

    else:
        destination_start, source_start, span = line.split()
        current_map.append(
            (
                int(source_start),
                int(source_start) + int(span),
                int(destination_start) - int(source_start),
            )
        )

    logger.debug("--------------")

logger.debug(f"Maps: {maps}")

seed_ranges: typ.List[typ.Tuple[SourceIdStart, SourceIdEnd]] = []
for i in range(0, len(seeds), 2):
    range_start = int(seeds[i])
    seed_ranges.append((range_start, range_start + int(seeds[i + 1])))
seed_ranges = sorted(seed_ranges)
logger.debug("----------------")
ranges = {"seed": seed_ranges}
# seed_ranges = sorted(maps["seed"][1])
# parsed_soil_ranges = sorted(maps["soil"][1])
# parsed_fertilizer_ranges = sorted(maps["fertilizer"][1])
# parsed_water_ranges = sorted(maps["water"][1])
# parsed_light_ranges = sorted(maps["light"][1])
# parsed_temperature_ranges = sorted(maps["temperature"][1])
# parsed_humidity_ranges = sorted(maps["humidity"][1])
# parsed_location_ranges = sorted(maps["location"][1])

current_source = "seed"
while current_source != "location":
    # current_destination = maps[current_source][0]
    current_ranges = ranges[current_source]
    logger.debug("-----------------")
    logger.debug(f"{current_source} ranges: {current_ranges}")
    next_ranges = []

    sorted_range_sources = sorted(maps[current_source][1])
    logger.debug(f"{current_source}-to-{maps[current_source][0]}: {sorted_range_sources}")
    range_sources = []
    # fill in blanks maybe
    sorted_range_sources.insert(0, (-1, 0, 0))
    sorted_range_sources.append((sorted_range_sources[-1][1], sys.maxsize, 0))
    logger.debug(f"{current_source}-to-{maps[current_source][0]}: {sorted_range_sources}")

    for current_range in current_ranges:
        start_range_index = None
        end_range_index = None
        
        for i in range(len(sorted_range_sources) - 1):
            if sorted_range_sources[i][1] < sorted_range_sources[i + 1][0]:
                range_sources.append(
                    (sorted_range_sources[i][1], sorted_range_sources[i + 1][0], 0)
                )

            range_sources.append(sorted_range_sources[i + 1])

        logger.debug(f"range_sources: {range_sources}")
        for i in range(len(range_sources)):
            if range_sources[i][0] <= current_range[0] < range_sources[i][1]:
                logger.debug(
                    f"  {range_sources[i][0]} <= {current_range[0]} < {range_sources[i][1]} => {range_sources[i][0] <= current_range[0] < range_sources[i][1]}"
                )
                start_range_index = i
            if range_sources[i][0] <= current_range[1] < range_sources[i][1]:
                logger.debug(
                    f"  {range_sources[i][0]} <= {current_range[1]} < {range_sources[i][1]} => {range_sources[i][0] <= current_range[1] < range_sources[i][1]}"
                )
                end_range_index = i
            if start_range_index is not None and end_range_index is not None:
                break


        logger.debug(
            f"start_range_index {start_range_index} - end_range_index {end_range_index}"
        )
        for i in range(start_range_index, end_range_index + 1):            
            start = (
                max(current_range[0], range_sources[i][0])
                + range_sources[i][2]
            )
            logger.debug(f"max({current_range[0]}, {range_sources[i][0]}) + {range_sources[i][2]}) = {start}")
            end = (
                min(current_range[1], range_sources[i][1])
                + range_sources[i][2]
            )
            logger.debug(f"min({current_range[1]}, {range_sources[i][1]}) + {range_sources[i][2]}) = {end}")

            next_ranges.append((start, end))

        logger.debug(next_ranges)


    current_source = maps[current_source][0]
    ranges[current_source] = next_ranges
for k,v in ranges.items():
    logger.info(f"{k}: {v}")
    logger.info(maps[k])
logger.info(f"Result: {sorted(ranges['location'])[0]}")
logger.info(f"Elapsed time: {time.perf_counter() - start_time} s")
