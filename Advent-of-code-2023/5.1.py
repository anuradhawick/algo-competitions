class Map:
    def __init__(self, dest, src, sz):
        self.dstart = dest
        self.sstart = src
        self.size = sz

    def get_match(self, src):
        if src >= self.sstart and src < self.sstart + self.size:
            return (src - self.sstart) + self.dstart
        return None


class Translator:
    def __init__(self, maps):
        self.maps: list[Map] = maps

    def translate(self, val):
        res = None
        for m in self.maps:
            if r := m.get_match(val):
                res = r
        return res if res else val


data = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
data = open("5.txt").read()

segs = data.strip().split("\n\n")
seeds = list(map(int, segs[0].split(":")[1].strip().split()))


def parse_map(seg):
    return Translator(
        [Map(*list(map(int, line.strip().split()))) for line in seg.split("\n")[1:]]
    )


parse_map(segs[1])

seed2soil = parse_map(segs[1])
soil2fertilizer = parse_map(segs[2])
fertilizer2water = parse_map(segs[3])
water2light = parse_map(segs[4])
light2temperature = parse_map(segs[5])
temperature2humidity = parse_map(segs[6])
humidity2location = parse_map(segs[7])

vals = []
for seed in seeds:
    x = seed2soil.translate(seed)
    x = soil2fertilizer.translate(x)
    x = fertilizer2water.translate(x)
    x = water2light.translate(x)
    x = light2temperature.translate(x)
    x = temperature2humidity.translate(x)
    x = humidity2location.translate(x)
    vals.append(x)

print(min(vals))
