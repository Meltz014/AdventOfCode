from AoC import AoC
import numpy as np
import sys
import time

class Solver(AoC):
    example_data = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

    example_data_1 = """11111
19991
19191
19991
11111"""

    def parse(self):
        raw = self.read_input_txt()
        width = len(raw[0].strip('\n'))
        height = len(raw)
        self.grid = np.zeros((height, width), np.uint8)
        for (y, row) in enumerate(raw):
            for (x, val) in enumerate(row.strip('\n')):
                self.grid[y,x] = int(val)

    def incr_point(self, y, x, flashers):
        if (0 <= y < self.grid.shape[0]) and (0 <= x < self.grid.shape[1]):
            self.grid[y,x] += 1
            if self.grid[y,x] >= 10 and (y,x) not in flashers:
                flashers.append((y,x))

    def step(self):
        # increment everything by 1
        self.grid += 1
        flashers = []
        done = False
        # find 10's
        new_flash = self.grid == 10
        #print(new_flash)
        if not np.any(new_flash):
            return 0
        new_flash_idx = np.where(new_flash)
        for (y, x) in zip(*new_flash_idx):
            flashers.append((y,x))

        flash_idx = 0
        while flash_idx < len(flashers):
            (y, x) = flashers[flash_idx]
            flash_idx += 1
            self.incr_point(y-1, x, flashers)
            self.incr_point(y, x-1, flashers)
            self.incr_point(y-1, x-1, flashers)
            self.incr_point(y+1, x, flashers)
            self.incr_point(y, x+1, flashers)
            self.incr_point(y+1, x+1, flashers)
            self.incr_point(y+1, x-1, flashers)
            self.incr_point(y-1, x+1, flashers)
        # set all flashers back to 0
        self.grid[self.grid>=10] = 0
        return len(flashers)

    def print_grid(self, clear=True):
        if clear:
            sys.stdout.write('\b' * len(str(self.grid)) + str(self.grid))
            sys.stdout.flush()
            time.sleep(0.1)
        else:
            print(self.grid)

    def part1(self):
        n_flash = 0
        for i in range(100):
            n_flash += self.step()
        #print(self.grid)
        return n_flash

    def part2(self):
        cur_step = 100
        #self.print_grid(clear=False)
        while True:
            flashers = self.step()
            #self.print_grid()
            cur_step += 1
            if flashers == self.grid.size:
                return cur_step