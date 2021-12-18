from AoC import AoC
import numpy as np
import matplotlib.pyplot as plt
import itertools

def pos(vi, a, t):
    return sum(range(vi, vi+(t*a), a))

def max_pos(vi):
    return int((1/2) * (vi)*(vi+1))

class Solver(AoC):
    example_data = """"""

    def parse(self):
        if self._use_example:
            self.target = (range(20, 30+1), range(-10, -5+1))
        else:
            self.target = (range(25, 67+1), range(-260, -200+1))

    def is_valid_vi(self, vi_x, vi_y):
        x, y = vi_x, vi_y
        while True:
            if x > max(self.target[0]) or y < min(self.target[1]):
                return False

            if x in self.target[0] and y in self.target[1]:
                return True
            if vi_x > 0:
                vi_x -= 1
                x += vi_x
            vi_y -= 1
            y += vi_y

    def part1(self):
        return max_pos(-1*min(self.target[1])-1)

    def part2(self):
        max_y = -1 * min(self.target[1])
        min_y = min(self.target[1])
        max_x = max(self.target[0])+1
        min_x = int((min(self.target[0])*2)**0.5)
        valid_count = 0
        max_t = 0
        for (x,y) in itertools.product(range(min_x, max_x), range(min_y, max_y)):
            is_valid = self.is_valid_vi(x,y)
            valid_count += 1 if is_valid else 0

        return valid_count