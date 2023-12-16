def str_hash(string):
    curr = 0
    for s in string:
        n = ord(s)
        curr += n
        curr *= 17
        curr %= 256
    return curr


# print(str_hash("HASH"))
s = 0
data = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

data = open("15.txt").read()

boxes = [[] for x in range(256)]


def pprint(boxes):
    for n, lenses in enumerate(boxes):
        if len(lenses) == 0:
            continue
        print(f"Box {n}:", "\t".join([f"[{l} {v}]" for l, v in lenses]))


for c in data.strip().split(","):
    if "=" in c:
        label, value = c.split("=")
        n = str_hash(label)
        lenses = boxes[n]
        lens_replaced = False
        # if already a lense with same label
        for i in range(len(lenses)):
            if lenses[i][0] == label:
                lenses[i] = (label, value)
                lens_replaced = True
        if not lens_replaced:
            lenses.append((label, value))

    if "-" in c:
        label, value = c.split("-")
        n = str_hash(label)
        lenses = boxes[n]
        boxes[n] = [(l, v) for (l, v) in boxes[n] if l != label]

    # print()
    # print(c)
    # pprint(boxes)
tot = 0

for n, lenses in enumerate(boxes):
    for m, (label, power) in enumerate(lenses):
        fp = (n + 1) * (m + 1) * int(power)
        print(label, fp)
        tot += fp

print(tot)
