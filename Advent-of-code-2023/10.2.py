from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from tqdm import tqdm

data = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

data = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

data = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

data = open("10.txt").read()


def pprint(m):
    for x in m:
        print("".join([f"{i:>3}" for i in x]))


matrix = [list(x) for x in data.strip().split("\n")]
matrix_copy = [list(x) for x in data.strip().split("\n")]
start = None


class Node:
    def __init__(self, neighbours, position, kind) -> None:
        self.neighbours: set = neighbours
        self.value: int = -1
        self.kind: str = kind
        self.position: tuple = position
        self.allow: set[str] = set()
        self.next = set()


nodes: dict[tuple, Node] = dict()

# init nodes
for r, rd in enumerate(matrix):
    for c, cd in enumerate(rd):
        if cd == ".":
            continue
        nodes[(r, c)] = Node(set(), (r, c), cd)
        if cd == "S":
            start = (r, c)
            nodes[(r, c)].allow.update(["N", "E", "S", "W"])
        match cd:
            case "|":
                nodes[(r, c)].allow.update(["N", "S"])
            case "-":
                nodes[(r, c)].allow.update(["W", "E"])
            case "L":
                nodes[(r, c)].allow.update(["N", "E"])
            case "J":
                nodes[(r, c)].allow.update(["N", "W"])
            case "7":
                nodes[(r, c)].allow.update(["S", "W"])
            case "F":
                nodes[(r, c)].allow.update(["E", "S"])


# make graph
for r, rd in enumerate(matrix):
    for c, cd in enumerate(rd):
        if cd == ".":
            continue
        node = nodes[(r, c)]
        north = (r - 1, c)
        east = (r, c + 1)
        south = (r + 1, c)
        west = (r, c - 1)
        match node.kind:
            case "|":
                if north in nodes and "S" in nodes[north].allow:
                    nodes[north].neighbours.add(node)
                    node.neighbours.add(nodes[north])
                if south in nodes and "N" in nodes[south].allow:
                    nodes[south].neighbours.add(node)
                    node.neighbours.add(nodes[south])

            case "-":
                if east in nodes and "W" in nodes[east].allow:
                    nodes[east].neighbours.add(node)
                    node.neighbours.add(nodes[east])
                if west in nodes and "E" in nodes[west].allow:
                    nodes[west].neighbours.add(node)
                    node.neighbours.add(nodes[west])

            case "L":
                if east in nodes and "W" in nodes[east].allow:
                    nodes[east].neighbours.add(node)
                    node.neighbours.add(nodes[east])
                if north in nodes and "S" in nodes[north].allow:
                    nodes[north].neighbours.add(node)
                    node.neighbours.add(nodes[north])

            case "J":
                if west in nodes and "E" in nodes[west].allow:
                    nodes[west].neighbours.add(node)
                    node.neighbours.add(nodes[west])
                if north in nodes and "S" in nodes[north].allow:
                    nodes[north].neighbours.add(node)
                    node.neighbours.add(nodes[north])

            case "7":
                if west in nodes and "E" in nodes[west].allow:
                    nodes[west].neighbours.add(node)
                    node.neighbours.add(nodes[west])
                if south in nodes and "N" in nodes[south].allow:
                    nodes[south].neighbours.add(node)
                    node.neighbours.add(nodes[south])

            case "F":
                if south in nodes and "N" in nodes[south].allow:
                    nodes[south].neighbours.add(node)
                    node.neighbours.add(nodes[south])
                if east in nodes and "W" in nodes[east].allow:
                    nodes[east].neighbours.add(node)
                    node.neighbours.add(nodes[east])


# pprint(matrix)

# print(len(nodes))

# for k, v in nodes.items():
#     print(k, v.kind, [c.kind for c in v.neighbours])

# BFS
queue = [nodes[start]]
queue[-1].value = 0
visited = list()
length = -1
d = dict()

# pbar = tqdm()
while queue:
    # pbar.update(1)
    # pbar.set_description("processed\t" + str(len(visited)))
    s = queue.pop(0)
    visited.append(s)
    # print("\nexplore", s.kind)
    for i in s.neighbours:
        if i not in visited:
            s.next.add(i)
            # print("\tneigh", i.kind, s.value + 1,  end="\t")
            i.value = s.value + 1
            queue.append(i)

    for v in visited:
        if v in queue:
            queue.remove(v)


# pprint(matrix)

s = nodes[start]
s1: Node = list(s.next)[0]
p1 = [s.position]
while True:
    p1.append(s1.position)
    s1 = list(s1.next)
    if len(s1) == 0:
        break
    s1 = s1[0]

s2: Node = list(s.next)[1]
p2 = [s.position]
while True:
    p2.append(s2.position)
    s2 = list(s2.next)
    if len(s2) == 0:
        break
    s2 = s2[0]

points = p1 + p2[::-1][1:]

polygon = Polygon(points)
ic = 0

print('Getting points')
for r, rd in tqdm(enumerate(matrix), total=len(matrix)):
    for c, cd in enumerate(rd):
        if (r, c) in points:
            continue
        point = Point(r, c)
        if polygon.contains(point):
            ic += 1
            matrix_copy[r][c] = "I"
        else:
            matrix_copy[r][c] = "O"

# print()
# pprint(matrix_copy)

print(ic)
