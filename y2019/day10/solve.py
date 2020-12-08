import numpy
import itertools
from math import atan2
from collections import defaultdict
from fractions import Fraction

debug = False

def test_points(blocked, current, test, max_x, max_y):
    if debug:
        print(f'testing {current} against {test}')
    (cur_x, cur_y) = current
    (test_x, test_y) = test
    visible = False
    if not blocked[test_y, test_x]:
        # mark as visible
        visible = True
        # get slope of line
        _dx = test_x - cur_x
        _dy = test_y - cur_y
        if _dx:
            m = Fraction(abs(_dy), abs(_dx))
            dy = m.numerator * (1 if _dy >= 0 else -1)
            dx = m.denominator * (1 if _dx >= 0 else -1)
        else:
            dx = _dx
            dy = 1 if (test_y > cur_y) else -1
        if dy:
            range_y = range(test_y+dy, (max_y+1) if dy > 0 else -1, dy)
        else:
            # dy = 0, don't change
            range_y = [cur_y] * max_y
        if dx:
            range_x = range(test_x+dx, (max_x+1) if dx > 0 else -1, dx)
        else:
            range_x = [cur_x] * max_x
        for (xx, yy) in zip(range_x, range_y):
            # mark as blocked
            blocked[yy, xx] = True

    return visible

def main():
    # part 1
    test = ( "......#.#.\n"
             "#..#.#....\n"
             "..#######.\n"
             ".#.#.###..\n"
             ".#..#.....\n"
             "..#....#.#\n"
             "#..#....#.\n"
             ".##.#..###\n"
             "##...#..#.\n" # 3rd one here
             ".#....####" )

    test_a = ( "..........\n"
               "..........\n"
               ".....#....\n"
               "..........\n"
               "....#.#...\n"
               "....#.....\n"
               "..........\n"
               "..#.......\n"
               "..........\n"
               ".........." )

    asteroids = []
    max_x = 0
    max_y = 0

    if False:
        rows = test_a.split('\n')
    else:
        with open(f'day10\input.txt') as fid:
            rows = fid.readlines()

    for (y,row) in enumerate(rows):
        if y > max_y:
            max_y = y
        for (x,c) in enumerate(row):
            if x > max_x:
                max_x = x
            if c == '#':
                asteroids.append((x,y))

    asteroid_visible_counts = []
    visible_db = defaultdict(list)
    for (current_i, current) in enumerate(asteroids):
        # create matrix of bools signifying if a space is blocked
        blocked = numpy.zeros((max_y+1, max_x+1), dtype=numpy.bool)
        visible_count = 0
        # scan asteroids after current
        for test in asteroids[current_i+1:]:
            if test_points(blocked, current, test, max_x, max_y):
                visible_db[current].append(test)
                visible_count += 1
        # scan asteroids before current
        if current_i > 0:
            for test in asteroids[(current_i-1)::-1]:
                if test_points(blocked, current, test, max_x, max_y):
                    visible_db[current].append(test)
                    visible_count += 1
        asteroid_visible_counts.append(visible_count)
        if debug:
            print(blocked)

    most = max(asteroid_visible_counts)
    most_i = asteroid_visible_counts.index(most)
    point = asteroids[most_i]
    print(f'Part 1: {most}, {point}')

    pivot_list = visible_db[point]
    by_angle = sorted(pivot_list, key=lambda p: atan2(p[0] - point[0], p[1] - point[1]), reverse=True)
    
    print(f'Part 2: {by_angle[199]}')

if __name__ == '__main__':
    main()
