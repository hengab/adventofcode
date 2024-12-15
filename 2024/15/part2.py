#!/usr/bin/env python

import sys
import time
import typing as typ
import logging

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

logger = logging.getLogger(__name__)
Location = typ.Tuple[int, int]
Direction = typ.Tuple[int, int]
box_left = "["
box_right = "]"
wall = "#"
empty = "."
grid: typ.List[typ.List[str]] = []
movements = {">": (1, 0), "v": (0, -1), "<": (-1, 0), "^": (0, 1)}


def print_grid(grid: typ.List[typ.List[str]]):
    y_digits = len(str(len(grid)))

    grid.reverse()
    for y in range(len(grid)):
        row = f"{len(grid) - y - 1}".rjust(y_digits)
        for x in range(len(grid[y])):
            row += grid[y][x]
        print(row)
    print(
        "".rjust(y_digits)
        + "012345678901234567890123456789012345678901234567890123456789"
    )
    print(
        "".rjust(y_digits)
        + "0         1         2         3         4         5         "
    )
    grid.reverse()


def split_at_blank_line(lines: typ.List[str]) -> typ.List[typ.List[str]]:
    results = []

    for i in range(len(lines)):
        if lines[i] == "":
            results.append(lines[:i])

    if len(results) == 0:
        results.append(lines)

    return results


def move(
    grid, fr: Location, to: Location, ch: str, text: str = "Moving"
) -> typ.List[typ.Tuple[Location, Location, str]]:
    print(f"{text} {ch} from {fr} to {to}")
    grid[to[1]][to[0]] = ch
    grid[fr[1]][fr[0]] = empty

    return [(to, fr, ch)]


def try_move(
    grid: typ.List[typ.List[str]], location: Location, direction: Direction, depth: int
) -> typ.Tuple[Location, typ.List[typ.Tuple[Location, Location, str]]]:
    source_grid_value = grid[location[1]][location[0]]
    destination_location = (location[0] + direction[0], location[1] + direction[1])
    destination_grid_value = grid[destination_location[1]][destination_location[0]]
    resulting_location = location
    undos = []

    print(
        f"{direction}:{depth} - Try moving {source_grid_value} from {location} to {destination_location}"
    )
    if destination_grid_value == empty:
        undos = move(
            grid,
            location,
            destination_location,
            source_grid_value,
            f"{direction}:{depth} - Moving",
        )
        resulting_location = destination_location
    elif destination_grid_value in [box_left, box_right]:
        new_box_location, box_undos = try_move(
            grid, destination_location, direction, depth + 1
        )
        if (
            direction in [movements["^"], movements["v"]]
            and new_box_location != destination_location
        ):
            other_box_location = (
                (destination_location[0] + 1, destination_location[1])
                if destination_grid_value == box_left
                else (destination_location[0] - 1, destination_location[1])
            )
            print(
                f"{direction}:{depth} - Try moving other box location {other_box_location}"
            )
            new_other_box_location, other_box_undos = try_move(
                grid, other_box_location, direction, depth + 1
            )
            if new_other_box_location == other_box_location:
                print(
                    f"{direction}:{depth} - Undo {new_box_location}:{destination_location} - {new_other_box_location}:{other_box_location} - {depth}"
                )
                print_grid(grid)
                for u in box_undos:
                    move(grid, u[0], u[1], u[2], f"{direction}:{depth} - Undoing")
            else:
                undos = other_box_undos + box_undos
        destination_grid_value = grid[destination_location[1]][destination_location[0]]
        if destination_grid_value == empty:
            undo = move(
                grid,
                location,
                destination_location,
                source_grid_value,
                f"{direction}:{depth} - Moving",
            )
            undos = undo + undos
            resulting_location = destination_location

    return resulting_location, undos


input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
logger.info("--------Part 2--------")

start_time = time.perf_counter()

with open(input_file_name) as fh:
    g, m = fh.read().split("\n\n")
    g = g.replace("#", "##").replace(".", "..").replace("O", "[]").replace("@", "@.")
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

print_grid(grid)

step = 0
for m in robot_movements:
    step += 1
    print(f"Move {m} ({step})")
    direction = movements[m]
    robot_location, undos = try_move(grid, robot_location, direction, 0)

    print_grid(grid)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == box_left and grid[y][x + 1] != box_right:
                exit()


grid.reverse()
result = 0
for y in range(len(grid)):
    for x in range(len(grid[y])):
        value = grid[y][x]
        if value == box_left:
            result += (y * 100) + x

print(f"Result: {result}")
logger.info(f"Elapsed time: {time.perf_counter() - start_time} s")
