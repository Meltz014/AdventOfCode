from AoC import AoC
import numpy as np
from scipy.signal import argrelmin
import matplotlib.pyplot as plt


class Solver(AoC):
    example_data = """2199943210
3987894921
9856789892
8767896789
9899965678"""

    def parse(self):
        raw = self.read_input_txt()
        # going to create a border of 9's around the grid
        width = len(raw[0].strip('\n'))+2
        height = len(raw)+2
        self.grid = np.zeros((height, width), np.uint8)
        for (y, row) in enumerate(raw):
            for (x, val) in enumerate(row.strip('\n')):
                self.grid[y+1,x+1] = int(val)
        self.grid[:,0] = 9
        self.grid[:,-1] = 9
        self.grid[0,:] = 9
        self.grid[-1,:] = 9
        #plt.imshow(self.grid)
        #plt.show()


    def part1(self):
        horiz = argrelmin(self.grid, axis=0)
        vert = argrelmin(self.grid, axis=1)
        horiz_pts = set([(y,x) for (y,x) in zip(*horiz)])
        vert_pts = set([(y,x) for (y,x) in zip(*vert)])
        self.local_min = horiz_pts & vert_pts
        local_min_seq = tuple(zip(*self.local_min))
        risk = (self.grid[local_min_seq] + 1).sum()
        return risk

    def part2(self):
        basins = []
        for bottom in self.local_min:
            queue = [bottom]
            visited = [bottom]
            basin_size = 0
            while queue:
                pt = queue.pop()
                if self.grid[pt] != 9:
                    basin_size += 1
                    newpt = (pt[0] + 1, pt[1])
                    if newpt not in visited:
                        queue.append(newpt)
                        visited.append(newpt)
                    newpt = (pt[0] - 1, pt[1])
                    if newpt not in visited:
                        queue.append(newpt)
                        visited.append(newpt)
                    newpt = (pt[0], pt[1] + 1)
                    if newpt not in visited:
                        queue.append(newpt)
                        visited.append(newpt)
                    newpt = (pt[0], pt[1] - 1)
                    if newpt not in visited:
                        queue.append(newpt)
                        visited.append(newpt)
            basins.append(basin_size)
        return np.prod(sorted(basins)[-3:])