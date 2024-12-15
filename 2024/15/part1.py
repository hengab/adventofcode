#!/usr/bin/env python

import sys
import time
import typing as typ
import logging

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

logger = logging.getLogger(__name__)
Location = typ.Tuple[int, int]
Direction = typ.Tuple[int, int]

def print_grid(grid: typ.List[typ.List[str]]):
    grid.reverse()
    for y in range(len(grid)):
        row = ""
        for x in range(len(grid[y])):
            row += grid[y][x]
        print(row)

    grid.reverse()


def split_at_blank_line(lines: typ.List[str]) -> typ.List[typ.List[str]]:
    results = []

    for i in range(len(lines)):
        if lines[i] == "":
            results.append(lines[:i])

    if len(results) == 0:
        results.append(lines)

    return results

def move(grid, fr: Location, to: Location, ch: str):    
    grid[to[1]][to[0]] = ch
    grid[fr[1]][fr[0]] = "."

def try_move(grid: typ.List[typ.List[str]], location: Location, direction: Direction) -> Location:
    source_grid_value = grid[location[1]][location[0]]
    destination_location = (location[0] + direction[0], location[1] + direction[1])
    destination_grid_value = grid[destination_location[1]][destination_location[0]]
    resulting_location = location

    if destination_grid_value == ".":
        move(grid, location, destination_location, source_grid_value)
        resulting_location = destination_location
    elif destination_grid_value == "O":
        try_move(grid, destination_location, direction)
        destination_grid_value = grid[destination_location[1]][destination_location[0]]
        if destination_grid_value == ".":
            move(grid, location, destination_location, source_grid_value)
            resulting_location = destination_location

    return resulting_location
    

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
logger.info("--------Part 1--------")

start_time = time.perf_counter()


grid: typ.List[typ.List[str]] = []
movements = {">": (1, 0), "v": (0, -1), "<": (-1, 0), "^": (0, 1)}

with open(input_file_name) as fh:
    g, m = fh.read().split("\n\n")
    raw_grid = [line.strip() for line in g.split("\n")]
    
    robot_movements = [c for c in m.replace("\n", "")]
    robot_location = (0, 0)
    raw_grid.reverse()
    for y in range(len(raw_grid)):
        row = []
        for x in range(len(raw_grid[y])):
            value = raw_grid[y][x]
            if value == "@":
                robot_location = (x, y)
            row.append(value)
        grid.append(row)

for m in robot_movements:
    print(f"Move {m}")
    direction = movements[m]
    robot_location = try_move(grid, robot_location, direction)
    print_grid(grid)


grid.reverse()
result = 0
for y in range(len(grid)):
    for x in range(len(grid[y])):
        value = grid[y][x]
        if value == "O":
            result += (y * 100) + x

print(f"Result: {result}")
logger.info(f"Elapsed time: {time.perf_counter() - start_time} s")
