
import numpy

def part1(data):
    """
    Find first number in list that is not a sum of any 2 previous 25 numbers
    """
    for i in range(25, len(data)):
        start = i-25
        end = i

        valid = False
        for ii in range(start, end):
            if data[i] - data[ii] in data[start:end]:
                valid = True
                break
        if valid:
            continue
        print(f'Part 1: {data[i]}')
        return i

def part2(data, target_idx):
    total = 0
    start = 0
    end = 1
    while True:
        # move window.  If total is > target, increment start.
        # if total is < target, increment end
        total = sum(data[start:end])
        if total > data[target_idx]:
            start += 1
        elif total < data[target_idx]:
            end += 1
        else:
            break

    print(f'Part 2: {max(data[start:end]) + min(data[start:end])}')

def main():
    data = numpy.loadtxt('day9\input.txt', dtype=numpy.int64)
    target_idx = part1(data)
    part2(data, target_idx)

if __name__ == '__main__':
    main()