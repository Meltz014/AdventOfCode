
import math
import numpy
from AoC import AoC


class Solver(AoC):
    example_data = """939
7,13,x,x,59,x,31,19"""

    def parse(self):
        lines = self.read_input_txt()
        self.my_time = int(lines[0])
        self.raw_buses = [int(i) if i!='x' else 'x' for i in lines[1].split(',')]
        self.buses = [i for i in self.raw_buses if i != 'x']
        print(self.my_time)
        print(self.raw_buses)
        print(self.buses)

    def part1(self):
        min_waited = [(abs(self.my_time % (-1 * x)), x) for x in self.buses]
        ans = min(min_waited)
        print(ans)
        return ans[0] * ans[1]

    def part2(self):
        # all ID's are prime.  Search on product of everything
        max_id = numpy.prod(self.buses)

        t_off = 0 #self.raw_buses.index(max_id)
        coef = 1
        print('0' * 16, end='')
        while True:
            # search on multiples of max bus id
            # offset to find actual t
            t = (coef * max_id) - t_off
            if coef % 100 == 0:
                print('\b' * 16 + f't: {t:013}', end='')
            # check other buses line up
            valid = True
            for (other_off, other) in enumerate(self.raw_buses):
                if other == 'x':
                    continue
                if (t + other_off) % other != 0:
                    valid = False
                    break
            if valid:
                return t
            coef += 1