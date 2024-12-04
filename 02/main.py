from copy import copy, deepcopy
from typing import List

from rich import print

from utils.readers import SpaceDelimitedColumnFileReader
from collections import Counter

data_sources_1 = (
    ("Test data", SpaceDelimitedColumnFileReader("input-test-1.txt").read(type_to_cast=int)),
    ("Prod data", SpaceDelimitedColumnFileReader("input-1.txt").read(type_to_cast=int)),
)


def is_report_safe(report: List[int]):
    if report[0] - report[1] > 0:
        is_increasing = False
    else:
        is_increasing = True

    for i in range(len(report)):
        if i < len(report) - 1:
            if report[i] == report[i+1]:
                return False

            if abs(report[i] - report[i+1]) > 3:
                return False

            if report[i] - report[i+1] > 0 and is_increasing:
                return False

            if report[i] - report[i+1] < 0 and not is_increasing:
                return False

    return True


def is_report_safe_with_dampener(report: List[int]):
    for i in range(len(report)):
        cleaned_report = deepcopy(report)
        del cleaned_report[i]
        if is_report_safe(cleaned_report):
            return True
    return False

def analyse_reports(reports: List[List[int]], dampener:bool=False):
    result = 0
    for report in reports:
        if not dampener:
            if is_report_safe(report):
                result += 1
        else:
            if is_report_safe(report):
                result += 1
            elif is_report_safe_with_dampener(report):
                result += 1

    return result


for data_source_name, data_source in data_sources_1:
    print(
        f"Day 1 - Result 1 - {data_source_name}: {analyse_reports(data_source)}"
    )

for data_source_name, data_source in data_sources_1:
    print(
        f"Day 1 - Result 2 - {data_source_name}: {analyse_reports(data_source, dampener=True)}"
    )
