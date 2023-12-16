from tqdm import tqdm

data = """
.....
.S-7.
.|.|.
.L-J.
....."""

data = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""

# data = """
# 7-F7-
# .FJ|7
# SJLL7
# |F--J
# LJ.LJ"""

data = open("10.txt").read()


def pprint(m):
    for x in m:
        print("".join(x))


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


nodes: dict[tuple, Node] = dict()

# init nodes
for r, rd in enumerate(matrix):
    for c, cd in enumerate(rd):
        if cd == ".":
            continue
        nodes[(r, c)] = Node(set(), (r, c), cd)
        if cd == "S":
            start = (r, c)
            nodes[(r, c)].allow.update(['N', 'E', 'S', 'W'])
        match cd:
            case "|":
                nodes[(r, c)].allow.update(['N', 'S'])
            case "-":
                nodes[(r, c)].allow.update(['W', 'E'])
            case "L":
                nodes[(r, c)].allow.update(['N', 'E'])
            case "J":
                nodes[(r, c)].allow.update(['N', 'W'])
            case "7":
                nodes[(r, c)].allow.update(['S', 'W'])
            case "F":
                nodes[(r, c)].allow.update(['E', 'S'])
                

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
                if north in nodes and 'S' in nodes[north].allow:
                    nodes[north].neighbours.add(node)
                    node.neighbours.add(nodes[north])
                if south in nodes and 'N' in nodes[south].allow:
                    nodes[south].neighbours.add(node)
                    node.neighbours.add(nodes[south])

            case "-":
                if east in nodes and 'W' in nodes[east].allow:
                    nodes[east].neighbours.add(node)
                    node.neighbours.add(nodes[east])
                if west in nodes and 'E' in nodes[west].allow:
                    nodes[west].neighbours.add(node)
                    node.neighbours.add(nodes[west])

            case "L":
                if east in nodes and 'W' in nodes[east].allow:
                    nodes[east].neighbours.add(node)
                    node.neighbours.add(nodes[east])
                if north in nodes and 'S' in nodes[north].allow:
                    nodes[north].neighbours.add(node)
                    node.neighbours.add(nodes[north])

            case "J":
                if west in nodes and 'E' in nodes[west].allow:
                    nodes[west].neighbours.add(node)
                    node.neighbours.add(nodes[west])
                if north in nodes and 'S' in nodes[north].allow:
                    nodes[north].neighbours.add(node)
                    node.neighbours.add(nodes[north])

            case "7":
                if west in nodes and 'E' in nodes[west].allow:
                    nodes[west].neighbours.add(node)
                    node.neighbours.add(nodes[west])
                if south in nodes and 'N' in nodes[south].allow:
                    nodes[south].neighbours.add(node)
                    node.neighbours.add(nodes[south])

            case "F":
                if south in nodes and 'N' in nodes[south].allow:
                    nodes[south].neighbours.add(node)
                    node.neighbours.add(nodes[south])
                if east in nodes and 'W' in nodes[east].allow:
                    nodes[east].neighbours.add(node)
                    node.neighbours.add(nodes[east])


# pprint(matrix)

print(len(nodes))

# for k, v in nodes.items():
#     print(k, v.kind, [c.kind for c in v.neighbours])

# BFS
queue = [nodes[start]]
queue[-1].value = 0
visited = set()
length = -1
d = dict()

# pbar = tqdm()
while queue:
    # pbar.update(1)
    # pbar.set_description("processed\t" + str(len(visited)))
    s = queue.pop(0)
    visited.add(s)
    # print("\nexplore", s.kind)
    for i in s.neighbours:
        if i not in visited:
            # print("\tneigh", i.kind, s.value + 1,  end="\t")
            i.value = s.value + 1
            queue.append(i)

    for v in visited:
        if v in queue:
            queue.remove(v)


# for v in visited:
#     matrix_copy[v.position[0]][v.position[1]] = str(v.value)
# print()
# pprint(matrix_copy)
print("==============")
print(max([v.value for v in visited]))
