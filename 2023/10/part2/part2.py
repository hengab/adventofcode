#!/usr/bin/env python

import sys
import time
import typing as typ
import logging
import dataclasses

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

logger = logging.getLogger(__name__)

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
logger.info("--------Part 2--------")

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
    # ·┌ ┐················
    #  └ ┘└

    symbols = {
        "L": "└",
        "J": "┘",
        "7": "┐",
        "F": "┌",
    }
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
            highlight = "\033[94m"
            end = "\033[0m"
            c = grid[column][row]
            line = f"{line}{symbols.get(c, c)}"
        print(f"|{line}|")

    print(f"+{top_and_bottom}+")


with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]


# grid = [["."] * len(lines) for _ in range(len(lines[0]))]
grid: typ.Dict[Coordinate, Node] = {}
start_node = None
ground_nodes: typ.Dict[Coordinate, Node] = {}
y = len(lines) - 1
for line in lines:
    for x in range(len(line)):
        node = Node(Coordinate(x, y), line[x])
        grid[node.coordinate] = node
        if line[x] == "S":
            start_node = node
        # if line[x] == ".":
        #     ground_nodes[node.coordinate] = node

        # grid[x][y] = line[x]

    y -= 1

print_map(Coordinate(0, 0), Coordinate(len(lines[0]) - 1, len(lines) - 1), grid)

N = Coordinate(0, 1)
NE = Coordinate(1, 1)
E = Coordinate(1, 0)
SE = Coordinate(1, -1)
S = Coordinate(0, -1)
SW = Coordinate(-1, -1)
W = Coordinate(-1, 0)
NW = Coordinate(-1, 1)

three_sixty = [N, NE, E, SE, S, SW, W, NW]
paths: typ.Dict[str, typ.List[Coordinate]] = {
    "|": [N, S],
    "-": [E, W],
    "L": [N, E],
    "J": [N, W],
    "7": [S, W],
    "F": [S, E],
    ".": [],
    "S": [],
}

side_one: typ.Dict[str, Coordinate] = {
    "|": W,
    "-": S,
    "L": S,
    "J": E,
    "7": N,
    "F": W,
    ".": [],
    "S": [],
}


sides = {
    "|": [d for d in three_sixty if d not in paths["|"]],
    "-": [d for d in three_sixty if d not in paths["-"]],
    "L": [d for d in three_sixty if d not in paths["L"]],
    "J": [d for d in three_sixty if d not in paths["J"]],
    "7": [d for d in three_sixty if d not in paths["7"]],
    "F": [d for d in three_sixty if d not in paths["F"]],
    ".": [],
    "S": [],
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
# ·┌ ┐················
#  └ ┘└
logger.debug(f"Starting nodes: {nodes_to_visit}")
logger.debug(f"len(nodes_to_visit): {len(nodes_to_visit)}")
# nodes_to_visit.popleft()
while nodes_to_visit:
    node: Node = nodes_to_visit.popleft()
    logger.debug(f"Visiting {node}")
    visited_nodes.append(node)
    for d in paths[node.shape]:
        candidate = grid[node.coordinate.move(d)]
        # logger.debug(f" Evaluating {candidate}")
        if candidate.min_distance is None:
            candidate.min_distance = node.min_distance + 1
            nodes_to_visit.append(candidate)

internal_nodes = []

pipe_part_score = {
    "L": 0.5,
    "F": -0.5,
    "7": 0.5,
    "J": -0.5,
}

for _, node in grid.items():
    # for _, node in ground_nodes.items():
    if node.min_distance is None:
        # This is a node not used by the pipe
        is_internal_node = True
        for direction in [N, S]:
            if is_internal_node:
                pipe_part_count = 0
                partial_pipe_part_count = 0
                candidate = node

                while candidate:
                    if (
                        candidate.min_distance is not None                        
                    ):
                        if candidate.shape == "S":
                            pipe_part_count = 1
                            partial_pipe_part_count = 0
                            break
                        elif candidate.shape == "-":
                            pipe_part_count += 1
                        else:
                            partial_pipe_part_count += pipe_part_score.get(candidate.shape, 0)
                        if node.coordinate == Coordinate(14, 6):
                            logger.debug(f"Node: {node} Direction {direction} - Candidate: {candidate} - pipe_part_count: {pipe_part_count} {paths[candidate.shape]} {direction in paths[candidate.shape]}")
                        
                    candidate = grid.get(candidate.coordinate.move(direction))
                if (pipe_part_count + abs(partial_pipe_part_count)) % 2 == 0:
                    is_internal_node = False
                    # node.shape = "O"

        if is_internal_node:
            internal_nodes.append(node)
            node.shape = "I"
        else:
            node.shape = "O"

# grid[Coordinate(14, 6)].shape = "X"

max_distance = 0
for node in visited_nodes:
    max_distance = max(max_distance, node.min_distance)

logger.info(f"Enclosed Tiles: {len(internal_nodes)}")
logger.info(f"Elapsed time: {time.perf_counter() - start_time} s")

print_map(Coordinate(0, 0), Coordinate(len(lines[0]) - 1, len(lines) - 1), grid)
