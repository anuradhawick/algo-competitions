from math import ceil, floor

data = """
Time:      7  15   30
Distance:  9  40  200"""

data = """
Time:        59     70     78     78
Distance:   430   1218   1213   1276"""

# 6.2
data = """
Time:      71530
Distance:  940200"""

data = """
Time:        59707878
Distance:   430121812131276"""

times = list(map(int, data.strip().split("\n")[0].replace("Time:", "").strip().split()))
distances = list(
    map(int, data.strip().split("\n")[1].replace("Distance:", "").strip().split())
)


def solns(b, c):
    a = 1
    t1 = (b - (b**2 - 4 * a * c) ** 0.5) / (2 * a)
    t2 = (b + (b**2 - 4 * a * c) ** 0.5) / (2 * a)

    return (
        ceil(t1) if ceil(t1) > t1 else int(t1) + 1,
        floor(t2) if floor(t2) < t2 else int(t2) - 1,
    )


ways = 1

for t, d in zip(times, distances):
    s, e = solns(t, d)
    ways *= e - s + 1

print(ways)
