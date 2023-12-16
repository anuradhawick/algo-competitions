data = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

data = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

data = open("8.txt").read()


class Node:
    def __init__(self, val, left=None, right=None) -> None:
        self.val = val
        self.left = left
        self.right = right


class Map:
    def __init__(self, start: Node) -> None:
        self.start = start

    def iterate(self, insutrctions):
        head = self.start
        count = 0

        while True:
            for i in insutrctions:
                count += 1
                if i == "L":
                    head = head.left
                else:
                    head = head.right
            if head.val == "ZZZ":
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

head = nodes["AAA"]

m = Map(head)

print(m.iterate(ins))
