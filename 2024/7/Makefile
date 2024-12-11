# Add 'export COOKIE="session=<your session cookie here>"  to .envrc
# see https://www.reddit.com/r/adventofcode/comments/5idb41/wget_the_input_files/
PART2:=$(wildcard part2.py)
DIRNAME_FULL:=$(shell pwd)
YEAR:=$(shell dirname ${DIRNAME_FULL})
YEAR:=$(shell basename ${YEAR})
DAY:=$(shell basename ${DIRNAME_FULL})

PYTHON_COMMAND:=uv run python

ifeq ("${PART2}", "")
	FILENAME=part1.py
else
	FILENAME=part2.py
endif

.PHONY: solve, test, part2, solve2, test2, solve1, solve2
test:
	${PYTHON_COMMAND} ./${FILENAME} test.txt
solve: input.txt
	${PYTHON_COMMAND} ./${FILENAME} input.txt
solve1:
	${PYTHON_COMMAND} ./part1.py
test1:
	${PYTHON_COMMAND} ./part1.py test.txt
solve2:
	${PYTHON_COMMAND} ./part2.py
test2:
	${PYTHON_COMMAND} ./part2.py test.txt
part2: part2.py
part2.py:
	sed 's/Part 1/Part 2/g' part1.py > part2.py
	chmod a+x part2.py
	code -r part2.py
input.txt:
	$(eval URL:=https://adventofcode.com/${YEAR}/day/${DAY}/input)
	@echo curling ${URL} with ${COOKIE}
	@curl -s --cookie "${COOKIE}" ${URL} > input.txt