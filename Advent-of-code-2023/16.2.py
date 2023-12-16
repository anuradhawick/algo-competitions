from functools import cache

data = """
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....
"""

data = open("16.txt").read()


class Ray:
    def __init__(self, pos, direction) -> None:
        self.pos = pos
        self.direction = direction


def is_valid(ray: Ray, matrix: list[list[str]]):
    r, c = ray.pos
    return not (r < 0 or c < 0 or r >= len(matrix) or c >= len(matrix[0]))


matrix: list[list[str]] = [list(line) for line in data.strip().split("\n")]


@cache
def get_next_rays(r, c, d):
    rays: list[Ray] = []
    visited = set()
    visited.add((r, c, d))

    # passthrough conditions
    while (
        matrix[r][c] == "."
        or (d in ("L", "R") and matrix[r][c] == "-")
        or (d in ("U", "D") and matrix[r][c] == "|")
    ):
        match d:
            case "R":
                c += 1
            case "L":
                c -= 1
            case "U":
                r -= 1
            case "D":
                r += 1

        if r < 0 or c < 0 or r >= len(matrix) or c >= len(matrix[0]):
            return [], visited

        visited.add((r, c, d))

    split = matrix[r][c]
    ray1 = None
    ray2 = None

    match split:
        case "|":
            ray1 = Ray((r - 1, c), "U")
            ray2 = Ray((r + 1, c), "D")
        case "-":
            ray1 = Ray((r, c - 1), "L")
            ray2 = Ray((r, c + 1), "R")
        case "/":
            match d:
                case "U":
                    ray1 = Ray((r, c + 1), "R")
                case "D":
                    ray1 = Ray((r, c - 1), "L")
                case "L":
                    ray1 = Ray((r + 1, c), "D")
                case "R":
                    ray1 = Ray((r - 1, c), "U")
        case "\\":
            match d:
                case "U":
                    ray1 = Ray((r, c - 1), "L")
                case "D":
                    ray1 = Ray((r, c + 1), "R")
                case "L":
                    ray1 = Ray((r - 1, c), "U")
                case "R":
                    ray1 = Ray((r + 1, c), "D")

    if ray1 and is_valid(ray1, matrix):
        rays.append(ray1)
    if ray2 and is_valid(ray2, matrix):
        rays.append(ray2)

    return rays, visited


def get_visited(r, c, d):
    rays, visited = get_next_rays(r, c, d)

    while len(rays):
        next_ray: Ray = rays.pop(0)
        r, c = next_ray.pos
        d = next_ray.direction
        new_rays, new_visited = get_next_rays(r, c, d)

        if len(new_visited - visited) == 0:
            continue

        rays.extend(new_rays)
        visited.update(new_visited)

    return {(r, c) for r, c, _ in visited}


e_max = 0

# Top left
e_max = max(e_max, len(get_visited(0, 0, "R")), len(get_visited(0, 0, "D")))
# Bottom left
e_max = max(
    e_max,
    len(get_visited(len(matrix) - 1, 0, "U")),
    len(get_visited(len(matrix) - 1, 0, "R")),
)
# Bottom right
e_max = max(
    e_max,
    len(get_visited(len(matrix) - 1, len(matrix) - 1, "U")),
    len(get_visited(len(matrix) - 1, len(matrix) - 1, "L")),
)
# Top right
e_max = max(
    e_max,
    len(get_visited(0, len(matrix) - 1, "D")),
    len(get_visited(0, len(matrix) - 1, "L")),
)

for r in range(1, len(matrix) - 1):
    r1, c1, d1 = r, 0, "R"
    r2, c2, d2 = r, len(matrix) - 1, "L"

    e_max = max(e_max, len(get_visited(r1, c1, d1)), len(get_visited(r2, c2, d2)))

for c in range(1, len(matrix[0]) - 1):
    r1, c1, d1 = 0, c, "D"
    r2, c2, d2 = len(matrix[0]) - 1, c, "U"
    e_max = max(e_max, len(get_visited(r1, c1, d1)), len(get_visited(r2, c2, d2)))

print(e_max)
