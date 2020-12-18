import numpy
import itertools
from collections import defaultdict
from AoC import AoC
import re

class GrowingGrid():
    """class to hold 3 dimensional array with automatic reallocation in +/- all dimensions"""
    def __init__(self, dtype=numpy.bool):
        self._grid = numpy.zeros((3,3,1), dtype=dtype)
        self.origin = numpy.zeros(3, dtype=numpy.uint16)
        self.min_set = [0, 0, 0]
        self.max_set = [3, 3, 0]

    def __getitem__(self, coords):
        if isinstance(coords, slice) or any(isinstance(k, slice) for k in coords):
            return self._grid[coords]

        if isinstance(coords, int):
            x = coords
        else:
            x = coords[0]
        if self.origin[0] + x not in range(self._grid.shape[0]):
            return False

        if isinstance(coords, int):
            mod_coords = self.origin[0] + x
        else:
            mod_coords = list(coords)
            mod_coords[0] = self.origin[0] + x

        if isinstance(coords, tuple) and len(coords) > 1:
            y = coords[1]
            mod_coords[1] = self.origin[1] + y
            if self.origin[1] + y not in range(self._grid.shape[1]):
                return False

        if isinstance(coords, tuple) and len(coords) > 2:
            z = coords[2]
            mod_coords[2] = self.origin[2] + z
            if self.origin[2] + z not in range(self._grid.shape[2]):
                return False

        if isinstance(mod_coords, list):
            mod_coords = tuple(mod_coords)
        return self._grid[mod_coords]

    def __setitem__(self, key, newval):
        if isinstance(key, slice) or any(isinstance(k, slice) for k in key):
            self._grid[key] = newval
        else:
            mod_key = self.check_coords(key, setitem=True)
            self._grid[mod_key] = newval

    def iter_all(self):
        for x in range(-1, self._grid.shape[0] + 1):
            for y in range(-1, self._grid.shape[1] + 1):
                for z in range(-1, self._grid.shape[2] + 1):
                    yield (x - self.origin[0], y - self.origin[1], z - self.origin[2])

    def iter_bounded(self):
        for x in range(self.min_set[0]-1, self.max_set[0] + 2):
            for y in range(self.min_set[1]-1, self.max_set[1] + 2):
                for z in range(self.min_set[2]-1, self.max_set[2] + 2):
                    yield (x - self.origin[0], y - self.origin[1], z - self.origin[2])


    def check_coords(self, coords, setitem=False):
        """runs check_coord on all appropriate coordinates"""
        mod_coords = coords

        # check indices and resize if necessary
        if isinstance(coords, int):
            x = coords
        else:
            x = coords[0]
        self.check_coord(x, 0)
        if setitem:
            self.min_set[0] = min(self.min_set[0], x)
            self.max_set[0] = max(self.max_set[0], x)

        if isinstance(coords, int):
            mod_coords = self.origin[0] + x
        else:
            mod_coords = list(coords)
            mod_coords[0] = self.origin[0] + x

        if isinstance(coords, tuple) and len(coords) > 1:
            y = coords[1]
            self.check_coord(y, 1)
            mod_coords[1] = self.origin[1] + y
            if setitem:
                self.min_set[1] = min(self.min_set[1], y)
                self.max_set[1] = max(self.max_set[1], y)


        if isinstance(coords, tuple) and len(coords) > 2:
            z = coords[2]
            self.check_coord(z, 2)
            mod_coords[2] = self.origin[2] + z
            if setitem:
                self.min_set[2] = min(self.min_set[2], z)
                self.max_set[2] = max(self.max_set[2], z)


        #print(f'mod_coords: {mod_coords}')
        #print(f'origin: {self.origin}')
        if isinstance(mod_coords, list):
            mod_coords = tuple(mod_coords)
        return mod_coords

    def check_coord(self, coord, dim):
        """bound checks a single coordinate and grows the array accordingly"""
        while True:
            if coord + self.origin[dim] >= self._grid.shape[dim]:
                self.grow(dim, 1)
                continue
            elif coord + self.origin[dim] < 0:
                self.grow(dim, -1)
                continue
            break

    def grow(self, dim, direction=1):
        #print(f'grow dim {dim} {"positive" if direction == 1 else "negative"}')
        new = numpy.zeros_like(self._grid)
        if direction == 1:
            # positive
            self._grid = numpy.concatenate((self._grid, new), axis=dim)
        else:
            # negative
            self._grid = numpy.concatenate((new, self._grid), axis=dim)
            # offset origin
            self.origin[dim] += new.shape[dim]
        #print(f'new shape: {self._grid.shape}, origin: {self.origin}')

    def count_active_neighbors(self, x, y, z):
        neigh = [self[x+nx, y+ny, z+nz] for (nx, ny, nz) in itertools.product([-1, 1, 0], repeat=3) if ((nx, ny, nz) != (0, 0, 0))]
        #print(f'neigh({x, y, z}): {sum(neigh)}')
        return sum(neigh)

    def count_active(self):
        return numpy.count_nonzero(self._grid)

    def disp(self):
        for z in range(self._grid.shape[2]):
            print(f'Z = {z-self.origin[2]}')
            layer = self._grid[:,:,z]
            for y in range(layer.shape[1]):
                print(''.join(['#' if x else '.' for x in layer[:,y]]))


class Solver(AoC):
    example_data = """.#.
..#
###"""

    def parse(self):
        lines = self.read_input_txt()
        self.grid = GrowingGrid()
        for (y, line) in enumerate(lines):
            for (x, cell) in enumerate(line.strip()):
                self.grid[x,y,0] = cell == '#'

        print(self.grid._grid)

    def cycle(self):
        to_flip = []
        for (x, y, z) in self.grid.iter_all():
            if self.grid[x, y, z]:
                if (self.grid.count_active_neighbors(x, y, z) in [2, 3]):
                    pass
                else:
                    to_flip.append((x, y, z))
            else:
                if self.grid.count_active_neighbors(x, y, z) == 3:
                    to_flip.append((x, y, z))

        print(f'to_flip: {to_flip}')

        for coord in to_flip:
            self.grid[coord] = not self.grid[coord]

    def part1(self):
        """
        If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
        If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
        """
        #print(self.grid.count_active_neighbors(0, 0, 0))
        #print(self.grid.count_active_neighbors(0, 1, 0))
        #print(self.grid.count_active_neighbors(0, 2, 0))
        #print(self.grid.count_active_neighbors(1, 0, 0))
        self.grid.disp()
        for i in range(6):
            self.cycle()
            #self.grid.disp()
            #input()
        return self.grid.count_active()

    def part2(self):
        pass