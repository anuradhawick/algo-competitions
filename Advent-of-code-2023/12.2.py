from tqdm import tqdm
from itertools import product
from functools import cache

data = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

data = """
#??.#??.??#?#????#?# 2,1,6,3"""


data = open("12.txt").read()


@cache
def discover_paths(segments, pattern):
    if len(segments) == 0:
        if "#" in pattern:
            return 0
        return 1

    curr = segments[0]
    paths = 0

    for i in range(len(pattern) - sum(segments[1:])):
        for j in range(i, i + curr):
            if j == i and j > 0 and pattern[j - 1] == "#":
                return paths
            if j >= len(pattern):
                return paths
            # invalid
            if pattern[j] == ".":
                break
            # valid path found
            if j == i + curr - 1:
                # conflicting ending
                if j + 1 < len(pattern) and pattern[j + 1] == "#":
                    break
                # happy path
                paths += discover_paths(segments[1:], pattern[j + 2 :])

    return paths


s = 0
for line in data.strip().split("\n"):
    pattern, order = line.strip().split()
    order = tuple(map(int, order.strip().split(",")))
    templates = ["#" * c for c in order]

    order *= 5
    pattern = "?".join([pattern for _ in range(5)])

    matrix = [[0 for x in range(len(pattern) + 1)]] + [
        [0] + [99] * len(pattern) for itr in range(sum(order))
    ]

    p = discover_paths(order, pattern)
    discover_paths.cache_clear()
    s += p
    # print(pattern, p)
print("total", s)
