#!/usr/bin/env python

import sys
import time
import typing as typ
import logging
import dataclasses

logging.basicConfig(format="%(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)

input_file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
logger.info("--------Part 2--------")

start_time = time.perf_counter()


@dataclasses.dataclass
class Label(object):
    text: str
    lens: int

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Label):
            return self.text == __value.text
        elif isinstance(__value, str):
            return self.text == __value

        return False


with open(input_file_name) as fh:
    lines = [line.strip() for line in fh.readlines()]

one_liner = "".join(lines)
steps = one_liner.split(",")


def hash(value: str):
    current_value = 0
    for c in value:
        ascii_value = ord(c)
        current_value += ascii_value
        current_value *= 17
        current_value = current_value % 256

    return current_value


boxes: typ.List[typ.List[Label]] = [[] for _ in range(256)]

sequence_value = 0
for step in steps:
    sign = "=" if step.find("=") != -1 else "-"
    label = Label(text=step.split(sign)[0], lens=0)
    box_index = hash(label.text)

    if sign == "-":
        if label in boxes[box_index]:
            boxes[box_index].remove(label)
    elif sign == "=":
        label.lens = int(step.split(sign)[1])
        box = boxes[box_index]
        label_found = False
        for l in box:
            if l == label:
                # replace
                l.lens = label.lens
                label_found = True
                break

        if not label_found:
            box.append(label)

    logger.debug(f"After {step}")
    for box_index in range(len(boxes)):
        if boxes[box_index]:
            logger.debug(f"Box {box_index}: {[lens for lens in boxes[box_index]]}")

total_focal_power = 0
for box_index in range(len(boxes)):
    box_value = box_index + 1
    for slot_index in range(len(boxes[box_index])):
        slot_value = slot_index + 1
        box = boxes[box_index][slot_index]
        focal_length = int(boxes[box_index][slot_index].lens)

        focal_power = box_value * slot_value * focal_length
        logger.debug(
            f"{box.text}: {box_value} (box {box_index}) * {slot_value} ({slot_value} slot) * {focal_length} (focal length) = {focal_power}"
        )

        total_focal_power += int(focal_power)


logger.info(f"Value = {total_focal_power}")
logger.info(f"Elapsed time: {time.perf_counter() - start_time} s")
