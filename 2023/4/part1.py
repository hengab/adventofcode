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


def score_card(winning_numbers: typ.List[int], my_numbers: typ.List[int]) -> int:
    next_score = 1
    score = 0
    for number in my_numbers:
        # print(f"Evaluating {number}")
        if number in winning_numbers:
            # print(f"{number} scores {next_score} points")
            score += next_score
            next_score = score

    return score


with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]

    score = 0
    for line in lines:
        card, line = line.split(":")
        winning_numbers_line, my_numbers_line = line.split("|")
        winning_numbers = winning_numbers_line.split()
        my_numbers = my_numbers_line.split()

        card_score = score_card(winning_numbers, my_numbers)
        score += card_score

        logger.debug(f"{card} worth {card_score} for a total of {score}")

    logger.info(f"Total Score: {score}")
logger.info(f"Elapsed time: {time.perf_counter() - start_time} s")
