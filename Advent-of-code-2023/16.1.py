from copy import deepcopy


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


first_ray: Ray = Ray((0, 0), "R")
rays: list[Ray] = [first_ray]
matrix: list[list[str]] = [list(line) for line in data.strip().split("\n")]
energized: list[list[str]] = [["."] * len(line) for line in data.strip().split("\n")]
rays_passed = set()

while len(rays) > 0:
    energized_copy = deepcopy(energized)
    ray = rays.pop(0)
    r, c = ray.pos
    d = ray.direction

    rays_passed.add((r, c, d))

    # print("casting from", r, c, matrix[r][c])
    ray_completed = False

    # passthrough conditions
    energized[r][c] = "#"
    while (
        matrix[r][c] == "."
        or (d in ("L", "R") and matrix[r][c] == "-")
        or (d in ("U", "D") and matrix[r][c] == "|")
    ):
        match d:
            case "R":
                c += 1
                pass
            case "L":
                c -= 1
                pass
            case "U":
                r -= 1
                pass
            case "D":
                r += 1
                pass

        if r < 0 or c < 0 or r >= len(matrix) or c >= len(matrix[0]):
            ray_completed = True
            break

        energized[r][c] = "#"

    if ray_completed:
        continue

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
                    pass
                case "D":
                    ray1 = Ray((r, c - 1), "L")
                    pass
                case "L":
                    ray1 = Ray((r + 1, c), "D")
                    pass
                case "R":
                    ray1 = Ray((r - 1, c), "U")
                    pass
        case "\\":
            match d:
                case "U":
                    ray1 = Ray((r, c - 1), "L")
                    pass
                case "D":
                    ray1 = Ray((r, c + 1), "R")
                    pass
                case "L":
                    ray1 = Ray((r - 1, c), "U")
                    pass
                case "R":
                    ray1 = Ray((r + 1, c), "D")
                    pass
    if (
        ray1
        and not ((ray1.pos[0], ray1.pos[1], ray1.direction) in rays_passed)
        and is_valid(ray1, matrix)
    ):
        rays.append(ray1)
    if (
        ray2
        and not ((ray2.pos[0], ray2.pos[1], ray2.direction) in rays_passed)
        and is_valid(ray2, matrix)
    ):
        rays.append(ray2)

count = 0
for line in energized:
    count += line.count("#")

print(count)
