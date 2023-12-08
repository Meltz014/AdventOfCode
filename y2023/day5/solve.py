from AoC import AoC
import numpy as np
from pprint import pprint
from itertools import chain

"""
0 69 1
1 0 69

1 0 55
57 56 13

60 56 37
56 93 4
"""

def range_intersect(x, y):
    a = max(x[0], y[0])
    b = min(x[-1], y[-1])
    if b < a:
        return None
    return a, b

def split_maps(a, b):
    q = a.copy()
    new_a = []
    min_b_start = min(b, key=lambda x: x[1])[1]
    while q:
        a_offset, a_start, a_len = q.pop()
        was_split = False
        print(f'a: {[a_offset, a_start, a_len]}')
        for b_offset, b_start, b_len in chain([[0, 0, min_b_start]], b):
            print(f'b: {[b_offset, b_start, b_len]}')
            isect = range_intersect([a_start, a_start+a_len-1], [b_start, b_start+b_len-1])
            if isect:
                was_split = True
                if isect[0] == a_start:
                    if isect[1] == a_start + a_len - 1:
                        # A range is fully reduced
                        n_a = [a_offset, a_start, a_len]
                        if n_a not in new_a:
                            new_a.append(n_a)
                        continue
                    else:
                        new_start_1 = isect[0]
                        new_len_1 = isect[1] - isect[0] + 1
                        new_start_2 = isect[1] + 1
                        new_len_2 = (a_start + a_len) - new_start_2
                else:
                    new_start_1 = a_start
                    new_len_1 = isect[0] - a_start
                    new_start_2 = isect[0]
                    new_len_2 = isect[1] - isect[0] + 1
                    if isect[1] < a_start + a_len - 1:
                        # B range is fully contained in A range.  split A into 3
                        new_start_3 = isect[1] + 1
                        new_len_3 = (a_start + a_len) - isect[1] - 1
                        new_offset_3 = a_offset - a_start + new_start_3
                        q.insert(0, [new_offset_3, new_start_3, new_len_3])
                        print(f'new a 3: {[new_offset_3, new_start_3, new_len_3]}')

                new_offset_1 = a_offset - a_start + new_start_1
                new_offset_2 = a_offset - a_start + new_start_2
                q.insert(0, [new_offset_2, new_start_2, new_len_2])
                q.insert(0, [new_offset_1, new_start_1, new_len_1])
                print(f'new a 1: {[new_offset_1, new_start_1, new_len_1]}')
                print(f'new a 2: {[new_offset_2, new_start_2, new_len_2]}')
                break
        if not was_split:
            n_a = [a_offset, a_start, a_len]
            if n_a not in new_a:
                new_a.append(n_a)
    return new_a



class Solver(AoC):
    example_data = """seeds: 79 14 55 13

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
56 93 4"""


    def translate(self, src_val, ranges):
        for map_range in ranges:
            if src_val in range(map_range[1], map_range[1]+map_range[2]):
                offset = map_range[0] - map_range[1]
                return src_val + offset
        return src_val

    def translate_seed(self, seed):
        soil = self.translate(seed, self.maps['seed_to_soil'])
        fert = self.translate(soil, self.maps['soil_to_fert'])
        water = self.translate(fert, self.maps['fert_to_water'])
        light = self.translate(water, self.maps['water_to_light'])
        temp = self.translate(light, self.maps['light_to_temp'])
        humid = self.translate(temp, self.maps['temp_to_humid'])
        loc = self.translate(humid, self.maps['humid_to_loc'])
        return loc

    def translate_seed_range(self, seed, n):
        #return min(self.translate_seed(seed), self.translate_seed(seed + n))

        return min(self.translate_seed(s) for s in range(seed, seed+n))


    def parse(self):
        raw = self.read_input_txt(split=False)
        chunks = raw.split('\n\n')
        self.seeds = [int(s) for s in chunks[0][7:].split(' ')]
        maps = chunks[1:]
        self.maps = {}
        self.maps['seed_to_soil']   = [[int(i) for i in line.split(' ')] for line in maps[0].split('\n')[1:]]
        self.maps['soil_to_fert']   = [[int(i) for i in line.split(' ')] for line in maps[1].split('\n')[1:]]
        self.maps['fert_to_water']  = [[int(i) for i in line.split(' ')] for line in maps[2].split('\n')[1:]]
        self.maps['water_to_light'] = [[int(i) for i in line.split(' ')] for line in maps[3].split('\n')[1:]]
        self.maps['light_to_temp']  = [[int(i) for i in line.split(' ')] for line in maps[4].split('\n')[1:]]
        self.maps['temp_to_humid']  = [[int(i) for i in line.split(' ')] for line in maps[5].split('\n')[1:]]
        self.maps['humid_to_loc']   = [[int(i) for i in line.split(' ')] for line in maps[6].split('\n')[1:]]
        for name, map in self.maps.items():
            map.sort(key=lambda m: m[1])
        #print(f'seeds: {self.seeds}')
        #pprint(self.maps)

    def part1(self):
        locations = [self.translate_seed(seed) for seed in self.seeds]
        return min(locations)

    def part2(self):

        naive = False
        if naive:
            locations = []
            for sstart, slen in zip(self.seeds[0::2], self.seeds[1::2]):
                for seed in range(sstart, sstart + slen):
                    locations.append(self.translate_seed(seed))
            print(f'seeds: {self.seeds}')
            print(f'locations: {locations}')
        else:
            merged = []
            for name, map in self.maps.items():
                for map_range in map:
                    merged.append(map_range[1])
                    merged.append(map_range[1] + map_range[2]-1)
                    merged.append(map_range[1] + map_range[2])
                    merged.append(map_range[1] + map_range[2]+1)
                    merged.append(map_range[0])
                    merged.append(map_range[0] + map_range[2]-1)
                    merged.append(map_range[0] + map_range[2])
                    merged.append(map_range[0] + map_range[2]+1)
            
            merged = sorted(list(set(merged)))
            print(f'seeds {self.seeds}')
            print(f'all ranges {merged}')

            #merged = []
            ## merge all ranges
            #for rng in all_ranges:
            #    merged.append(rng[1])
            #    merged.append(rng[1]+rng[2])
            #merged = sorted(set(merged))
#
            #print(f'merged: {merged}')
            locations = []
            for sstart, slen in zip(self.seeds[0::2], self.seeds[1::2]):
                endpoints = [m for m in merged if m > sstart and m < sstart+slen-1]
                print(f'test seed {sstart}')
                locations.append(self.translate_seed(sstart-1))
                locations.append(self.translate_seed(sstart))
                locations.append(self.translate_seed(sstart+1))
                for end_seed in endpoints:
                    print(f'test seed {end_seed-1}')
                    locations.append(self.translate_seed(end_seed-1))
                    print(f'test seed {end_seed}')
                    locations.append(self.translate_seed(end_seed))
                    print(f'test seed {end_seed}')
                    locations.append(self.translate_seed(end_seed+1))
                print(f'test seed {sstart+slen-1}')
                locations.append(self.translate_seed(sstart+slen-1))
                locations.append(self.translate_seed(sstart+slen))

        print(f'locations: {locations}')

        return min(locations)
