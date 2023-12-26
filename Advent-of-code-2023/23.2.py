from tqdm import tqdm
import networkx as nx

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
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

edges = []

for r, rd in enumerate(matrix):
    for c, cd in enumerate(rd):
        if cd == "#":
            continue
        for d in directions:
            dr, dc = d
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < len(matrix)
                and 0 <= nc < len(matrix[0])
                and matrix[nr][nc] != "#"
            ):
                edge = (f"{r},{c}", f"{nr},{nc}")
                edges.append(edge)
                edge = (f"{nr},{nc}", f"{r},{c}")
                edges.append(edge)

G = nx.Graph(edges)
start_node = ",".join(map(str, start))
end_node = ",".join(map(str, end))
edge_weights = dict()

for u, v in G.edges:
    edge_weights[(u, v)] = 1
    edge_weights[(v, u)] = 1

print("Initial nodes count", len(G.nodes))
print("Initial edges count", len(G.edges))


# Wikipedia says this is a NP hard problem
# So best I could think was this
# iGraph library is known to be faster for this
def compress(G: nx.Graph):
    for node in list(G.nodes):
        neighbours = list(G.neighbors(node))

        if len(neighbours) == 2:
            u, v = neighbours
            replacements = [(u, v), (v, u)]
            edge_weights[(u, v)] = edge_weights[(u, node)] + edge_weights[(node, v)]
            edge_weights[(v, u)] = edge_weights[(v, node)] + edge_weights[(node, u)]
            G.remove_node(node)
            G.add_edges_from(replacements)


compress(G)
print("Simplified nodes count", len(G.nodes))
print("Simplified edges count", len(G.edges))
pbar = tqdm()
longest = 0

for path in nx.all_simple_paths(G, source=start_node, target=end_node):
    prev = path[0]
    dist = 0
    for nxt in path[1:]:
        dist += edge_weights[(prev, nxt)]
        prev = nxt
    longest = max(longest, dist)
    pbar.set_description(f"Longest so far {longest}")
    pbar.update()
print(longest)

# Answer 6498 ~ 2 minutes
