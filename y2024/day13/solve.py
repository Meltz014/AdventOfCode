from AoC import AoC
from tqdm import tqdm
import re
from itertools import combinations_with_replacement

class Solver(AoC):
    example_data = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""



    def parse(self):
        self.prizes = [] # {'a': (x,y), 'b': (x,y), 'target': (x,y)}
        raw = self.read_input_txt()
        prize = None
        btn_pat = re.compile(r'Button \w: X\+(\d+), Y\+(\d+)')
        pize_pat = re.compile(r'Prize: X=(\d+), Y=(\d+)')
        for line in raw:
            if 'Button A' in line:
                prize = {}
                m_obj = btn_pat.match(line.strip())
                print(m_obj.groups())
                prize['a'] = (int(m_obj.group(1)), int(m_obj.group(2)))
            elif 'Button B' in line:
                m_obj = btn_pat.match(line.strip())
                prize['b'] = (int(m_obj.group(1)), int(m_obj.group(2)))
            elif 'Prize' in line:
                m_obj = pize_pat.match(line.strip())
                prize['target'] = (int(m_obj.group(1)), int(m_obj.group(2)))
                self.prizes.append(prize)
                prize = None
        self.debug(self.prizes)


    def part1(self):
        """
        """
        total_score = 0

        for prize in self.prizes:
            # find min and max num of presses
            min_x = min(prize['target'][0] // prize['a'][0], prize['target'][0] // prize['b'][0])
            max_x = max(prize['target'][0] // prize['a'][0], prize['target'][0] // prize['b'][0])
            min_y = min(prize['target'][1] // prize['a'][1], prize['target'][1] // prize['b'][1])
            max_y = max(prize['target'][1] // prize['a'][1], prize['target'][1] // prize['b'][1])
            self.debug(f'min_x: {min_x}, max_x: {max_x}, min_y: {min_y}, max_y: {max_y}')
            min_btn = min(min_x, min_y)
            max_btn = min(max(max_x, max_y), 200)
            self.debug(f'min_btn: {min_btn}, max_btn: {max_btn}')
            found = False
            for sa in range(101):
                for sb in range(101):
                    if sa+sb < min_btn:
                        continue

                    #self.debug(f'sa: {sa}, sb: {sb}')
                    if sa * prize['a'][0] + sb * prize['b'][0] == prize['target'][0] and \
                        sa * prize['a'][1] + sb * prize['b'][1] == prize['target'][1]:
                        found = True
                        self.debug(f'FOUND {sa}, {sb}')
                        total_score += 3*sa + sb
                        break
                if found:
                    break

        return total_score

    def part2(self):
        """
        """
        total_score = 0
        evil = 10000000000000
        for prize in self.prizes:
            # find min and max num of presses
            tx = prize['target'][0] + evil
            ty = prize['target'][1] + evil
            ax, ay = prize['a']
            bx, by = prize['b']
            # linear equation with two vars
            # ty = a * ay + b * by
            # tx = a * ax + b * bx
            # b = (ty - a * ay) / by
            a = (bx * ty - by * tx)/(bx * ay - by * ax)
            b = (ty - a * ay) / by
            if int(a) == a and int(b) == b:
                total_score += 3*int(a) + int(b)

        return total_score
