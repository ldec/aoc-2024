from dataclasses import dataclass
from typing import List

from utils.readers import FileReader


@dataclass
class Block:
    is_empty_space: bool = False
    id: int = -1
    length: int = -1


def build_disk(raw_data: str, whole_file=False) -> (List[Block], int):
    disk = []
    current_block_id = 0
    for i, item in enumerate(raw_data):
        is_empty_space = i % 2 == 1
        block_id = -1
        if not is_empty_space:
            block_id = current_block_id
            current_block_id += 1

        if not whole_file:
            disk.extend(
                [Block(is_empty_space=is_empty_space, id=block_id)] * int(raw_data[i])
            )
        else:
            disk.append(
                Block(is_empty_space=is_empty_space, id=block_id, length=int(raw_data[i]))
            )

    return disk, current_block_id - 1


def display_disk(disk: List[Block], whole_file=False):
    result = ""
    if not whole_file:
        for block in disk:
            if block.is_empty_space:
                result += "."
            else:
                result += f"{block.id}"
    else:
        for block in disk:
            if block.is_empty_space:
                result += "." * block.length
            else:
                result += f"{block.id}" * block.length
    return result


def disk_checksum(disk: List[Block], whole_file=False):
    result = 0
    for i, block in enumerate(disk):
        if not block.is_empty_space:
            result += i * block.id

    return result


def part1(raw_data: str):
    disk, highest_file_id = build_disk(raw_data)

    negative_index = len(disk) -1
    for i in range(len(disk)):
        if not disk[i].is_empty_space:
            continue

        while disk[negative_index].is_empty_space:
            negative_index += -1

        if i >= negative_index:
            break

        disk[i] = disk[negative_index]
        disk[negative_index] = Block(is_empty_space=True)

    return disk_checksum(disk)

def part2(raw_data: str):
    disk, highest_file_id = build_disk(raw_data, whole_file=True)

    while highest_file_id > 0:
        negative_index = len(disk) - 1
        while disk[negative_index].is_empty_space or disk[negative_index].id > highest_file_id:
            negative_index += -1

        for i in range(len(disk)):
            if i > negative_index:
                break

            if not disk[i].is_empty_space:
                continue

            if disk[negative_index].length > disk[i].length:
                continue

            if disk[negative_index].length == disk[i].length:
                disk[i] = disk[negative_index]
                disk[negative_index] = Block(is_empty_space=True, length=disk[negative_index].length)
                break

            if disk[negative_index].length < disk[i].length:
                disk[i].length = disk[i].length - disk[negative_index].length
                disk.insert(i, disk[negative_index])
                disk[negative_index + 1] = Block(is_empty_space=True, length=disk[i].length)
                break

        highest_file_id -= 1

    new_disk = []
    for block in disk:
        new_disk.extend([Block(is_empty_space=block.is_empty_space, id=block.id)] * block.length)

    return disk_checksum(new_disk)


input_test_1 = FileReader("input-test-1.txt").read()
input_test_mini_1 = FileReader("input-mini-1.txt").read()
input_1 = FileReader("input-1.txt").read()

print(f"Day 9 - Result 1 - mini: {part1(input_test_mini_1)}")
print(f"Day 9 - Result 1 - test: {part1(input_test_1)}")
print(f"Day 9 - Result 1: {part1(input_1)}")

print(f"Day 9 - Result 2 - mini: {part2(input_test_mini_1)}")
print(f"Day 9 - Result 2 - test: {part2(input_test_1)}")
print(f"Day 9 - Result 2: {part2(input_1)}")
