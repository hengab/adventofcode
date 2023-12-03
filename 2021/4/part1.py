#!/usr/bin/env python

import sys
import time
import typing as typ

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
print("--------Part 1--------")

start_time = time.perf_counter()


Value = int
Marked = bool


def mark_boards(
    drawn_number: int,
    boards: typ.List[typ.List[typ.List[typ.Tuple[Value, Marked]]]],
) -> typ.List[typ.List[typ.List[typ.Tuple[Value, Marked]]]]:
    for board in boards:
        for x, row in enumerate(board):
            for y, content in enumerate(row):
                if content[0] == drawn_number:
                    board[x][y] = (drawn_number, True)

    return boards


def evaluate_bingo(
    boards: typ.List[typ.List[typ.List[typ.Tuple[Value, Marked]]]]
    # boards: typ.List[typ.Dict[typ.Tuple[X, Y], typ.Type(Value, Marked)]]
) -> typ.List[typ.List[typ.List[typ.Tuple[Value, Marked]]]]:
    bingo_boards: typ.List[typ.List[typ.List[typ.Tuple[Value, Marked]]]] = []

    for board in boards:
        for row in board:
            if all([v[1] for v in row]):
                bingo_boards.append(board)

    return bingo_boards


def calculate_bingo_score(
    boards: typ.List[typ.List[typ.List[typ.Tuple[Value, Marked]]]], last_number: int
) -> int:
    assert len(boards) == 1, "No idea what to do now"

    total = 0
    for row in boards[0]:
        for column in row:
            if not column[1]:
                total += column[0]

    return total * last_number


def play_bingo(
    drawn_numbers: typ.List[int],
    boards: typ.List[typ.List[typ.List[typ.Tuple[Value, Marked]]]],
) -> int:
    for number in drawn_numbers:
        boards = mark_boards(number, boards)
        bingo_boards = evaluate_bingo(boards)

        if bingo_boards:
            return calculate_bingo_score(bingo_boards, number)

    assert False, "No bingos"


with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]
    drawn_numbers: typ.List[int] = []
    boards: typ.List[typ.List[typ.List[typ.Tuple[Value, Marked]]]] = []
    current_board = []
    # current_board_row = 0
    for line in lines:
        how = ""
        what = None
        line = line.strip()
        if not drawn_numbers:
            # drawn numbers
            how = "drawn numbers"
            drawn_numbers = [int(n) for n in line.split(",")]
        elif line:
            # board row
            how = "board row"
            new_row = [(int(value), False) for value in line.split()]
            current_board.append(new_row)
            what = new_row
            # row = {
            #     (current_board_row, i): (int(value), False)
            #     for i, value in enumerate(line.split())
            # }
            # what = str(row)
            # current_board = {**current_board, **row}
            # current_board_row += 1
        else:
            # new board
            how = "new board"
            if current_board:
                print(f"Appending {current_board}")
                boards.append(current_board)
            current_board = []
            # current_board_row = 0

        print(f"Processed {line} as {how} - {what}")
        print(current_board)

    if current_board:
        boards.append(current_board)
    print(",".join(map(str, drawn_numbers)))
    print(len(boards))
    print(boards)

    print(play_bingo(drawn_numbers, boards))

print(f"Elapsed time: {time.perf_counter() - start_time} s")
