from collections import defaultdict
from copy import deepcopy

data = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""


class Vertex:
    def __init__(self, cost, position) -> None:
        self.cost: int = cost
        self.position: tuple = position
        self.neighbours: dict[str, "Vertex"] = dict()
        self.distance = {
            "t": float("inf"),
            "l": float("inf"),
            "r": float("inf"),
            "b": float("inf"),
        }
        self.distance = float("inf")
        self.parent = None
        self.direction_travelled = defaultdict(int)
        self.parent: "Vertex" = None


direction_map = {"t": "b", "b": "t", "l": "r", "r": "l"}


def is_valid(r, c, matrix: list[list[str]]):
    return not (r < 0 or c < 0 or r >= len(matrix) or c >= len(matrix[0]))


vertices: list[list[Vertex]] = [
    [None for _ in list(line)] for line in data.strip().split("\n")
]
for r, line in enumerate(data.strip().split()):
    for c, d in enumerate(line):
        v = Vertex(int(d), (r, c))
        vertices[r][c] = v


for r, vl in enumerate(vertices):
    for c, v in enumerate(vl):
        # top
        ur, uc = r - 1, c
        if is_valid(ur, uc, vertices):
            v.neighbours["t"] = vertices[ur][uc]
            vertices[ur][uc].neighbours["b"] = v
        # bottom
        dr, dc = r + 1, c
        if is_valid(dr, dc, vertices):
            v.neighbours["b"] = vertices[dr][dc]
            vertices[dr][dc].neighbours["t"] = v
        # right
        rr, rc = r, c + 1
        if is_valid(rr, rc, vertices):
            v.neighbours["r"] = vertices[rr][rc]
            vertices[rr][rc].neighbours["l"] = v
        # left
        lr, lc = r, c - 1
        if is_valid(lr, lc, vertices):
            v.neighbours["l"] = vertices[lr][lc]
            vertices[lr][lc].neighbours["r"] = v


queue: list[Vertex] = []

for vl in vertices:
    for v in vl:
        queue.append(v)

queue[0].distance = {k: 0 for k in "trlb"}
# queue[0].distance = 0

# solve the distances for each direction.
while len(queue) > 0:
    # solve for each direction
    for ddd in "trlb":
        u: Vertex = min(queue, key=lambda x: x.distance[ddd])
        print(u.position, u.distance)
        queue.remove(u)

        for direction in "trlb":
            if direction in u.neighbours and u.neighbours[direction] in queue:
                n = u.neighbours[direction]
                alt = n.cost + u.distance

                if alt < n.distance and u.direction_travelled[direction] + 1 <= 3:
                    n.distance = alt
                    n.direction_travelled[direction] = u.direction_travelled[direction] + 1
                    n.parent = u

print(vertices[-1][-1].__dict__)
matrix = [["."] * len(line) for line in data.strip().split()]

p = vertices[-1][-1]
matrix[p.position[0]][p.position[1]] = "#"
while p := p.parent:
    matrix[p.position[0]][p.position[1]] = "#"

print("\n".join(["".join(line) for line in matrix]))
