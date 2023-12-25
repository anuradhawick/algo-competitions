from tqdm import tqdm

data = """
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""
data = open("22.txt").read()


# from https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


# Given three collinear points p, q, r, the function checks if
# point q lies on line segment 'pr'
def onSegment(p: Point, q: Point, r: Point):
    if (
        (q.x <= max(p.x, r.x))
        and (q.x >= min(p.x, r.x))
        and (q.y <= max(p.y, r.y))
        and (q.y >= min(p.y, r.y))
    ):
        return True
    return False


def orientation(p, q, r):
    # to find the orientation of an ordered triplet (p,q,r)
    # function returns the following values:
    # 0 : Collinear points
    # 1 : Clockwise points
    # 2 : Counterclockwise

    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
    # for details of below formula.

    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if val > 0:
        # Clockwise orientation
        return 1
    elif val < 0:
        # Counterclockwise orientation
        return 2
    else:
        # Collinear orientation
        return 0


# The main function that returns true if
# the line segment 'p1q1' and 'p2q2' intersect.
def doIntersect(p1, q1, p2, q2):
    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if (o1 != o2) and (o3 != o4):
        return True

    # Special Cases

    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
    if (o1 == 0) and onSegment(p1, p2, q1):
        return True

    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
    if (o2 == 0) and onSegment(p1, q2, q1):
        return True

    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
    if (o3 == 0) and onSegment(p2, p1, q2):
        return True

    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
    if (o4 == 0) and onSegment(p2, q1, q2):
        return True

    # If none of the cases
    return False


class Cube:
    def __init__(self, p, q, name=None) -> None:
        self.p: Point = p
        self.q: Point = q
        self.supported_by = set()
        self.supported_to = set()
        self.name = name

    def move_down(self, offset):
        self.p.z += offset
        self.q.z += offset

    def intersects(self, other: "Cube"):
        p1, q1 = self.p, self.q
        p2, q2 = other.p, other.q
        return doIntersect(p1, q1, p2, q2)


class Grid:
    def __init__(self, cubes) -> None:
        self.cubes: list[Cube] = cubes

    def order_cubes(self) -> None:
        self.cubes.sort(key=lambda cube: (cube.p.z, cube.q.z))

    def move_all(self):
        moved_cubes = []
        for cube in tqdm(self.cubes):
            intersecting_z = 0
            support = []
            for moved_cube in moved_cubes:
                if cube.intersects(moved_cube):
                    support.append(moved_cube)
            intersecting_z = [max(c.p.z, c.q.z) for c in support]
            intersecting_z = max(intersecting_z) if len(intersecting_z) else 0

            support = [c for c in support if max(c.p.z, c.q.z) == intersecting_z]
            cube.supported_by = set(support)
            for s in cube.supported_by:
                s.supported_to.add(cube)
            cube.move_down(-(min(cube.p.z, cube.q.z) - intersecting_z - 1))
            moved_cubes.insert(0, cube)


def check_planar(x1, y1, z1, x2, y2, z2):
    return x1 == x2 and y1 == y2 or x1 == x2 and z1 == z2 or y1 == y2 and z1 == z2


cubes = []

for line in data.strip().split("\n"):
    cord1, cord2 = line.strip().split("~")
    x1, y1, z1 = list(map(int, cord1.split(",")))
    x2, y2, z2 = list(map(int, cord2.split(",")))

    assert x1 <= x2 and y1 <= y2 and z1 <= z2
    assert check_planar(x1, y1, z1, x2, y2, z2)

    p = Point(x1, y1, z1)
    q = Point(x2, y2, z2)
    cube = Cube(p, q)
    cubes.append(cube)


grid = Grid(cubes)
grid.order_cubes()
grid.move_all()

removables = 0

for cube in grid.cubes:
    if all([len(s.supported_by) > 1 for s in cube.supported_to]):
        removables += 1




def disintegrate(start):
    broken = set([start])
    to_break = [start]

    while len(to_break) > 0:
        u = to_break.pop(0)
        dependents: list[Cube] = u.supported_to

        for dependent in dependents:
            # this brick is falling down
            if all([s in broken for s in dependent.supported_by]):
                broken.add(dependent)
                to_break.append(dependent)
    return len(broken) - 1


total = 0
for cube in tqdm(grid.cubes):
    total += disintegrate(cube)
print(total)
