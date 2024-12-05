import re
from typing import List, Optional

from rich import print

from utils.readers import GridReader


data_sources_1 = (
    ("Test data", GridReader("input-test-1.txt").read()),
    ("Prod data", GridReader("input-1.txt").read()),
)


def print_grid(grid):
    for row in grid:
        print(*row, sep=" ")

def get_case_or_none(grid: List[List[str]], x: int, y: int) -> Optional[str]:
    if x < 0 or y < 0:
        return None

    try:
        return grid[y][x]
    except:
        return None

def horizontal(grid: List[List[str]], x,y: int):
    word = [
        get_case_or_none(grid, x, y),
        get_case_or_none(grid, x+1, y),
        get_case_or_none(grid, x+2, y),
        get_case_or_none(grid, x+3, y),
    ]
    if not None in word:
        return [x, y, "h", word]
    return []

def vertical(grid: List[List[str]], x,y: int):
    word = [
        get_case_or_none(grid, x, y),
        get_case_or_none(grid, x, y+1),
        get_case_or_none(grid, x, y+2),
        get_case_or_none(grid, x, y+3),
    ]
    if not None in word:
        return [x, y, "v", word]
    return []

def diagonal_right(grid: List[List[str]], x,y: int):
    word = [
        get_case_or_none(grid, x, y),
        get_case_or_none(grid, x+1, y+1),
        get_case_or_none(grid, x+2, y+2),
        get_case_or_none(grid, x+3, y+3),
    ]
    if not None in word:
        return [x, y, "dr", word]
    return []

def diagonal_left(grid: List[List[str]], x,y: int):
    word = [
        get_case_or_none(grid, x, y),
        get_case_or_none(grid, x-1, y+1),
        get_case_or_none(grid, x-2, y+2),
        get_case_or_none(grid, x-3, y+3),
    ]
    if not None in word:
        return [x, y, "dl", word]
    return []


def part1(grid: List[List[str]]):
    words_complete = []
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            words_complete.append(horizontal(grid, x, y))
            words_complete.append(vertical(grid, x, y))
            words_complete.append(diagonal_right(grid, x, y))
            words_complete.append(diagonal_left(grid, x, y))

    found_words = [i for i in words_complete if i and i[3] in [["X", "M", "A", "S"], ["S", "A", "M", "X"]]]
    return len(found_words)

def diagonal_x(grid: List[List[str]], x,y: int):
    ul = get_case_or_none(grid, x-1, y-1)
    ur = get_case_or_none(grid, x+1, y-1)
    dl = get_case_or_none(grid, x-1, y+1)
    dr = get_case_or_none(grid, x+1, y+1)

    if ((ul == "M" and dr == "S") or (ul == "S" and dr == "M")) and \
            ((ur == "M" and dl =="S") or (ur == "S" and dl =="M")):
        return True

    return False

def part2(grid: List[List[str]]):
    result = 0
    # print_grid(grid)
    for x in range(len(grid[0])):
        for y in range(len(grid)):
                if grid[y][x] == "A":
                    if diagonal_x(grid, x, y):
                        result += 1

    return result

for data_source_name, data_source in data_sources_1:
    print(f"Day 1 - Result 1 - {data_source_name}: {part1(data_source)}")

for data_source_name, data_source in data_sources_1:
    print(f"Day 1 - Result 2 - {data_source_name}: {part2(data_source)}")