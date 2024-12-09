from math import ceil, floor

from utils.data_structures import Grid
from utils.readers import GridReaderv2


def find_antinodes(grid, node1, node2, harmonics=False):
    x1, y1 = node1
    x2, y2 = node2
    
    m = (y2 - y1) / (x2 - x1)
    b = -(m*x1-y1)
    print(f"Node1: {node1}, Node2: {node2} - m {m}, b {b}")

    if not harmonics:
        anti_node_1_x = round(x1*2 - x2)
        anti_node_1_y = round(m*anti_node_1_x + b)

        anti_node_2_x = round(x2*2 - x1)
        anti_node_2_y = round(m*anti_node_2_x + b)
        return (anti_node_1_x, anti_node_1_y), (anti_node_2_x, anti_node_2_y)

    antinodes = []
    for x in range(grid.width+1):
        y = m*x + b
        if floor(y) == y or ceil(y) - y <= 0.0001 or  y - floor(y) <= 0.0001:
            antinodes.append((x, round(y)))

    return antinodes


def get_antinodes(grid:Grid, harmonics=False):
    grid_display = Grid(grid.width, grid.height)
    print(grid.render(fmt="ultra_compact", headers=False))

    all_antinodes = set()
    for frequency, antennas in grid.item_map.items():
        if frequency != "#" and len(antennas) > 1:
            print(f"Frequency {frequency}")
            for antenna in antennas[:-1]:
                for other_antenna in antennas:
                    if not antenna == other_antenna:
                        antinodes = find_antinodes(grid, antenna, other_antenna, harmonics=harmonics)
                        for antinode in antinodes:
                            if not grid.out_of_bound(*antinode):
                                all_antinodes.add(antinode)

                                grid_display.set(*antinode, "#")

    return len(all_antinodes)

input_mini_1 = GridReaderv2("input-mini-1.txt").read()
input_mini_2 = GridReaderv2("input-mini-2.txt").read()
input_test_1 = GridReaderv2("input-test-1.txt").read()
input_1 = GridReaderv2("input-1.txt").read()

print(f"Day 1 - Result 1 - mini: {get_antinodes(input_mini_1)}")
print(f"Day 1 - Result 1 - test: {get_antinodes(input_test_1)}")
print(f"Day 1 - Result 1: {get_antinodes(input_1)}")

print(f"Day 1 - Result 2 - mini: {get_antinodes(input_mini_2, harmonics=True)}")
print(f"Day 1 - Result 2 - test: {get_antinodes(input_test_1, harmonics=True)}")
print(f"Day 1 - Result 2: {get_antinodes(input_1, harmonics=True)}")

