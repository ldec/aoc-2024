from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple

from rich import print
from tqdm import tqdm

from utils.data_structures import Grid
from utils.readers import FileReader

TRAIL_LENGTH = 3


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4


@dataclass
class Guard:
    x: int = -1
    y: int = -1
    starting_x: int = -1
    starting_y: int = -1

    facing: Direction = Direction.NORTH

    visited_cases: List[Tuple[int, int]] = field(default_factory=list)
    visited_cases_str: str = ""
    trail: List[Tuple[int, int]] = field(default_factory=list)

    left_the_grid: bool = False

    @property
    def starting_position(self) -> Tuple[int, int]:
        return self.starting_x, self.starting_y

    # Grid data structure is oon quadrant four
    def get_next_position(self, step=1):
        if self.facing == Direction.NORTH:
            return self.x, self.y - step
        if self.facing == Direction.SOUTH:
            return self.x, self.y + step
        if self.facing == Direction.EAST:
            return self.x + step, self.y
        if self.facing == Direction.WEST:
            return self.x - step, self.y

    def go_to_next_position(self, grid: Grid):
        x, y = self.get_next_position()

        if not grid.get(x, y) in ["#", "O"]:
            self.visited_cases.append((x, y))
            self.x = x
            self.y = y

            if len(self.visited_cases) >= TRAIL_LENGTH:
                self.visited_cases_str = f"{self.visited_cases_str}) ({x}, {y}"

            if len(self.trail) == TRAIL_LENGTH:
                del self.trail[0]
            self.trail.append((x, y))

    def turn(self):
        if self.facing == Direction.NORTH:
            self.facing = Direction.EAST
        elif self.facing == Direction.EAST:
            self.facing = Direction.SOUTH
        elif self.facing == Direction.SOUTH:
            self.facing = Direction.WEST
        elif self.facing == Direction.WEST:
            self.facing = Direction.NORTH


class GuardMapReader(FileReader):
    """
    Implementation of a Guard Map
    """

    def read(self, *args, **kwargs) -> (List[List[int]], List[List[int]]):
        lines = super(GuardMapReader, self).read().splitlines()
        grid = Grid(len(lines[0]), len(lines))
        guard = None
        for y in range(len(lines)):
            line = list(lines[y])
            for x in range(len(line)):
                case = lines[y][x]
                if case == "^":
                    guard = Guard(
                        x=x,
                        starting_x=x,
                        y=y,
                        starting_y=y,
                        visited_cases=[(x, y)],
                        facing=Direction.NORTH,
                    )
                    case = "|"
                grid.set(x, y, case)

        return grid, guard


def is_sublist(list_b: List[Tuple[int, int]], list_s: List[Tuple[int, int]]):
    b_str = " ".join(map(str, list_b))
    s_str = " ".join(map(str, list_s))
    return s_str in b_str


def set_case_render(grid: Grid, position: Tuple[int, int], guard: Guard):
    if position == guard.starting_position:
        return
    if grid.get(*position) == ".":
        if guard.facing in [Direction.NORTH, Direction.SOUTH]:
            grid.set(*position, "|")
        if guard.facing in [Direction.EAST, Direction.WEST]:
            grid.set(*position, "-")

    if grid.get(*position) == "|":
        if guard.facing in [Direction.EAST, Direction.WEST]:
            grid.set(*position, "+")

    if grid.get(*position) == "-":
        if guard.facing in [Direction.NORTH, Direction.SOUTH]:
            grid.set(*position, "+")


def create_path(
    grid: Grid, guard: Guard, enable_loop: bool = False
) -> (Grid, Guard, bool):
    while True:
        next_position = guard.get_next_position()
        if grid.out_of_bound(*next_position):
            guard.left_the_grid = True
            return grid, guard, False

        if enable_loop:
            if (
                len(guard.trail) == TRAIL_LENGTH
                and len(guard.visited_cases) > 2 * TRAIL_LENGTH
            ):
                trail_str = " ".join(map(str, guard.trail))
                match = trail_str in guard.visited_cases_str
                if match:
                    return grid, guard, True

        if grid.get(*next_position) == "#" or grid.get(*next_position) == "O":
            guard.turn()
            grid.set(guard.x, guard.y, "+")

        next_position = guard.get_next_position()
        set_case_render(grid, next_position, guard)
        guard.go_to_next_position(grid)


def part1(grid: Grid, guard: Guard):
    grid_with_path, guard, _ = create_path(grid, guard)
    return grid_with_path.count("X")


def part2(grid: Grid, guard: Guard):
    grid_with_initial_path, guard_with_initial_path, _ = create_path(
        deepcopy(grid), deepcopy(guard)
    )
    loop_count = 0
    for initial_path_visited_case in tqdm(set(guard_with_initial_path.visited_cases)):
        if initial_path_visited_case != guard.starting_position:
            new_grid = deepcopy(grid)
            new_guard = deepcopy(guard)

            new_grid.set(*initial_path_visited_case, "O")
            new_grid_with_path, new_guard, loop = create_path(
                new_grid, new_guard, enable_loop=True
            )
            if loop:
                loop_count += 1

    return loop_count


data_sources_1 = (
    # ("Test data", GuardMapReader("input-test-1.txt").read()),
    ("Prod data", GuardMapReader("input-1.txt").read()),
)

# for data_source_name, data_source in data_sources_1:
#     print(f"Day 1 - Result 1 - {data_source_name}: {part1(*deepcopy(data_source))}")

for data_source_name, data_source in data_sources_1:
    print(f"Day 1 - Result 2 - {data_source_name}: {part2(*data_source)}")
