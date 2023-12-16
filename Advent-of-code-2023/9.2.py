data = """
10 13 16 21 30 45
"""

data = open("9.txt").read()


def process(line):
    matrix = [line]

    while not all([x == 0 for x in matrix[-1]]):
        last_line = matrix[-1]
        new_line = [last_line[x + 1] - last_line[x] for x in range(len(last_line) - 1)]
        matrix.append(new_line)

    # for x in matrix:
    #     print(x)

    new_matrix = matrix[::-1]

    for i, row in enumerate(new_matrix[:-1]):
        new_matrix[i + 1].insert(0,  new_matrix[i + 1][0] - row[0])

    # for x in matrix:
    #     print(x)

    return matrix[0][0]


s = 0
for line in data.strip().split("\n"):
    line = list(map(int, line.strip().split()))
    s += process(line)
print(s)
