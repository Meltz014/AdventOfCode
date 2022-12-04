from AoC import AoC
import re

class Solver(AoC):
    example_data = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

    def parse(self):
        raw = self.read_input_txt(split=True)
        self.ranges = []
        for line in raw:
            a, b, c, d = re.split(',|-',line.strip())
            ra = range(int(a), int(b)+1)
            rb = range(int(c), int(d)+1)
            self.ranges.append((set(ra), set(rb)))

    def part1(self):
        tot = 0
        for (sa, sb) in self.ranges:
            if (not sa - sb) or not (sb - sa):
                tot+=1
        return tot

    def part2(self):
        tot = 0
        for (sa, sb) in self.ranges:
            if (sa & sb):
                tot+=1
        return tot