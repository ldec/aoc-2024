import timeit

import numpy as np


def compareA():
    list_b = [(6, 7), (6, 8), (5, 8), (4, 8), (3, 8), (6, 7)]
    list_s = [(6, 7), (6, 8)]

    np_list_b = np.array(list_b, dtype="i,i")
    start_indexes = np.where(np_list_b == np.array([list_s[0]], dtype="i,i"))[0]

    for index in start_indexes:
        if list_b[index : index + len(list_s)] == list_s:
            return True


def compareB():
    list_b = [(6, 7), (6, 8), (5, 8), (4, 8), (3, 8), (6, 7)]
    list_s = [(6, 7), (6, 8)]

    np_list_b = np.array(list_b, dtype="i,i")
    np_list_s = np.array(list_s, dtype="i,i")

    for i in range(len(np_list_b)):
        if np.array_equal(np_list_s, np_list_b[i : i + len(np_list_s)]):
            return True
    return False


def compareC():
    list_b = [(6, 7), (6, 8), (5, 8), (4, 8), (3, 8), (6, 7)]
    list_s = [(6, 7), (6, 8)]

    b_str = " ".join(map(str, list_b))
    s_str = " ".join(map(str, list_s))
    return s_str in b_str


if __name__ == "__main__":
    print(timeit.Timer(compareA).timeit(number=100000))
    print(timeit.Timer(compareB).timeit(number=100000))
    print(timeit.Timer(compareC).timeit(number=100000))

    # Results:
    # 1.5294703990002745
    # 1.6728675790000125
    # 0.2062916739996581
