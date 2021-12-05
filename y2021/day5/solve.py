from AoC import AoC
import numpy as np

class Vector:
    def __init__(self, x1, y1, x2, y2):
        self.x_step = 1 if x1 <= x2 else -1
        self.y_step = 1 if y1 <= y2 else -1
        self.start = np.array([x1, y1], dtype=np.uint32)
        self.end = np.array([x2, y2], dtype=np.uint32)
        self.min_x = min([self.start[0], self.end[0]])
        self.min_y = min([self.start[1], self.end[1]])
        self.max_x = max([self.start[0], self.end[0]])
        self.max_y = max([self.start[1], self.end[1]])

    def is_horiz(self):
        return self.start[1] == self.end[1]

    def is_vert(self):
        return self.start[0] == self.end[0]

    def get_points(self):
        return (range(self.start[0], self.end[0] + self.x_step, self.x_step),
                range(self.start[1], self.end[1] + self.y_step, self.y_step))

    def get_slice(self):
        # only for Part 1
        return (slice(self.min_x, self.max_x+1), slice(self.min_y, self.max_y+1))

    def __str__(self):
        return f'{self.start[0]},{self.start[1]} -> {self.end[0]},{self.end[1]}'

class Solver(AoC):
    example_data = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

    def parse(self):
        raw = self.read_input_txt()
        self.vectors = []
        for line in raw:
            (start, end) = line.split(' -> ')
            (x1, y1) = start.split(',')
            (x2, y2) = end.split(',')
            self.vectors.append(Vector(int(x1), int(y1), int(x2), int(y2)))
        x = max(self.vectors, key=lambda v: v.max_x).max_x
        y = max(self.vectors, key=lambda v: v.max_y).max_y
        self.grid = np.zeros((x+1, y+1), dtype=np.uint32)

    def reset(self):
        self.grid[:,:] = 0

    def part1(self):
        for v in self.vectors:
            if v.is_horiz() or v.is_vert():
                self.grid[v.get_slice()] += 1
        return np.sum(self.grid > 1)

    def part2(self):
        self.reset()
        for v in self.vectors:
            self.grid[v.get_points()] += 1
        return np.sum(self.grid > 1)
