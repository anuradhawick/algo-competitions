def str_hash(string):
    curr = 0
    for s in string:
        n = ord(s)
        curr += n
        curr *= 17
        curr %= 256
    return curr


print(str_hash("HASH"))
s = 0
data = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

data = open("15.txt").read()

for c in data.strip().split(","):
    n = str_hash(c)
    print(c, n)
    s += n

print(s)