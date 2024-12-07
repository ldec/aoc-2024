import re
from itertools import product

from tqdm import tqdm

from utils.readers import FileReader


class OperationsReader(FileReader):
    """
    Implementation of an operation list reader
    """

    def read(self, *args, **kwargs):
        lines = super(OperationsReader, self).read().splitlines()
        operations = []
        for line in lines:
            result, values = line.split(":")
            result = int(result)

            values = list(
                map(str, [value.strip() for value in values.split(" ") if value])
            )

            operations.append((result, values))

        return operations


OPERATION_REGEX = re.compile(r"(\d+[+*|]+\d+)")


def custom_eval(operation, goal):
    while True:
        current_operation = OPERATION_REGEX.search(operation)
        if current_operation is None:
            return int(operation)

        if "|" in current_operation.groups()[0]:
            current_operation_result = int(
                current_operation.groups()[0].replace("||", "")
            )
        else:
            current_operation_result = eval(current_operation.groups()[0])

        if current_operation_result > goal:
            return -1

        operation = OPERATION_REGEX.sub(
            str(current_operation_result), operation, count=1
        )


def find_total_calibration(operations, new_operator=False):
    operators = ["*", "+"]
    if new_operator:
        operators.append("||")

    result = 0
    for operation in tqdm(operations):
        operation_result, operation_values = operation

        if len(operation_values) >= 3:
            possible_operations_per_values = []
            for value in operation_values[:-1]:
                possible_operations_per_value = list(product([value], operators))
                possible_operations_per_values.append(
                    list(map(lambda x: "".join(x), possible_operations_per_value))
                )

            possible_operations = list(
                product(*possible_operations_per_values, repeat=1)
            )
            possible_operations_str = list(
                map(lambda x: "".join(x) + operation_values[-1], possible_operations)
            )
        else:
            possible_operations_str = [
                f"{operation_values[0]}+{operation_values[1]}",
                f"{operation_values[0]}*{operation_values[1]}",
            ]
            if new_operator:
                possible_operations_str.append(
                    f"{operation_values[0]}||{operation_values[1]}"
                )

        for possible_operation_str in possible_operations_str:
            if (
                custom_eval(possible_operation_str, operation_result)
                == operation_result
            ):
                result += operation_result
                break

    return result


data_sources_1 = (
    ("Test data", OperationsReader("input-test-1.txt").read()),
    ("Prod data", OperationsReader("input-1.txt").read()),
)

for data_source_name, data_source in data_sources_1:
    print(
        f"Day 1 - Result 1 - {data_source_name}: {find_total_calibration(data_source)}"
    )

for data_source_name, data_source in data_sources_1:
    print(
        f"Day 1 - Result 2 - {data_source_name}: {find_total_calibration(data_source, new_operator=True)}"
    )
