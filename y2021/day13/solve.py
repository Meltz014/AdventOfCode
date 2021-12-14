from AoC import AoC
import numpy as np

class Solver(AoC):
    example_data = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

    def parse(self):
        raw = self.read_input_txt()
        grid_done = False
        grid_ = []
        self.folds = []
        for line in raw:
            if line == '\n':
                grid_done = True
                continue
            if not grid_done:
                (x,y) = line.strip('\n').split(',')
                grid_.append((int(x), int(y)))
            else:
                l = line.strip('fold along ').strip('\n')
                (axis, val) = l.split('=')
                self.folds.append((axis, int(val)))

        max_x = max(grid_, key=lambda coord: coord[0] )[0] + 1
        max_y = max(grid_, key=lambda coord: coord[1] )[1] + 1
        self.grid = np.zeros((max_y, max_x), dtype=np.bool8)
        for (x,y) in grid_:
            self.grid[y,x] = True

    def print_grid(self):
        for row in self.grid:
            print(''.join('#' if r else ' ' for r in row))

    def fold(self, axis, val):
        """
        Very confusing prompt...the "fold line" is *always* discarded.
        Fold lines aren't necessairliy right in the middle
        Better logic examples in 1D:
        [0 0 0 0 0 1 0 1] fold at i=4 ==> 
            throw away idx 4: [0 0 0 0 x 1 0 1], 
            mirror about x: [0 1 0 1 x]
            drop x: [0 1 0 1]

        [0 0 0 0 1 0 1] fold at i=5 ==>
            throw away idx 5: [0 0 0 0 0 x 0 1]
            mirror about x: [0 0 0 1 0 x]
            throw away x: [0 0 0 1 0]
        """
        if axis == 'x':
            mirror = self.grid[:,-1:val:-1]
            start = val - mirror.shape[1]
            self.grid[:, start:val] += mirror
            self.grid = self.grid[:, 0:val]
        if axis == 'y':
            mirror = self.grid[-1:val:-1,:]
            start = val - mirror.shape[0]
            self.grid[start:val,:] += mirror
            self.grid = self.grid[0:val,:]

    def part1(self):
        self.fold(*self.folds.pop(0))
        return np.sum(self.grid)

    def part2(self):
        while self.folds:
            self.fold(*self.folds.pop(0))
        self.print_grid()
