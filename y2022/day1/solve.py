from AoC import AoC
import numpy as np

class Solver(AoC):
    example_data = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

    def parse(self):
        raw = self.read_input_txt(split=True)
        self.elves = []
        elf = []
        for line in raw:
            line = line.strip()
            if not line:
                self.elves.append(elf)
                elf = []
                continue
            elf.append(int(line))


    def part1(self):
        self.ranked = sorted(self.elves, key=sum)
        return sum(self.ranked[-1])

    def part2(self):
        return sum(sum(e) for e in self.ranked[-3:])