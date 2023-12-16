from copy import deepcopy
from tqdm import tqdm

data = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
data = open("14.txt").read()


transpose = lambda m: [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]


def get_new(matrix):
    matrix = deepcopy(matrix)
    new_matrix = []
    for row in matrix:
        idx = 0
        row = list(row)

        for ci, c in enumerate(row):
            # if # do nothing just increment
            if c == "#":
                idx = ci + 1
            # if a ball move to idx
            if c == "O":
                if ci > idx:
                    # print("move", ci, "to", idx)
                    row[idx] = "O"
                    row[ci] = "."
                    for x in range(idx + 1, len(row)):
                        if row[x] == ".":
                            idx = x
                            break
                else:
                    idx += 1
        new_matrix.append(row)
    return new_matrix


def rotate_anti_lockwise(matrix, times=1):
    matrix = matrix
    for _ in range(times):
        matrix = list(reversed(list(zip(*matrix))))
    return matrix


def score(matrix):
    total = 0
    for row in matrix:
        for ci, c in enumerate(row):
            total += (len(row) - ci) if c == "O" else 0
    return total


def pprint(matrix):
    return "\n".join(["".join(line) for line in matrix])


def cycle(data):
    # do north
    matrix = transpose(data)
    matrix = get_new(matrix)
    matrix = transpose(matrix)
    # do west
    matrix = rotate_anti_lockwise(matrix, 3)
    matrix = transpose(matrix)
    matrix = get_new(matrix)
    matrix = transpose(matrix)
    matrix = rotate_anti_lockwise(matrix, 1)
    # do south
    matrix = rotate_anti_lockwise(matrix, 2)
    matrix = transpose(matrix)
    matrix = get_new(matrix)
    matrix = transpose(matrix)
    matrix = rotate_anti_lockwise(matrix, 2)
    # do east
    matrix = rotate_anti_lockwise(matrix, 1)
    matrix = transpose(matrix)
    matrix = get_new(matrix)
    matrix = transpose(matrix)
    matrix = rotate_anti_lockwise(matrix, 3)

    return matrix


m = [list(x) for x in data.strip().split("\n")]
m_cache = []
score_cache = []
repeat_index = 0
period = None
for x in range(1, 1000000000):
    m = cycle(m)
    mstr = "\n".join(["".join(line) for line in m])
    if mstr in m_cache:
        period = x
        repeat_index = m_cache.index(mstr)
        break
    m_cache.append(mstr)
    score_cache.append(score(transpose(m)))

harminic_region = 1000000000 - repeat_index
repeat_scores = score_cache[repeat_index:]
score_pos = harminic_region % len(repeat_scores)
print(repeat_scores[score_pos - 1])
