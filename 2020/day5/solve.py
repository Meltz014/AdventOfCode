
import numpy

def part1(seats):
    print(f'Part 1: {max(seats)}')

def part2(seats):
    max_id = max(seats)
    min_id = min(seats)

    existing = set(seats)
    missing = set(range(min_id, max_id+1)) - existing
    print(f'Part 2: {missing}')

def main():
    with open('day5\input.txt') as fid:
        data = fid.readlines()

    seats = [] # (row, col, id)
    for line in data:
        # F is 0, B is 1
        # L is 0, R is 1
        id_bin = line[:10].replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1')
        seats.append(int(id_bin, 2))

    part1(seats)
    part2(seats)

if __name__ == '__main__':
    main()