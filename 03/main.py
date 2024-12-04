import re

from rich import print

from utils.readers import FileReader

MUL_REGEX = re.compile(r"mul\((\d+,\d+)\)")
MUL_COMPLETE_REGEX = re.compile(r"(do)\(\)|(don)'t\(\)|mul\((\d+,\d+)\)")

data_sources_1 = (
    ("Test data", FileReader("input-test-1.txt").read()),
    ("Prod data", FileReader("input-1.txt").read()),
)

data_sources_2 = (
    ("Test data", FileReader("input-test-2.txt").read()),
    ("Prod data", FileReader("input-1.txt").read()),
)


def multiplication_parsing_and_execution(operation_raw):
    operation_raw_split = operation_raw.split(",")
    return int(operation_raw_split[0]) * int(operation_raw_split[1])


def execute_simple(program):
    result = 0
    operations_raw = MUL_REGEX.findall(program)
    for operation_raw in operations_raw:
        result += multiplication_parsing_and_execution(operation_raw)

    return result


def execute_with_do(program):
    result = 0
    matches = MUL_COMPLETE_REGEX.finditer(program)
    is_running = True
    for match in matches:
        operation_raw = match.group()
        if "mul" in operation_raw and is_running:
            operands = MUL_REGEX.findall(operation_raw)
            result += multiplication_parsing_and_execution(operands[0])
        if "don" in operation_raw:
            is_running = False
        if "do(" in operation_raw:
            is_running = True

    return result


for data_source_name, data_source in data_sources_1:
    print(f"Day 1 - Result 1 - {data_source_name}: {execute_simple(data_source)}")

for data_source_name, data_source in data_sources_2:
    print(f"Day 1 - Result 2 - {data_source_name}: {execute_with_do(data_source)}")
