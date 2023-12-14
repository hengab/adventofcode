#!/usr/bin/env python

import sys
import time
import typing as typ
import logging
import dataclasses

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

logger = logging.getLogger(__name__)

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
logger.info("--------Part 1--------")

start_time = time.perf_counter()

X = int
Y = int


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

    def move(self, direction: "Coordinate") -> "Coordinate":
        return Coordinate(self.x + direction.x, self.y + direction.y)


@dataclasses.dataclass
class Node(object):
    coordinate: Coordinate
    shape: str
    min_distance = None


def print_map(
    min_coordinate: Coordinate,
    max_coodinate: Coordinate,
    nodes: typ.Dict[Coordinate, Node],
) -> None:
    default_symbol = "."
    rows = max_coodinate.y - min_coordinate.y + 1
    columns = max_coodinate.x - min_coordinate.x + 1
    grid = [[default_symbol for _ in range(rows)] for _ in range(columns)]

    # Assign values to the non-default cells
    for coordinate, frequency in nodes.items():
        grid[coordinate.x - min_coordinate.x][coordinate.y - min_coordinate.y] = str(
            frequency.shape
        )

    top_and_bottom = "-" * columns
    print(f"+{top_and_bottom}+")
    for row in range(rows - 1, -1, -1):
        line = ""
        for column in range(columns):
            line = f"{line}{grid[column][row]}"
        print(f"|{line}|")

    print(f"+{top_and_bottom}+")


with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]


# grid = [["."] * len(lines) for _ in range(len(lines[0]))]
grid: typ.Dict[Coordinate, Node] = {}
start_node = None
y = len(lines) - 1
for line in lines:
    for x in range(len(line)):
        node = Node(Coordinate(x, y), line[x])
        grid[node.coordinate] = node
        if line[x] == "S":
            start_node = node

        # grid[x][y] = line[x]

    y -= 1

# print_map(Coordinate(0, 0), Coordinate(4, 4), grid)

N = Coordinate(0, 1)
E = Coordinate(1, 0)
S = Coordinate(0, -1)
W = Coordinate(-1, 0)
paths: typ.Dict[str, typ.List[Coordinate]] = {
    "|": [N, S],
    "-": [E, W],
    "L": [N, E],
    "J": [N, W],
    "7": [S, W],
    "F": [S, E],
    ".": [],
    "S": []
}

import collections

nodes_to_visit: collections.deque = collections.deque()
visited_nodes: typ.List[Node] = []
# Create initial list of nodes to visit
for direction in [N, E, S, W]:
    node = grid[start_node.coordinate.move(direction)]
    for d in paths[node.shape]:
        if node.coordinate.move(d) == start_node.coordinate:
            node.min_distance = 1
            nodes_to_visit.append(node)

logger.debug(f"Starting nodes: {nodes_to_visit}")

while nodes_to_visit:    
    node: Node = nodes_to_visit.popleft()
    logger.debug(f"Visiting {node}")
    visited_nodes.append(node)
    for d in paths[node.shape]:
        candidate = grid[node.coordinate.move(d)]
        logger.debug(f" Evaluating {candidate}")
        if candidate.min_distance is None:
            candidate.min_distance = node.min_distance + 1
            nodes_to_visit.append(candidate)

max_distance = 0
for node in visited_nodes:
    max_distance = max(max_distance, node.min_distance)

logger.info(f"Max distance: {max_distance}")
logger.info(f"Elapsed time: {time.perf_counter() - start_time} s")
