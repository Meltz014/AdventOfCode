from AoC import AoC
from copy import deepcopy
import numpy as np
import re

class Solver(AoC):
    example_data = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

    def parse(self):
        raw = self.read_input_txt(split=True)
        num_stacks = 0
        stacks = []
        self.ops = []
        for (i,line) in enumerate(raw):
            if '[' not in line:
                break
            if num_stacks == 0:
                num_stacks = len(line) // 4
            spl = list(line[1::4])
            stacks.append(spl)

        for line in raw[i+2:]:
            nums = re.findall(r'\d+', line)
            self.ops.append(tuple(int(n) for n in nums))

        stacks = np.array(stacks)
        self.stacks = [list(stacks[:,i])[::-1] for i in range(stacks.shape[1])]
        # clear emptys
        for stack in self.stacks:
            while stack[-1] == ' ':
                stack.pop()

    def part1(self):
        tot = 0
        stacks = deepcopy(self.stacks)
        for (move, frm, to) in self.ops:
            for i in range(move):
                stacks[to-1].append(stacks[frm-1].pop())
        tot = ''.join(s[-1] for s in stacks)

        return tot

    def part2(self):
        stacks = deepcopy(self.stacks)
        for (move, frm, to) in self.ops:
            stacks[to-1].extend(stacks[frm-1][-move::])
            stacks[frm-1] = stacks[frm-1][:-move]
        tot = ''.join(s[-1] for s in stacks)
        return tot