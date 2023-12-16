data = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
data = open('14.txt').read()
transpose = lambda m: "\n".join(
    [
        "".join(row)
        for row in [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]
    ]
)
# print(data)
data = data.strip().split("\n")
matrix = transpose(data)

print()
new_matrix = []
for row in matrix.strip().split("\n"):
    idx = 0
    row = list(row)
    # print()
    # print(row)

    for ci, c in enumerate(row):
        # print(ci, c)
        # if # do nothing just increment
        if c == "#":
            idx = ci + 1
        # if a ball move to idx
        if c == "O":
            if ci > idx:
                # print("move", ci, "to", idx)
                row[idx] = "O"
                row[ci] = "."
                for x in range(idx + 1, len(row)):
                    if row[x] == ".":
                        idx = x
                        break
            else:
                idx += 1

    # print(row)
    new_matrix.append(row)
    # break
total = 0

for row in new_matrix:
    for ci, c in enumerate(row):
        total += (len(row) - ci) if c == "O" else 0
print(total)
# print("\n".join(["".join(row) for row in new_matrix]))
# print(transpose(new_matrix))
