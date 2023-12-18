from collections import defaultdict
from copy import deepcopy
import heapq

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

# data = """
# 111111111111
# 999999999991
# 999999999991
# 999999999991
# 999999999991"""


data = open("17.txt").read()


class Vertex:
    def __init__(self, cost, position) -> None:
        self.cost: int = cost
        self.position: tuple = position
        self.neighbours: dict[str, "Vertex"] = dict()

    def __lt__(self, other):
        # do not care
        return True


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

# this heap gives us the node with shortest distance to it
# despite the direction it may have gone
queue: list[tuple[int, tuple[Vertex, str, int]]] = []
heapq.heappush(queue, (vertices[0][1].cost, (vertices[0][1], "r", 1)))
heapq.heappush(queue, (vertices[1][0].cost, (vertices[1][0], "b", 1)))

# start node, direction, steps_taken: distance so far
# in order to set initial direction, I have hard coded the next two possible 
# points after the start node
cost = {
    (vertices[0][0], "", 0): 0,
    (vertices[1][0], "b", 1): vertices[1][0].cost,
    (vertices[0][1], "r", 1): vertices[0][1].cost,
}
parent: dict[tuple[Vertex, str, int], tuple[Vertex, str, int]] = {
    (vertices[0][0], "", 0): None,
    (vertices[1][0], "b", 1): (vertices[0][0], "", 0),
    (vertices[0][1], "r", 1): (vertices[0][0], "", 0),
}


def can_go_four(start: Vertex, direction: str, min_depth=3):
    start = start
    for _ in range(min_depth):
        if direction in start.neighbours:
            start = start.neighbours[direction]
        else:
            return False
    return True


# solve the distances for each direction.
while len(queue) > 0:
    current_cost, current_state = heapq.heappop(queue)
    (current_node, current_direction, current_step_count) = current_state
    # check each direction
    for new_direction in "trlb":
        # must move four blocks min
        if new_direction in current_node.neighbours:
            neighbour = current_node.neighbours[new_direction]
            # are we going in same direction or turning, if turning, it is a new step counter
            new_step_count = (
                current_step_count + 1 if current_direction == new_direction else 1
            )
            # same direction, too far? discontinue
            if new_step_count > 10:
                continue

            # in the new direction, there must be 4 blocks ahead
            if new_step_count == 1:
                can = True
                n_temp = neighbour
                for _ in range(3):
                    if new_direction not in n_temp.neighbours:
                        can = False
                        break
                    n_temp = n_temp.neighbours[new_direction]
                if not can:
                    continue

            # not gone enough? can only go in parent direction
            if current_step_count < 4 and new_direction != current_direction:
                continue

            # already visited node and already visited neighbour? skip
            if current_state in parent and neighbour == parent[current_state][0]:
                continue

            new_state = (neighbour, new_direction, new_step_count)
            new_cost = current_cost + neighbour.cost

            # if this is a brand new visit or it has already been visited at a greater cost
            if new_state not in cost or new_cost < cost[new_state]:
                # print(new_state)
                cost[new_state] = new_cost
                parent[new_state] = current_state
                heapq.heappush(queue, (new_cost, new_state))


matrix = [["."] * len(line) for line in data.strip().split()]
current_state = (vertices[-1][-1], "", "")

cost_to_dest = 9999999
current_state = None
for k, v in cost.items():
    n, d, s = k
    if n == vertices[-1][-1] and v < cost_to_dest:
        cost_to_dest = v
        current_state = k

# DEBUG
# while current_state is not None:
#     n, d, s = current_state
#     matrix[n.position[0]][n.position[1]] = str(n.cost)
#     if current_state not in parent:
#         break
#     current_state = parent[current_state]

# print("\n".join(["".join(line) for line in matrix]))
print(cost_to_dest)
