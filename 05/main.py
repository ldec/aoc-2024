from math import floor
from typing import List

from rich import print

from utils.readers import FileReader


class SafetyManualReader(FileReader):
    """
    Implementation of a Safety Manual

    47|53
    97|13

    47,53,97,13
    """

    def read(self, *args, **kwargs) -> (List[List[int]], List[List[int]]):
        rules = []
        updates = []
        lines = super(SafetyManualReader, self).read().splitlines()
        for line in lines:
            if "|" in line:
                rules.append(list(map(int, line.split("|"))))
            if "," in line:
                updates.append(list(map(int, line.split(","))))

        rules = sorted(rules, key=lambda x: (x[0], x[1]))

        return rules, updates


data_sources_1 = (
    ("Test data", SafetyManualReader("input-test-1.txt").read()),
    ("Prod data", SafetyManualReader("input-1.txt").read()),
)


def check_rule(rule: List[int], update: List[int]) -> bool:
    if not (rule[0] in update and rule[1] in update):
        return True

    return update.index(rule[0]) < update.index(rule[1])


def get_update_middle_page(update: List[int]) -> int:
    assert len(update) % 2 == 1
    return update[floor(len(update) / 2)]


def check_part1(rules: List[List[int]], updates: List[List[int]]) -> (int, int):
    sum_of_middle_pages = 0
    for update in updates:
        update_valid = True
        for rule in rules:
            if not check_rule(rule, update):
                update_valid = False
                break
        if update_valid:
            sum_of_middle_pages += get_update_middle_page(update)

    return sum_of_middle_pages


def correct_update(update: List[int], rules: List[List[int]]) -> List[int]:
    for rule in rules:
        if not check_rule(rule, update):
            temp = update[update.index(rule[0])]
            update[update.index(rule[0])] = update[update.index(rule[1])]
            update[update.index(rule[1])] = temp

    return update


def check_part2(rules: List[List[int]], updates: List[List[int]]) -> (int, int):
    sum_of_middle_pages = 0

    for update in updates:
        update_valid = True
        for rule in rules:
            if not check_rule(rule, update):
                update_valid = False
                break
        if not update_valid:
            fixed_update = correct_update(update, rules)
            fixed_update = correct_update(fixed_update, rules)
            fixed_update = correct_update(fixed_update, rules)
            fixed_update = correct_update(fixed_update, rules)

            for rule in rules:
                assert check_rule(rule, fixed_update)
            sum_of_middle_pages += get_update_middle_page(fixed_update)

    return sum_of_middle_pages


for data_source_name, data_source in data_sources_1:
    print(f"Day 1 - Result 1 - {data_source_name}: {check_part1(*data_source)}")

for data_source_name, data_source in data_sources_1:
    print(f"Day 1 - Result 2 - {data_source_name}: {check_part2(*data_source)}")
