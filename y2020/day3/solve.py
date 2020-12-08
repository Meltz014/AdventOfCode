def solve_slope(hill, width, height, slope):
    tree_count = 0
    x, y = 0, 0
    while y < height:
        tree_count += int(hill[x, y])
        x = (x + slope[0]) % width
        y += slope[1]
    return tree_count

def part1(hill, width, height):
    # find trees encounterd on slope of (3, 1)
    tree_count = solve_slope(hill, width, height, (3, 1))
    print(f'Part1: {tree_count}')

def part2(hill, width, height):
    a = solve_slope(hill, width, height, (1, 1))
    b = solve_slope(hill, width, height, (3, 1))
    c = solve_slope(hill, width, height, (5, 1))
    d = solve_slope(hill, width, height, (7, 1))
    e = solve_slope(hill, width, height, (1, 2))
    print(f'Part2: {a * b * c * d * e}')


def main():
    with open('day3\input.txt') as fid:
        lines = fid.readlines()

    # build hill map
    # dict of (x, y) = true if tree
    hill = {}
    for (y, line) in enumerate(lines):
        for (x, t) in enumerate(line.strip()):
            hill[(x, y)] = t == '#'

    width = x+1
    height = y+1
    part1(hill, width, height)
    part2(hill, width, height)

if __name__ == '__main__':
    main()