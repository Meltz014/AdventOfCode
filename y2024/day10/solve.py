from AoC import AoC
from itertools import zip_longest
from tqdm import tqdm
import numpy as np

class Solver(AoC):
    example_data = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

    def show_grid(self, grid):
        if self._debug:
            for y, row in enumerate(grid):
                for x, char in enumerate(row):
                    print(f" {char}", end="")
                print()

    def parse(self):
        self.tqdm_total = 0
        self.grid = []
        self.trailheads = []
        raw = self.read_input_txt()
        for y, line in enumerate(raw):
            self.grid.append([])
            for x, char in enumerate(line.strip()):
                t = int(char)
                if t == 0:
                    self.trailheads.append((y,x))
                self.grid[y].append(t)
        self.bounds = (y,x)
        self.show_grid(self.grid)
        self.debug(self.trailheads)

    def part1(self):
        """
        BFS to find number of 9's reachable by each 0
        """
        total_score = 0

        def bfs(nines, coords):
            y, x = coords[0], coords[1]
            cur = self.grid[y][x]
            for dy, dx in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                ny, nx = y+dy, x+dx
                if ny >= 0 and ny <= self.bounds[0] and nx >= 0 and nx <= self.bounds[1]:
                    nxt = self.grid[ny][nx]
                    if cur == 8 and nxt == 9:
                        nines.add((ny,nx))
                    elif nxt == cur+1:
                        bfs(nines, (ny, nx))

        for y, x in self.trailheads:
            nines = set()
            bfs(nines, (y,x))
            self.debug(f"({y},{x}) -> {len(nines)}")
            total_score += len(nines)

        return total_score

    def part2(self):
        """
        """
        total_score = 0

        def bfs(nines, coords):
            y, x = coords[0], coords[1]
            cur = self.grid[y][x]
            for dy, dx in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                ny, nx = y+dy, x+dx
                if ny >= 0 and ny <= self.bounds[0] and nx >= 0 and nx <= self.bounds[1]:
                    nxt = self.grid[ny][nx]
                    if cur == 8 and nxt == 9:
                        nines.append((ny,nx))
                    elif nxt == cur+1:
                        bfs(nines, (ny, nx))

        for y, x in self.trailheads:
            nines = []
            bfs(nines, (y,x))
            self.debug(f"({y},{x}) -> {len(nines)}")
            total_score += len(nines)

        return total_score
