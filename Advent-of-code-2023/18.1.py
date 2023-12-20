from shapely import Point, Polygon

data = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

data = open("18.txt").read()

points = [(0, 0)]
circumference = 0
for line in data.strip().split("\n"):
    direction, length, color = line.strip().split()
    length = int(length)
    circumference += length
    r, c = points[-1]
    match direction:
        case "R":
            next_point = (r, c + length)
        case "L":
            next_point = (r, c - length)
        case "U":
            next_point = (r - length, c)
        case "D":
            next_point = (r + length, c)
    points.append(next_point)

points = [Point(p) for p in points]
poly = Polygon(points)

# inner area + half of curcumference + correction value
print(poly.area + circumference / 2 + 1)
