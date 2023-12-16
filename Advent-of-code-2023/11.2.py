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

matrix = [list(line.strip()) for line in data.strip().split()]

expanded_rows = None
expanded_cols = None

def expand(lines):
    rows = []
    for n, line in enumerate(lines):
        line = "".join(line)
        if re.match(rgx, line):
            rows.append(n)
    return set(rows)


expanded_rows = expand(matrix)

t_matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
expanded_cols = expand(t_matrix)

locs = dict()
p = 1
for r, rd in enumerate(matrix):
    # print("".join(rd))
    for c, cd in enumerate(rd):
        if cd == "#":
            locs[p] = (r, c)
            p += 1

dists = dict()
penalty = 2
penalty = 1000000

# print(locs)
for p, u in locs.items():
    for q, v in locs.items():
        if p >= q:
            continue

        h_dist = abs(v[1] - u[1])
        v_dist = abs(v[0] - u[0])

        for r in range(min([v[0], u[0]]), max([v[0], u[0]]) + 1):
            if r in expanded_rows:
                v_dist -= 1
                v_dist += penalty

        for r in range(min([v[1], u[1]]), max([v[1], u[1]]) + 1):
            if r in expanded_cols:
                h_dist -= 1
                h_dist += penalty

        dist = h_dist + v_dist
        cords = (p, q)
        if cords in dists:
            dists[cords] = min(dists[cords], dist)
        else:
            dists[cords] = dist

print(len(dists))
print(sum(dists.values()))
