from AoC import AoC
from tqdm import tqdm
from collections import defaultdict
from functools import cache


class Solver(AoC):
    example_data = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""


    def parse(self):
        self.bytes = []
        raw = self.read_input_txt()
        collec = raw[0].strip().split(', ')
        self.tests = []
        for line in raw[2:]:
            self.tests.append(line.strip())
        
        self.tqdm_total = len(self.tests)

        # organize collection into a dict by first letter
        self.collection = defaultdict(list)
        for item in collec:
            self.collection[item[0]].append(item)

        self.debug(self.collection)

    def part1(self):
        """
        BFS to find number of 9's reachable by each 0
        """
        total = 0
        self.total_p2 = 0

        @cache
        def bfs(test):
            possible = self.collection.get(test[0])
            tot = 0
            if not possible:
                return tot

            for p in possible:
                l = len(p)
                if l > len(test):
                    continue
                if test[0:l] == p:
                    if l == len(test):
                        tot += 1
                    else:
                        ret = bfs(test[l::])
                        if ret:
                            tot += ret
            return tot

        pbar = tqdm(total=self.tqdm_total, disable=self._debug)
        for t in self.tests:
            self.debug(f'Testing {t}...')
            tot = bfs(t)
            if tot:
                total += 1
                self.total_p2 += tot
                self.debug(f'PASS {tot}')
            else:
                self.debug('FAIL')

            pbar.update(1)
        pbar.close()
        return total


    def part2(self):
        """
        """
        return self.total_p2