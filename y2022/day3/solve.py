from AoC import AoC
from string import ascii_letters

class Solver(AoC):
    example_data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

    def parse(self):
        raw = self.read_input_txt(split=True)
        self.sacks = []
        for line in raw:
            line = line.strip()
            n = len(line)//2
            self.sacks.append((line[:n], line[n:]))


    def part1(self):
        tot = 0
        for (a,b) in self.sacks:
            common = (set(a) & set(b)).pop()
            tot += ascii_letters.index(common)+1
        return tot


    def part2(self):
        tot = 0
        group = []
        for (i, (a,b)) in enumerate(self.sacks):
            group.append(set(a+b))
            if i % 3 == 2:
                common = group[0] & group[1] & group[2]
                tot += ascii_letters.index(common.pop())+1
                group = []

        return tot