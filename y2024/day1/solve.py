from AoC import AoC
import numpy as np
from collections import Counter


class Solver(AoC):
    example_data = """3   4
4   3
2   5
1   3
3   9
3   3"""

    def parse(self):
        self.raw = self.read_input_numeric(dtype=np.int64)
        self.raw = np.reshape(self.raw, (-1, 2))


    def part1(self):
        l = self.raw.T[0,:]
        r = self.raw.T[1,:]
        l = np.sort(l)
        r = np.sort(r)
        dif = np.abs(l - r)
        return dif.sum()

    def part2(self):
        l = self.raw.T[0,:]
        r = self.raw.T[1,:]
        counts = Counter(r)
        l_counts = np.array([counts[ll] for ll in l], dtype=np.int64)
        return sum(l * l_counts)
