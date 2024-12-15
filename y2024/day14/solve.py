from AoC import AoC
from tqdm import tqdm
import re
import numpy as np
from matplotlib import pyplot as plt

class Solver(AoC):
    example_data = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

    def parse(self):
        self.tqdm_total = 0
        self.robots = []
        self.bounds = (103,101)
        if self._use_example:
            self.bounds = (7,11)
        raw = self.read_input_txt()
        pat = re.compile(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)')
        for line in raw:
            m_obj = pat.match(line.strip())
            px, py, vx, vy = m_obj.groups()
            bot = {'pos': (int(py), int(px)), 'vel': (int(vy), int(vx))}
            self.robots.append(bot)

        self.debug(self.robots)

    def tick(self):
        for bot in self.robots:
            py, px = bot['pos']
            vy, vx = bot['vel']
            bot['pos'] = (py + vy) % self.bounds[0], (px + vx) % self.bounds[1]

    def part1(self):
        """
        """
        total_score = 0
        for _ in range(100):
            self.tick()

        # build grid
        grid = np.zeros(self.bounds, dtype=np.uint16)
        for bot in self.robots:
            grid[bot['pos']] += 1
        quad_size = (self.bounds[0]//2, self.bounds[1]//2)
        total_score = np.sum(grid[0:quad_size[0], 0:quad_size[1]])
        total_score *= np.sum(grid[-quad_size[0]:, -quad_size[1]:])
        total_score *= np.sum(grid[0:quad_size[0], -quad_size[1]:])
        total_score *= np.sum(grid[-quad_size[0]:, 0:quad_size[1]])
        return total_score

    def part2(self):
        """
        """
        total_score = 0
        self.parse()
        n = 10000
        i = 0
        center_counts = []
        center_range = slice(self.bounds[0]//2-15, self.bounds[0]//2+16), slice(self.bounds[1]//2-15, self.bounds[1]//2+16)
        pbar = tqdm(total=n, ncols=100)
        for i in range(n):
            self.tick()
            grid = np.zeros(self.bounds, dtype=np.uint16)
            for bot in self.robots:
                grid[bot['pos']] += 1
            center_counts.append(np.sum(grid[center_range]))
            pbar.update(1)
        pbar.close()
        m_count = max(center_counts)
        m_i = center_counts.index(m_count)
        print(f'Max counts after {n} ticks: {m_count} at time {m_i+1}')

        self.parse()
        for i in range(m_i+1):
            self.tick()

        grid = np.zeros(self.bounds, dtype=np.uint16)
        for bot in self.robots:
            grid[bot['pos']] += 1
        plt.imshow(grid)
        plt.show()
        return m_i+1

