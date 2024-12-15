from AoC import AoC
from itertools import zip_longest
from tqdm import tqdm
import numpy as np

class Solver(AoC):
    example_data_1 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

    example_data = """YXY
XYX
YXY"""

    def show_grid(self, grid):
        if self._debug:
            for y, row in enumerate(grid):
                for x, char in enumerate(row):
                    print(f" {char}", end="")
                print()

    def parse(self):
        self.grid = []
        raw = self.read_input_txt()
        for y, line in enumerate(raw):
            self.grid.append([])
            for x, char in enumerate(line.strip()):
                self.grid[y].append(char)
        self.bounds = (y,x)
        self.tqdm_total = (x+1) * (y+1)
        self.show_grid(self.grid)

    def part1(self):
        """
        BFS to find number of 9's reachable by each 0
        """
        total_score = 0
        visited = set()

        def bfs(coords):
            area = 1
            perimiter = 0
            y, x = coords[0], coords[1]
            visited.add((y,x))
            cur = self.grid[y][x]
            for dy, dx in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                ny, nx = y+dy, x+dx
                if ny >= 0 and ny <= self.bounds[0] and nx >= 0 and nx <= self.bounds[1]:
                    new = self.grid[ny][nx]
                    if new != cur:
                        perimiter += 1
                        continue
                    if (ny, nx) in visited:
                        continue
                    a, p = bfs((ny, nx))
                    area += a
                    perimiter += p
                else:
                    perimiter += 1
            return area, perimiter

        pbar = tqdm(total=self.tqdm_total, ncols=100)

        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                if (y,x) not in visited:
                    a, p = bfs((y,x))
                    total_score += a * p
                pbar.update(1)
        pbar.close()
        return total_score

    def part2(self):
        """
        """
        total_score = 0
        visited = set()

        def corner_detect(y, x):
            tot = 0
            cur = self.grid[y][x]
            def peek_in_plot(yy, xx):
                if yy >= 0 and yy <= self.bounds[0] and xx >= 0 and xx <= self.bounds[1]:
                    if self.grid[yy][xx] == cur:
                        return True
                return False
            
            for corner_test in [
                [(1,0), (1,1), (0,1)],     # bottom right
                [(1,0), (1,-1), (0,-1)],   # bottom left
                [(0,-1), (-1,-1), (-1,0)], # top left
                [(-1,0), (-1,1), (0,1)]    # top right
            ]:
                test = []
                for dy,dx in corner_test:
                    test.append(peek_in_plot(y+dy, x+dx))
                if test == [False, False, False] or test == [True, False, True] or test == [False, True, False]:
                    tot += 1
            return tot

        def bfs(coords):
            area = 1
            corners = corner_detect(*coords)
            self.debug(f'{coords}: {corners} corners')
            y, x = coords[0], coords[1]
            visited.add((y,x))
            cur = self.grid[y][x]
            for dy, dx in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                ny, nx = y+dy, x+dx
                if ny >= 0 and ny <= self.bounds[0] and nx >= 0 and nx <= self.bounds[1]:
                    new = self.grid[ny][nx]
                    if new != cur:
                        continue
                    if (ny, nx) in visited:
                        continue
                    a, c = bfs((ny, nx))
                    area += a
                    corners += c
            return area, corners

        pbar = tqdm(total=self.tqdm_total, ncols=100)

        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                if (y,x) not in visited:
                    a, c = bfs((y,x))
                    total_score += a * c
                pbar.update(1)
        pbar.close()
        return total_score
