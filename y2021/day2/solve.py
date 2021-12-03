from AoC import AoC
import numpy as np

class Solver(AoC):
    example_data = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""

    def parse(self):
        data = self.read_input_txt()
        clean = lambda x: (x[0][0], int(x[1].strip('\n')))
        self.inst = [clean(cmd.split()) for cmd in data]

    def part1(self):
        self.x = 0
        self.z = 0
        for (direction, n) in self.inst:
            if direction == 'f':
                self.x += n
            elif direction == 'u':
                self.z -= n
            elif direction == 'd':
                self.z += n
        return self.x * self.z


    def part2(self):
        self.x = 0
        self.z = 0
        self.aim = 0

        for (direction, n) in self.inst:
            if direction == 'f':
                self.x += n
                self.z += n * self.aim
            elif direction == 'u':
                self.aim -= n
            elif direction == 'd':
                self.aim += n

        return self.x * self.z