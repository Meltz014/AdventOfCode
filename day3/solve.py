import numpy
plot = 0
GRIDSIZE = 20000

def build_grid(line):
    grid = numpy.zeros((GRIDSIZE, GRIDSIZE), dtype=numpy.bool8)
    x = GRIDSIZE // 2
    y = GRIDSIZE // 2
    origin = (y,x)
    grid[origin] = True
    for segment in line.split(','):
        #print(f'x {x}, y {y}')
        direction = segment[0]
        dist = int(segment[1:])
        if direction == 'R':
            #print(f'right {dist}')
            x += 1
            grid[y, x:x+dist] = True
            x += (dist-1)
        elif direction == 'L':
            #print(f'left {dist}')
            grid[y, x-dist:x] = True
            x -= dist
        elif direction == 'U':
            #print(f'up {dist}')
            y += 1
            grid[y:y+dist, x] = True
            y += (dist-1)
        elif direction == 'D':
            #print(f'down {dist}')
            grid[y-dist:y, x] = True
            y -= dist

    return grid

def point_on_line(y0, y1, x0, x1, point):
    # point is (y,x)
    dist = -1
    if point[0] in range(y0, y1+1):
        dist = abs(point[0] - y0)
        if point[1] in range(x0, x1+1):
            dist += abs(point[1] - x0)
        else:
            dist = -1

    return dist

def find_intersection(line, cross_coords):
    x = GRIDSIZE // 2
    y = GRIDSIZE // 2
    steps = 0
    origin = (y,x)
    for segment in line.split(','):
        direction = segment[0]
        dist = int(segment[1:])
        start_x = x
        end_x = x
        start_y = y
        end_y = y
        if direction == 'R':
            #print(f'right {dist}')
            end_x = x + dist
            x += dist
        elif direction == 'L':
            #print(f'left {dist}')
            start_x = x - dist
            x -= dist
        elif direction == 'U':
            #print(f'up {dist}')
            end_y = y + dist
            y += dist
        elif direction == 'D':
            #print(f'down {dist}')
            start_y = y - dist
            y -= dist

        # check if any crossing points are on the line segment
        for point in cross_coords:
            _steps = point_on_line(start_y, end_y, start_x, end_x, point)
            if _steps >= 0:
                if direction in 'DL':
                    _steps = dist - _steps
                _steps += steps
                yield _steps, point

        steps += dist


def main():
    grids = []
    with open('day3\input.txt') as fid:
        line_a = fid.readline()
        line_b = fid.readline()

    #line_a = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
    #line_b = 'U62,R66,U55,R34,D71,R55,D58,R83'
    #line_a = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'
    #line_b = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
    #line_a = 'R100,D110'
    #line_b = 'D100,R110'

    grid_a = build_grid(line_a)
    grid_b = build_grid(line_b)

    origin = GRIDSIZE // 2

    # assume only 2 wires
    # get x and y values of intersection between 2 grids
    (cross_y, cross_x) = numpy.where(grid_a & grid_b)
    # compute manhattan distance
    cross_coords = [(y,x) for (y,x) in zip(cross_y, cross_x) if (y,x) != (origin,origin)]
    dists = [abs(x-origin) + abs(y-origin) for (y,x) in cross_coords]
    print(f'Part 1: Min dist: {numpy.min(dists)}')

    if plot:
        import matplotlib.pyplot as plt
        plt.imshow(grid_a, cmap='gray')
        plt.imshow(grid_b, cmap='jet', alpha=0.5)
        plt.show()

    # part 2: find min number of "steps" or wire length to get to the first intersection
    line_a_steps = [(dist, point) for (dist, point) in find_intersection(line_a, cross_coords)]
    line_a_steps = sorted(line_a_steps, key=lambda x: x[1])
    line_b_steps = [(dist, point) for (dist, point) in find_intersection(line_b, cross_coords)]
    line_b_steps = sorted(line_b_steps, key=lambda x: x[1])
    assert(len(line_a_steps) == len(line_b_steps))
    min_steps = min(a[0]+b[0] for (a,b) in zip(line_a_steps, line_b_steps))
    print(f'Part 2: min steps: {min_steps}')

if __name__ == '__main__':
    main()