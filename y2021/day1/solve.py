from AoC import AoC
import numpy as np

class Solver(AoC):
    example_data = """199
200
208
210
200
207
240
269
260
263"""

    def parse(self):
        self.readings = self.read_input_numeric()

    def part1(self):
        return np.sum(np.diff(self.readings) > 0)

    def part2(self):
        conv = np.convolve(self.readings, np.ones(3, dtype=int), 'valid')
        return np.sum(np.diff(conv) > 0)