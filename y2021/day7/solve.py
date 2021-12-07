from AoC import AoC
import numpy as np

class Solver(AoC):
    example_data = """16,1,2,0,4,2,7,1,2,100"""

    def total_fuel(self, target, pt_2=False):
        if pt_2:
            dist = np.absolute(self.crabs - target)
            return ((dist*(dist+1))//2).sum()
        else:
            return np.absolute(self.crabs - target).sum()

    def parse(self):
        self.crabs = self.read_input_numeric(dtype=np.int32, sep=',')

    def part1(self):
        return min([self.total_fuel(i) for i in range(self.crabs.min(), self.crabs.max()+1)])

    def part2(self):
        pass
        return min([self.total_fuel(i, pt_2=True) for i in range(min(self.crabs), max(self.crabs)+1)])
