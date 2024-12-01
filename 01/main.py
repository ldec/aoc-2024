from rich import print

from utils.readers import SpaceDelimitedColumnFileReader
from collections import Counter

data_sources_1 = (
    ("Test data", SpaceDelimitedColumnFileReader("input-test-1.txt").read(type_to_cast=int)),
    ("Prod data", SpaceDelimitedColumnFileReader("input-1.txt").read(type_to_cast=int)),
)


def columns_to_list(data):
    c1 = sorted([i[0] for i in data])
    c2 = sorted([i[1] for i in data])

    assert len(c1) == len(c2)

    return [c1, c2]

def compute_distance(data):
    data = columns_to_list(data)

    return sum([abs(i - j) for i,j in zip(data[0], data[1])])

def compute_similarity(data):
    data = columns_to_list(data)
    counter = Counter(data[1])

    return sum([i * counter[i] for i in data[0]])


for data_source_name, data_source in data_sources_1:
    print(
        f"Day 1 - Result 1 - {data_source_name}: {compute_distance(data_source)}"
    )

for data_source_name, data_source in data_sources_1:
    print(
        f"Day 1 - Result 2 - {data_source_name}: {compute_similarity(data_source)}"
    )
