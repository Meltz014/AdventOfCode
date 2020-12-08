
import numpy

def part1(entries):
    current = set()
    for i in entries:
        if (2020 - i) in current:
            print(f'Part 1: {(2020 - i) * i}')
            return
        else:
            current.add(i)

def part2(entries):
    for i in entries:
        current = set()
        target = 2020 - i
        for j in entries:
            if (target - j) in current:
                print(f'Part 2: {(target - j)} + {j} + {i} = {(target - j) + j + i}')
                print(f'Part 2: {(target - j) * j * i}')
                return
            else:
                current.add(j)

def main():
    entries = numpy.loadtxt('day1\input.txt', dtype=numpy.int64)
    part1(entries)
    part2(entries)

if __name__ == '__main__':
    main()