import re

data = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
data = open('11.txt').read()

rgx = re.compile(r"^\.+$")

lines = [list(line.strip()) for line in data.strip().split()]


def expand(lines):
    matrix = []
    for line in lines:
        line = "".join(line)
        if re.match(rgx, line):
            matrix.append(list(line))
        matrix.append(list(line))
    return matrix


matrix = expand(lines)
t_matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
t_matrix = expand(t_matrix)
matrix = [
    [t_matrix[j][i] for j in range(len(t_matrix))] for i in range(len(t_matrix[0]))
]


locs = dict()
p = 1
for r, rd in enumerate(matrix):
    # print("".join(rd))
    for c, cd in enumerate(rd):
        if cd == "#":
            locs[p] =(r, c)
            p += 1

dists = dict()

# print(locs)
for p, u in locs.items():
    for q, v in locs.items():
        if p >= q:
            continue

        dist = abs(v[1] - u[1]) + abs(v[0] - u[0])
        cords = (p, q)
        if cords in dists:
            dists[cords] = min(dists[cords], dist)
        else:
            dists[cords] = dist

print(len(dists))
print(sum(dists.values()))