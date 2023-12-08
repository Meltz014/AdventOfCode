from AoC import AoC
import numpy as np
TRANS = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'zero': '0'
}


class Solver(AoC):
    example_data = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

    def parse(self):
        self.raw = self.read_input_txt(split=True)


    def part1(self):
        #_sum = 0
        #for line in self.raw:
        #    digits = ''
        #    for c in line:
        #        if c.isnumeric():
        #            digits += c
        #    num = int(digits[0]+digits[-1])
        #    _sum += num
        #return _sum
        return 0

    def part2(self):
        _sum = 0
        for line in self.raw:

            digits = ''
            for (i, c) in enumerate(line):
                if c.isnumeric():
                    digits += c
                for t in TRANS:
                    if line[i::].find(t) == 0:
                        digits += TRANS[t]
            print(digits)
            num = int(digits[0]+digits[-1])
            _sum += num
        return _sum
