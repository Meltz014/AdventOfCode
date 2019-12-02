
import numpy

def find_fuel(masses):
    fuel = masses // 3 - 2
    fuel[fuel < 0] = 0
    if numpy.sum(fuel) == 0:
        return fuel
    return fuel + find_fuel(fuel)

def part1(masses):
    fuel = (masses // 3) - 2
    print(f'Part 1: {numpy.sum(fuel)}')

def part2(masses):
    full = find_fuel(masses)
    print(f'Part 2: {numpy.sum(full)}')

def main():
    masses = numpy.loadtxt('input.txt', dtype=numpy.int64)
    part1(masses)
    part2(masses)

main()