from AoC import AoC
import numpy as np

class Solver(AoC):
    example_data = """3,4,3,1,2"""

    def parse(self):
        self.fish = self.read_input_numeric(dtype=np.uint8, sep=',')
        self.day_rem = np.zeros(9, dtype=np.uint64)
        for f in self.fish:
            self.day_rem[f] += 1
        self.init_days = self.day_rem.copy()

    def part1(self):
        self.day_rem = self.init_days.copy()
        for i in range(80):
            # shift days rem
            self.day_rem = np.roll(self.day_rem, -1)
            # account for old fish resetting
            self.day_rem[6] += self.day_rem[-1]

        return np.sum(self.day_rem)

    def part2(self):
        day_rem = self.day_rem.copy()

        for i in range(80, 256):
            # shift days rem
            day_rem = np.roll(day_rem, -1)
            # account for old fish resetting
            day_rem[6] += day_rem[-1]

        return np.sum(day_rem)
