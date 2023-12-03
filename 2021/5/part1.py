#!/usr/bin/env python

import sys
import time
import typing as typ

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
print("--------Part 1--------")


class Coordinate(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Coordinate):
            return self.x == __value.x and self.y == __value.y

        return False

    def __hash__(self):
        return (self.x, self.y).__hash__()


start_time = time.perf_counter()

Line = typ.Tuple[Coordinate, Coordinate]


def print_map(
    min_coordinate: Coordinate,
    max_coodinate: Coordinate,
    frequencies: typ.Dict[Coordinate, int],
) -> None:
    default_symbol = "."
    rows = max_coodinate.y - min_coordinate.y + 1
    columns = max_coodinate.x - min_coordinate.x + 1
    grid = [[default_symbol for _ in range(rows)] for _ in range(columns)]

    # Assign values to the non-default cells
    for coordinate, frequency in frequencies.items():
        grid[coordinate.x - min_coordinate.x][coordinate.y - min_coordinate.y] = str(
            frequency
        )

    top_and_bottom = "-" * columns
    print(f"+{top_and_bottom}+")
    for row in range(rows):
        line = ""
        for column in range(columns):
            line = f"{line}{grid[column][row]}"
        print(f"|{line}|")

    print(f"+{top_and_bottom}+")


def line_coordinates(x0, y0, x1, y1) -> typ.Generator[Coordinate, None, None]:
    deltax = x1 - x0
    deltay = y1 - y0
    if deltax == 0 or deltay == 0:
        dxsign = int(abs(deltax) / deltax) if deltax != 0 else 0
        dysign = int(abs(deltay) / deltay) if deltay != 0 else 0
        x = x0
        y = y0
        while x != x1 or y != y1:
            yield Coordinate(x, y)
            x += dxsign
            y += dysign

        yield Coordinate(x1, y1)


def mark_coordinates(vent_lines: typ.List[Line]) -> typ.Dict[Coordinate, int]:
    coordinate_frequencies: typ.Dict[Coordinate, int] = {}
    for vent_line in vent_lines:
        for coords in line_coordinates(
            vent_line[0].x, vent_line[0].y, vent_line[1].x, vent_line[1].y
        ):
            print
            coordinate_frequencies[coords] = coordinate_frequencies.get(coords, 0) + 1

    return coordinate_frequencies


with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]

    vent_lines: typ.List[Line] = []
    min_coordinate = Coordinate(0, 0)
    max_coordinate = Coordinate(0, 0)

    for line in lines:
        line = line.strip()
        start, end = line.split("->")
        start_coordinate = Coordinate(
            int(start.split(",")[0]), int(start.split(",")[1])
        )
        end_coordinate = Coordinate(int(end.split(",")[0]), int(end.split(",")[1]))
        vent_line = (start_coordinate, end_coordinate)
        vent_lines.append(vent_line)
        min_coordinate.x = min(min_coordinate.x, start_coordinate.x, end_coordinate.x)
        min_coordinate.y = min(min_coordinate.y, start_coordinate.y, end_coordinate.y)
        max_coordinate.x = max(max_coordinate.x, start_coordinate.x, end_coordinate.x)
        max_coordinate.y = max(max_coordinate.y, start_coordinate.y, end_coordinate.y)

    # for line in vent_lines:
    #     print(line)

    r = mark_coordinates(vent_lines)
    print_map(min_coordinate, max_coordinate, r)
    high_frequency_count = 0
    for coord, frequency in r.items():
        if frequency > 1:
            high_frequency_count += 1

    print(f"High frequency cells: {high_frequency_count}")

print(f"Elapsed time: {time.perf_counter() - start_time} s")
