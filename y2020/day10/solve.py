
import numpy

def part1(adaptors):
    diffs = numpy.diff(adaptors)
    total = len(diffs[diffs==1]) * len(diffs[diffs==3])
    print(f'Part 1: {total}')

def part2(adaptors):
    diffs = numpy.diff(adaptors)
    # 1 x 1: 1 permutation
    # 2 x 1: 2 permutations
    # 3 x 1: 4 permutations
    # 4 x 1: 7 permutations
    threes = numpy.where(diffs==3)
    # insert a "dummy" location for a three at index 0
    threes = numpy.insert(threes, 0, -1)
    # diff of locations of 3's is the gaps between each 3.  I.e. num of consecutive 1's
    one_chunks = numpy.diff(threes) - 1
    # convert to num permutations
    perms = numpy.ones_like(one_chunks)
    perms[one_chunks==4] = 7
    perms[one_chunks==3] = 4
    perms[one_chunks==2] = 2

    print(f'Part 2: {numpy.prod(perms)}')


def main():
    adaptors = numpy.loadtxt('day10\input.txt', dtype=numpy.int64)
    example = numpy.array([28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3])
    #adaptors = numpy.sort(example)
    adaptors = numpy.sort(adaptors)
    # add 2 implicit nodes (wall outlet and device at either end)
    adaptors = numpy.insert(adaptors, 0, 0)
    adaptors = numpy.insert(adaptors, adaptors.size, adaptors[-1]+3)
    part1(adaptors)
    part2(adaptors)

if __name__ == '__main__':
    main()