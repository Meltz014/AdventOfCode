from AoC import AoC
import re

class Solver(AoC):
    example_data = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

    def parse(self):
        self.raw = self.read_input_txt()

    def part1(self):

        total = 0
        pattern = re.compile(r'mul\((\d+),(\d+)\)')
        for line in self.raw:
            groups = pattern.findall(line)
            for group in groups:
                total += int(group[0]) * int(group[1])
        return total

    def part2(self):
        if self._use_example:
            self.raw = ["""xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""]
        total = 0

        """doesnt work for some reason"""
        """
        mul_pattern = re.compile(r'mul\((\d+),(\d+)\)')
        disable_pattern = re.compile(r"don't\(\).*?($|do\(\))")
        for line in self.raw:
            new_line = disable_pattern.sub("", line)
            groups = mul_pattern.findall(new_line)
            print(groups)
            for group in groups:
                total += int(group[0]) * int(group[1])
        """

        pattern = re.compile(r"(mul\((\d+),(\d+)\))|(don't\(\))|(do\(\))")
        do = True
        for line in self.raw:
            groups = pattern.findall(line)
            for group in groups:
                if do:
                    if group[0]:
                        total += int(group[1]) * int(group[2])
                    elif group[3]:
                        do = False
                elif group[4]:
                    do = True

        return total
