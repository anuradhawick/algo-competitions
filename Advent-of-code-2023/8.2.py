from functools import reduce
from operator import mul

data = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

data = open("8.txt").read()

class Node:
    def __init__(self, val, left=None, right=None) -> None:
        self.val = val
        self.left = left
        self.right = right


class Map:
    def __init__(self, start: Node) -> None:
        self.start = start
        self.head = start

    def iterate(self, insutrctions):
        count = 0
        while True:
            count += 1
            for i in insutrctions:
                if i == "L":
                    self.head = self.head.left
                else:
                    self.head = self.head.right
            
            if self.head.val.endswith("Z"):
                return count


ins = list(data.strip().split("\n")[0].strip())

nodes: dict[str, Node] = dict()

for line in data.strip().split("\n\n")[1].split("\n"):
    line = line.strip().split("=")
    start = line[0].strip()
    left, right = [x.strip() for x in line[1].strip().strip("(").strip(")").split(",")]

    for x in [start, left, right]:
        if x not in nodes:
            nodes[x] = Node(x)

    nodes[start].left = nodes[left]
    nodes[start].right = nodes[right]


candidates = [v for k, v in nodes.items() if k.endswith('A')]

vals = []
for head in candidates:
    m = Map(head)
    vals.append(m.iterate(ins))

print(len(ins) * reduce(mul, vals))