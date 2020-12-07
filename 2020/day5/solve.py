
import numpy

def part1(seats):
    target = max(seats, key=lambda x: x[2])
    print(f'Part 1: {target[2]}')

def part2(seats):
    max_id = max(seats, key=lambda x: x[2])[2]
    min_id = min(seats, key=lambda x: x[2])[2]

    existing = set([seat[2] for seat in seats])
    missing = set(range(min_id, max_id+1)) - existing
    print(f'Part 2: {missing}')

def main():
    with open('day5\input.txt') as fid:
        data = fid.readlines()

    seats = [] # (row, col, id)
    for line in data:
        # F is 0, B is 1
        row_bin = line[:7].replace('F', '0').replace('B', '1')
        # L is 0, R is 1
        col_bin = line[7:10].replace('L', '0').replace('R', '1')
        (row, col) = (int(row_bin, 2), int(col_bin, 2))
        seats.append((row, col, row*8 + col))

    part1(seats)
    part2(seats)

if __name__ == '__main__':
    main()