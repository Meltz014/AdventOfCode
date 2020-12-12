
import re
from AoC import AoC

class Solver(AoC):
    example_data = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""

    def parse(self):
        lines = self.read_input_txt()
        self.passwords = []
        for line in lines:
            m_obj = re.match(r'(?P<low>\d+)-(?P<high>\d+)\s(?P<chr>\w):\s(?P<pwd>\w+)', line)
            if m_obj:
                datum = m_obj.groupdict()
                datum['low'] = int(datum['low'])
                datum['high'] = int(datum['high'])
                self.passwords.append(datum)


    def part1(self):
        def is_valid(password):
            return password['pwd'].count(password['chr']) in range(password['low'], password['high']+1)

        return sum([1 if is_valid(password) else 0 for password in self.passwords])


    def part2(self):
        def is_valid(password):
            try:
                low_valid = (password['pwd'][password['low']-1] == password['chr'])
                high_valid = (password['pwd'][password['high']-1] == password['chr'])
            except IndexError:
                return False
            return low_valid ^ high_valid

        return sum([1 if is_valid(password) else 0 for password in self.passwords])