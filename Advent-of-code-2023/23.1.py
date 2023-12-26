import heapq as hq

data = """
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""

data = open("23.txt").read()

matrix = [list(line) for line in data.strip().split("\n")]
start = 0, matrix[0].index(".")
end = len(matrix) - 1, matrix[-1].index(".")
directions = dict()
directions["."] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
directions[">"] = [(0, 1)]
directions["<"] = [(0, -1)]
directions["^"] = [(-1, 0)]
directions["v"] = [(1, 0)]

# queue stores (distance, (parent, node)) to account for four possible incomings
# same as Day 17 AoC 2023
queue = [(0, (None, start))]
cost = {(None, start): 0}
parent = {(None, start): (None, None)}

while len(queue):
    curr_cost, curr_state = hq.heappop(queue)
    curr_parent, (r, c) = curr_state
    curr_char = matrix[r][c]

    for d in directions[curr_char]:
        dr, dc = d
        nr, nc = r + dr, c + dc

        if 0 <= nr < len(matrix) and 0 <= nc < len(matrix[0]) and matrix[nr][nc] != "#":
            new_cost = curr_cost - 1
            new_state = ((r, c), (nr, nc))

            if curr_state in parent and (nr, nc) == parent[curr_state][1]:
                continue

            if new_state not in cost or curr_cost < cost[new_state]:
                cost[new_state] = new_cost
                parent[new_state] = curr_state
                hq.heappush(queue, (new_cost, new_state))

for k, v in cost.items():
    p, s = k
    if s == end:
        print(s, abs(v))
