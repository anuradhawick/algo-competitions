from tqdm import tqdm
from itertools import product

data = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


data = open('12.txt').read()


def get_groups(line):
    groups = []
    x = line[0]
    for char in line[1:]:
        if char != x[-1]:
            groups.append(x)
            x = char
        else:
            x += char
    groups.append(x)
    return groups


def is_valid(candidate, pattern):
    for t, p in zip(candidate, pattern):
        if p == "#" and t != "#" or p == "." and t != ".":
            return False
    return True


s = 0
for line in tqdm(data.strip().split("\n")):
    pattern, order = line.strip().split()
    order = list(map(int, order.strip().split(",")))
    template = [("#" * x, 3) for x in order]
    tlen = sum(order)
    # print(line)
    # gap_template = [0] + [1 for _ in template[:-1]] + [0]
    # print(template)
    # print(gap_template)
    # print()
    # print(pattern, order)
    count = 0

    for gaps in product(range(len(pattern) - (tlen + len(template) - 4)), repeat=len(template) + 1):
        if 0 in gaps[1:-1]:
            continue
        if sum(gaps) + tlen >len(pattern):
            continue
        # print(gaps)
        dots = ["." * g for g in gaps]
        candidate = dots.pop(0)
        for t, d in zip(template, dots):
            candidate += t[0] + d
        if len(candidate) != len(pattern):
            continue
        if is_valid(candidate, pattern):
            # print(gaps)
            # print(candidate)
            count += 1
    s += count
    print(pattern, count)
print(s)
