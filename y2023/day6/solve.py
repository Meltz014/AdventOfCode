from AoC import AoC
import numpy as np
import re
import math


class Solver(AoC):
    example_data = """Time:      7  15   30
Distance:  9  40  200"""

    def parse(self):
        raw = self.read_input_txt(split=True)
        self.times = [int(t) for t in re.findall(r'(\d+)', raw[0])]
        self.dists = [int(d) for d in re.findall(r'(\d+)', raw[1])]


    def part1(self):
        beat_methods = []
        for (race_time, record_dist) in zip(self.times, self.dists):
            # dist = t * (race_time - t)
            # dist = t * race_time - t*t
            # t = (1/2) * (r +/- sqrt(r**2 - 4d))
            record_hold_time_a = (1/2) * (race_time + math.sqrt(race_time ** 2 - 4 * record_dist))
            record_hold_time_b = (1/2) * (race_time - math.sqrt(race_time ** 2 - 4 * record_dist))
            print(record_hold_time_a, record_hold_time_b)
            upper = max(record_hold_time_a, record_hold_time_b)
            lower = min(record_hold_time_a, record_hold_time_b)
            num_btwn = math.floor(upper) - math.ceil(lower) + 1
            if math.isclose(upper, int(upper)):
                num_btwn -= 1
            if math.isclose(lower, int(lower)):
                num_btwn -= 1
            beat_methods.append(num_btwn)
        return np.prod(beat_methods)

    def part2(self):
        race_time = int(''.join([str(s) for s in self.times]))
        record_dist = int(''.join([str(s) for s in self.dists]))
        record_hold_time_a = (1/2) * (race_time + math.sqrt(race_time ** 2 - 4 * record_dist))
        record_hold_time_b = (1/2) * (race_time - math.sqrt(race_time ** 2 - 4 * record_dist))
        print(record_hold_time_a, record_hold_time_b)
        upper = max(record_hold_time_a, record_hold_time_b)
        lower = min(record_hold_time_a, record_hold_time_b)
        num_btwn = math.floor(upper) - math.ceil(lower) + 1
        if math.isclose(upper, int(upper)):
            num_btwn -= 1
        if math.isclose(lower, int(lower)):
            num_btwn -= 1

        return num_btwn
