from copy import deepcopy
example = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".splitlines()

EMPTY = False
FULL = True

def count_adj_full(grid, x, y, w, h, part2):
    # a  b  c
    # d  .  e
    # f  g  h
    count = 0

    incr = [
        (-1, -1), # a
        (0, -1),  # b
        (1, -1),  # c
        (-1, 0),  # d
        (1, 0),   # e
        (-1, 1),  # f
        (0, 1),   # g
        (1, 1),   # h
    ]

    for (dx, dy) in incr:
        if part2:
            subx = x
            suby = y
            while (subx in range(w)) and (suby in range(h)):
                subx += dx
                suby += dy
                seat = grid.get((subx, suby), None)
                if seat is not None:
                    if seat:
                        count += 1
                    break
        else:
            if grid.get((x+dx, y+dy)):
                count += 1
    return count

def cycle(grid, width, height, part2=False):
    to_flip = []
    for ((x, y), seat) in grid.items():
        adj = count_adj_full(grid, x, y, width, height, part2)
        if seat and adj >= (5 if part2 else 4):
            to_flip.append((x, y))
        elif (not seat) and (adj == 0):
            to_flip.append((x, y))

    if to_flip:
        for (x, y) in to_flip:
            grid[x,y] = not grid[x, y]
        return True
    return False


def part1(grid, width, height):
    while cycle(grid, width, height, part2=False):
        pass

    # count occupied seats
    count = sum([i for i in grid.values()])
    print(f'Part 1: {count}')


def part2(grid, width, height):
    while cycle(grid, width, height, part2=True):
        pass

    # count occupied seats
    count = sum([i for i in grid.values()])
    print(f'Part 2: {count}')


def main():
    with open('day11\input.txt') as fid:
        lines = fid.readlines()
    #lines = example

    # build grid
    grid = {}
    width = None
    height = None
    for (y, line) in enumerate(lines):
        for (x, seat) in enumerate(line.strip()):
            if seat == 'L':
                grid[x,y] = EMPTY
            else:
                # don't track floor
                pass
        if width is None:
            width = x+1
    height = y+1

    part1(deepcopy(grid), width, height)
    part2(deepcopy(grid), width, height)

if __name__ == '__main__':
    main()