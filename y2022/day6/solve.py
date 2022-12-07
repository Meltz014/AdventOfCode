from AoC import AoC

class Solver(AoC):
    example_data = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""

    def parse(self):
        raw = self.read_input_txt(split=True)
        self.signal = raw[0].strip()
        print(self.signal)


    def part1(self):
        tot = 0
        for i in range(len(self.signal[:-3])):
            if len(set(self.signal[i:i+4])) == 4:
                tot = i+4
                break
        return tot


    def part2(self):
        tot = 0
        for i in range(len(self.signal[:-13])):
            if len(set(self.signal[i:i+14])) == 14:
                tot = i+14
                break
        return tot