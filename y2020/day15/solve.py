from collections import defaultdict
from AoC import AoC
import re

class Solver(AoC):
    #example_data = '\n'.join(['1','3','2'])
    example_data = '\n'.join(['2','1','3'])

    def parse(self):
        self.starting = self.read_input_numeric()
        print(self.starting)

    def part1(self):
        nums_said = defaultdict(list)
        last_num = -1
        for (turn, n) in enumerate(self.starting):
            nums_said[n].append(turn)
            last_num = n
        for turn in range(len(self.starting), 2020):
            if len(nums_said[last_num]) > 1:
                last_num = nums_said[last_num][-1] - nums_said[last_num][-2]
            else:
                last_num = 0
            nums_said[last_num].append(turn)

        return last_num

    def part2(self):
        nums_said = defaultdict(list)
        last_num = -1
        for (turn, n) in enumerate(self.starting):
            nums_said[n].append(turn)
            last_num = n
        for turn in range(len(self.starting), 30000000):
            if len(nums_said[last_num]) > 1:
                last_num = nums_said[last_num][-1] - nums_said[last_num][-2]
            else:
                last_num = 0
            nums_said[last_num].append(turn)

        return last_num
        
