#!/usr/bin/env python

import sys
import time
import typing as typ

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
print("--------Part 1--------")

start_time = time.perf_counter()


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


def is_adjacent(
    coordinates: typ.List[Coordinate], symbol_locations: typ.List[Coordinate]
) -> bool:
    for symbol_location in symbol_locations:
        if symbol_location in coordinates:
            return True

    return False


with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]

    symbol_locations: typ.List[Coordinate] = []
    numbers: typ.List[typ.Tuple[int, typ.List[Coordinate]]] = []

    for i_line in range(len(lines)):
        line = lines[i_line]
        number = ""
        for i_char in range(len(line)):
            c = line[i_char]
            if c.isdigit():
                number = f"{number}{c}"
            else:
                if len(number) > 0:
                    number_length = len(number)
                    number_entry = (
                        int(number),
                        [
                            Coordinate(i_char, i_line),
                            Coordinate(i_char, i_line - 1),
                            Coordinate(i_char, i_line + 1),
                        ],
                    )
                    for i in range(i_char - number_length - 1, i_char):
                        number_entry[1].append(Coordinate(i, i_line - 1))
                        number_entry[1].append(Coordinate(i, i_line + 1))
                    number_entry[1].append(
                        Coordinate(i_char - number_length - 1, i_line)
                    )
                    numbers.append(number_entry)
                    number = ""

                if c != ".":
                    symbol_locations.append(Coordinate(i_char, i_line))
        if len(number) > 0:
            number_length = len(number)
            number_entry = (
                int(number),
                [
                    Coordinate(i_char, i_line),
                    Coordinate(i_char, i_line - 1),
                    Coordinate(i_char, i_line + 1),
                ],
            )
            for i in range(i_char - number_length - 1, i_char):
                number_entry[1].append(Coordinate(i, i_line - 1))
                number_entry[1].append(Coordinate(i, i_line + 1))
            number_entry[1].append(Coordinate(i_char - number_length - 1, i_line))
            numbers.append(number_entry)
            number = ""

    print(symbol_locations)

    print(numbers)
    adjacent_numbers = []

    for number, coordinates in numbers:
        if is_adjacent(coordinates, symbol_locations):
            adjacent_numbers.append(number)
            print(f"A {number}")
        else:
            print(f"N {number}")

    print(f"Sum of adjacent numbers: {sum(adjacent_numbers)}")

print(f"Elapsed time: {time.perf_counter() - start_time} s")
