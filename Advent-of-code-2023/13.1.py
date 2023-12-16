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
    posses = [i for i in range(len(line))]
    valids = list(posses)

    for line in data.strip().split():
        for pos in posses:
            p1 = line[:pos]
            p2 = line[pos:][::-1]
            if len(p1) == 0 or len(p2) == 0:
                valids.remove(pos)
                continue
            # mlen = min(pos, len(line) - pos)
            # print(p1, p2[::-1])
            if not (p1.endswith(p2) or p2.endswith(p1)):
                valids.remove(pos)
        posses = list(valids)
    return valids


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
    d1, d2 = parse_1(entry)
    valids1 = get_splits(d1)
    valids2 = get_splits(d2)
    # print(valids1, valids2)
    s += sum(valids1 + [100 * v for v in valids2])

    # break
print(s)
