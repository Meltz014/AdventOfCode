from AoC import AoC

class Solver(AoC):
    example_data = """1721
979
366
299
675
1456"""

    def parse(self):
        self.entries = self.read_input_numeric()

    def part1(self):
        current = set()
        for i in self.entries:
            if (2020 - i) in current:
                return (2020 - i) * i
            else:
                current.add(i)

    def part2(self):
        for i in self.entries:
            current = set()
            target = 2020 - i
            for j in self.entries:
                if (target - j) in current:
                    #print(f'Part 2: {(target - j)} + {j} + {i} = {(target - j) + j + i}')
                    return (target - j) * j * i
                else:
                    current.add(j)
