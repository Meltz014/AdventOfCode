from AoC import AoC
import numpy as np

class Solver(AoC):
    example_data = """2x3x4
1x1x10"""

    def parse(self):
        raw = self.read_input_txt()
        self.boxes = np.zeros((len(raw), 3), dtype=np.uint32)
        for (i, line) in enumerate(raw):
            self.boxes[i,:] = sorted([int(b) for b in line.split('x')])
        print(self.boxes.shape)

    def part1(self):
        side_a = self.boxes[:,0] * self.boxes[:,1]
        side_b = self.boxes[:,1] * self.boxes[:,2]
        side_c = self.boxes[:,0] * self.boxes[:,2]
        return (3*side_a + 2*side_b + 2*side_c).sum()

    def part2(self):
        bows = self.boxes[:,0] * 2 + self.boxes[:,1] * 2 + np.multiply.reduce(self.boxes, axis=1)
        return bows.sum()
