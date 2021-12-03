from AoC import AoC
import numpy as np

class Solver(AoC):
    example_data = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

    def parse(self):
        raw = self.read_input_txt()
        # 2d array of bit vals
        self.readings = np.array([[int(c) for c in line.strip('\n')] for line in raw])

    def part1(self):
        gamma = np.sum(self.readings, axis=0) > (self.readings.shape[0] / 2)
        gamma_str = ''.join([str(int(g)) for g in gamma])
        epsilon_str = ''.join([str(int(not g)) for g in gamma])
        return int(gamma_str, 2) * int(epsilon_str, 2)

    def part2(self):
        # loop through bits, filter data based on most/least common bit found

        # oxygen - keep most common (1 in case of tie)
        # co2 - keep least common (0 in case of tie)
        o2_data = np.copy(self.readings)
        co2_data = np.copy(self.readings)
        for i in range(self.readings.shape[1]):
            if o2_data.shape[0] > 1:
                bit = int(np.sum(o2_data, axis=0)[i] >= o2_data.shape[0] / 2)
                o2_data = o2_data[o2_data[:,i] == bit]
            if co2_data.shape[0] > 1:
                bit = int(np.sum(co2_data, axis=0)[i] < co2_data.shape[0] / 2)
                co2_data = co2_data[co2_data[:,i] == bit]
        oxy = ''.join([str(int(g)) for g in o2_data[0]])
        co2 = ''.join([str(int(g)) for g in co2_data[0]])

        return int(oxy, 2) * int(co2, 2)

