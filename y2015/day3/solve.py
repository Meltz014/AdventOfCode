from AoC import AoC

class Solver(AoC):
    example_data = """^>V<"""

    def parse(self):
        pass

    def part1(self):
        return self.instructions.count('(') - self.instructions.count(')')

    def part2(self):
        floor = 0
        for (i, inst) in enumerate(self.instructions):
            if inst == '(':
                floor += 1
            else:
                floor -= 1
            if floor == -1:
                return i+1

        return None
