import networkx as nx
from matplotlib import pyplot as plt
from tqdm import tqdm

from networkx.generators.lattice import grid_2d_graph
from rich import print

from utils.readers import GridReader


data_sources_1 = (
    # ("Test data", GridReader("input-test-1.txt").read()),
    ("Prod data", GridReader("input-1.txt").read()),
)
#
# data_sources_2 = (
#     ("Test data", GridReader("input-test-2.txt").read()),
#     ("Prod data", GridReader("input-1.txt").read()),
# )

def draw_graph(graph):
    labels = nx.get_node_attributes(graph, 'value')

    # plt.figure(figsize=(6, 6))
    # pos = {(x, y): (y, -x) for x, y in graph.nodes()}
    # nx.draw(graph, pos=pos,
    #         node_color='lightgreen',
    #         with_labels=True,
    #         # labels=labels,
    #         node_size=600)
    # nx.draw(graph, pos=pos,
    #         node_color='lightgreen',
    #         # with_labels=True,
    #         labels=labels,
    #         node_size=600)
    # plt.show()
    #
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_figheight(10)
    fig.set_figwidth(16)
    pos = {(x, y): (y, -x) for x, y in graph.nodes()}
    nx.draw(graph, pos=pos,
            ax=ax1,
            node_color='lightgreen',
            with_labels=True,
            # labels=labels,
            node_size=600)
    nx.draw(graph, pos=pos,
            ax=ax2,
            node_color='lightgreen',
            # with_labels=True,
            labels=labels,
            node_size=600)
    plt.show()

def create_graph(grid):
    print("Creating graph")
    len_ab = len(grid)
    len_or = len(grid[0])
    graph = grid_2d_graph(len_ab, len_or)

    for node in graph.nodes():
        x, y = node
        nx.set_node_attributes(graph, {node: grid[x][y]}, "value")

    graph.add_edges_from([
                         ((x, y), (x + 1, y + 1))
                         for x in range(len_ab - 1)
                         for y in range(len_or - 1)
                     ] + [
                         ((x + 1, y), (x, y + 1))
                         for x in range(len_ab - 1)
                         for y in range(len_or - 1)
                     ])

    print("Created graph")
    return graph

only_length_of_four_filter = lambda x: len(x) == 4

def compatible_nodes(graph, node_source, node_destination, values):
    if values[node_source] != "X":
        return False
    if values[node_destination] != "S":
        return False
    x_source, y_source = node_source
    x_destination, y_destination = node_destination

    if len(nx.shortest_path(graph, source=node_source, target=node_destination)) != 4:
        return False

    if x_source == x_destination:
        return True
    if x_destination == y_destination:
        return True
    # if abs(x_source - x_destination) == 0 and abs(y_source - y_destination) == 0:
    #     return True

    return True


def translate_path(path, values):
    return [values[path[i]] for i in range(4)]

def part1(grid):
    graph = create_graph(grid)
    values = nx.get_node_attributes(graph, "value")

    result = 0

    draw_graph(graph)

    for node_source in tqdm(graph.nodes()):
        # if values[node_source] == "X":
        #     for node_destination in graph.nodes():
            for node_destination in nx.dfs_preorder_nodes(graph, source=node_source, depth_limit=5):
                if not compatible_nodes(graph, node_source, node_destination, values):
                    continue
                # if values[node_destination] == "S":

                all_paths = list(nx.all_simple_paths(graph, node_source, node_destination, cutoff=4))
                all_paths_length_of_four = list(filter(only_length_of_four_filter, all_paths))
                if not all_paths_length_of_four:
                    continue

                for path in all_paths_length_of_four:
                    display_path = translate_path(path, values)
                    if display_path == ["X", "M", "A", "S"]:
                            result += 1

    return result


    # values = nx.get_node_attributes(graph, "value")
    # for node in graph.nodes:
    #     value = values[node]
    #     if value == "X":
    #
    #         i = 1
    #     i = 1




    # G = nx.petersen_graph()
    # subax1 = plt.subplot(121)
    # nx.draw(G, with_labels=True, font_weight='bold')
    # subax2 = plt.subplot(122)
    # nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
    # plt.show()

for data_source_name, data_source in data_sources_1:
    print(f"Day 1 - Result 1 - {data_source_name}: {part1(data_source)}")
#