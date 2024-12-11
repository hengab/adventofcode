#!/usr/bin/env python

import sys
import time
import typing as typ
import logging

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

logger = logging.getLogger(__name__)

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
logger.info("--------Part 1--------")

start_time = time.perf_counter()

def add(x: int, y: int) -> int:
    return x + y

def mult(x: int, y: int) -> int:
    return x * y

def operate(answer: int, previous_results: typ.List[int], operand: int) -> typ.List[int]:
    results = []
    for previous_result in previous_results:
        for operator in operators:
            result = operator(previous_result, operand)
            if result <= answer:
                results.append(operator(previous_result, operand))

    return results

operators = [add, mult]
possible_results = 0

with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]
    for line in lines:
        ans, rest = line.split(":")
        answer = int(ans)
        operands = list(map(lambda x: int(x), rest.split()))
        print(f"{line} - {answer} - {operands}")

        results = [0]
        for operand in operands:
            results = operate(answer, results, operand)

        print(results)
        if answer in results:
            possible_results += answer
            print(f"Answer in results - {possible_results}")

print(f"Result: {possible_results}")
logger.info(f"Elapsed time: {time.perf_counter() - start_time} s")