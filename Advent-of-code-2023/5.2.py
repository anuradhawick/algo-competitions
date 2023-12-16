from tqdm import tqdm
from tqdm.contrib.concurrent import process_map


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
        self.cache: Map = maps[0]

    def translate(self, val):
        if res := self.cache.get_match(val):
            return res
        for m in self.maps:
            if res := m.get_match(val):
                self.cache = m
                return res
        return val

    def maps_for_the_range(self, start, end):
        maps = []
        for m in self.maps:
            # start region is within map
            if start < m.sstart + m.size and end >= m.sstart:
                maps.append(m)
        return maps


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
seed_ranges_flat = list(map(int, segs[0].split(":")[1].strip().split()))


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

ranges_iter = iter(seed_ranges_flat)
seed_ranges = zip(ranges_iter, ranges_iter)

val = float("inf")


def get_val(x):
    x = seed2soil.translate(x)
    x = soil2fertilizer.translate(x)
    x = fertilizer2water.translate(x)
    x = water2light.translate(x)
    x = light2temperature.translate(x)
    x = temperature2humidity.translate(x)
    x = humidity2location.translate(x)

    return x


for start, size in seed_ranges:
    r = process_map(
        get_val, range(start, start + size), max_workers=32, chunksize=100000
    )
    val = min(min(r), val)

print(val)
