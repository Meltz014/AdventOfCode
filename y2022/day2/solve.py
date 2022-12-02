from AoC import AoC
import numpy as np


TRANS = str.maketrans({
    'A': '0',
    'X': '0',
    'B': '1',
    'Y': '1',
    'C': '2',
    'Z': '2'
})

SC_WIN = 6
SC_TIE = 3
SC_LOS = 0

def outcome(opp, me):
    result = (int(me) - int(opp)) % 3
    return SC_WIN if result == 1 else SC_TIE if result == 0 else SC_LOS


class Solver(AoC):
    example_data = """A Y
B X
C Z"""

    def parse(self):
        raw = self.read_input_txt(split=True)
        self.strategy = []
        for line in raw:
            self.strategy.append(line.strip().translate(TRANS).split(' '))


    def part1(self):
        tot = 0

        for (opp, me) in self.strategy:
            tot += outcome(opp, me) +int(me) + 1
        return tot


    def part2(self):
        # add 2 for loss, add 1 for win, add 0 for tie
        # "0" - loose, "1" - draw, "2" - win
        ops = {
            "0": 2, # loss
            "1": 0, # draw
            "2": 1  # win
        }

        tot = 0
        for (opp, out) in self.strategy:
            me = ((int(opp) + ops[out]) % 3)
            tot += me + 1 + outcome(opp, me)

        return tot