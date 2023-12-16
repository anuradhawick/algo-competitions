data = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
"""

data = """
#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


def parse_1(data):
    m = [list(line.strip()) for line in data.strip().split("\n")]
    dataT = "\n".join(
        [
            "".join(row)
            for row in [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]
        ]
    )
    return data, dataT


def get_splits(data):
    line = data.strip().split()[0]
    positions = [i for i in range(len(line))]
    valid_positions = list(positions)

    for line in data.strip().split():
        for pos in positions:
            p1 = line[:pos]
            p2 = line[pos:][::-1]
            if len(p1) == 0 or len(p2) == 0:
                valid_positions.remove(pos)
                continue
            if not (p1.endswith(p2) or p2.endswith(p1)):
                valid_positions.remove(pos)
        positions = list(valid_positions)
    return valid_positions


def print_reflection(valids):
    for v in valids:
        print()
        for line in data.strip().split():
            chars = list(line)
            chars.insert(v, " ")
            print("".join(chars))


# valids1 = get_splits(data)
# valids2 = get_splits(dataT)

# print(sum(valids1 + [100 * v for v in valids2]))


# d1, d2 = parse_1(data)
# print(d2)
# print(get_splits(d1))
# print()
# print(get_splits(d2))

data = open("13.1.txt").read().strip().split("\n\n")
data = open('13.txt').read().strip().split('\n\n')
s = 0

for entry in data:
    matrix = [list(line) for line in entry.strip().split("\n")]
    found = False
    d1, d2 = parse_1(entry)
    old_valids1 = get_splits(d1)
    old_valids2 = get_splits(d2)
    for ri in range(len(matrix)):
        for ci in range(len(matrix[0])):
            o = matrix[ri][ci]
            matrix[ri][ci] = "." if o == "#" else "#"
            new_entry = "\n".join(["".join(row) for row in matrix])
            d1, d2 = parse_1(new_entry)
            valids1 = get_splits(d1)
            valids2 = get_splits(d2)
            matrix[ri][ci] = o
            valids1 = [v for v in valids1 if v not in old_valids1]
            valids2 = [v for v in valids2 if v not in old_valids2]
            found = len(valids1) > 0 or len(valids2) > 0
            if found:
                # print(valids1, valids2, ri, ci)
                s += sum(valids1 + [100 * v for v in valids2])
                break
        if found:
            break

    # break
print(s)
