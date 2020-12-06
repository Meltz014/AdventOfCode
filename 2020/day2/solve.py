
import re


def part1(passwords):
    def is_valid(password):
        return password['pwd'].count(password['chr']) in range(password['low'], password['high']+1)

    print('Part1: ', end='') 
    print(sum([1 if is_valid(password) else 0 for password in passwords]))


def part2(passwords):
    def is_valid(password):
        try:
            low_valid = (password['pwd'][password['low']-1] == password['chr'])
            high_valid = (password['pwd'][password['high']-1] == password['chr'])
        except IndexError:
            return False
        return low_valid ^ high_valid
    
    print('Part2: ', end='') 
    print(sum([1 if is_valid(password) else 0 for password in passwords]))


def main():
    with open('day2\input.txt') as fid:
        lines = fid.readlines()

    data = []
    for line in lines:
        m_obj = re.match(r'(?P<low>\d+)-(?P<high>\d+)\s(?P<chr>\w):\s(?P<pwd>\w+)', line)
        if m_obj:
            datum = m_obj.groupdict()
            datum['low'] = int(datum['low'])
            datum['high'] = int(datum['high'])
            data.append(datum)
    part1(data)
    part2(data)

if __name__ == '__main__':
    main()