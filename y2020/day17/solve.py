import numpy
import itertools
from collections import defaultdict
from AoC import AoC
import re

class GrowingGrid():
    """class to hold 3 dimensional array with automatic reallocation in +/- all dimensions"""
    def __init__(self, dtype=numpy.bool, ndims=3):
        if ndims not in [3, 4]:
            raise Exception('Only 3 or 4 dims!')
        self.ndims = ndims
        self._grid = numpy.zeros((3,3,1) if ndims==3 else (3,3,1,1), dtype=dtype)
        self.origin = numpy.zeros(ndims, dtype=numpy.uint16)
        self.min_active = [0] * ndims
        self.max_active = [0] * ndims

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

        for dim in range(1, self.ndims):
            if isinstance(coords, tuple) and len(coords) > dim:
                c = coords[dim]
                mod_coords[dim] = self.origin[dim] + c
                if self.origin[dim] + c not in range(self._grid.shape[dim]):
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
                    if self.ndims == 3:
                        yield (x - self.origin[0], y - self.origin[1], z - self.origin[2])
                    else:
                        # 4 dims
                        for j in range(-1, self._grid.shape[3] + 1):
                            yield (x - self.origin[0], y - self.origin[1], z - self.origin[2], j - self.origin[3])

    def iter_bounded(self):
        for x in range(self.min_active[0]-1, self.max_active[0] + 2):
            for y in range(self.min_active[1]-1, self.max_active[1] + 2):
                for z in range(self.min_active[2]-1, self.max_active[2] + 2):
                    if self.ndims == 3:
                        yield (x - self.origin[0], y - self.origin[1], z - self.origin[2])
                    else:
                        # 4 dims
                        for j in range(self.min_active[3]-1, self.max_active[3] + 2):
                            yield (x - self.origin[0], y - self.origin[1], z - self.origin[2], j - self.origin[3])



    def check_coords(self, coords, setitem=False):
        """runs check_coord on all appropriate coordinates"""
        mod_coords = list(coords)

        for dim in range(0, self.ndims):
            # check indices and resize if necessary
            if isinstance(coords, int):
                c = coords
            elif isinstance(coords, tuple) and len(coords) > dim:
                c = coords[dim]

            self.check_coord(c, dim)

            if isinstance(coords, int):
                # only happens for dim0
                mod_coords = self.origin[dim] + c
            else:
                mod_coords[dim] = self.origin[dim] + c

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

    def count_active_neighbors(self, x, y, z, j=None):
        if self.ndims == 3:
            neigh = [self[x+nx, y+ny, z+nz] for (nx, ny, nz) in itertools.product([-1, 1, 0], repeat=3) if ((nx, ny, nz) != (0, 0, 0))]
        else:
            # 4 dims
            neigh = [self[x+nx, y+ny, z+nz, j+nj] for (nx, ny, nz, nj) in itertools.product([-1, 1, 0], repeat=4) if ((nx, ny, nz, nj) != (0, 0, 0, 0))]

        return sum(neigh)

    def count_active(self):
        return numpy.count_nonzero(self._grid)

    def calc_bounds(self):
        #print('calc bounds')
        #self.disp()
        nz = numpy.nonzero(self._grid)
        for dim in range(self.ndims):
            self.min_active[dim] = nz[dim].min()
            self.max_active[dim] = nz[dim].max()
        #print(f'min: {self.min_active}')
        #print(f'max: {self.max_active}')

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
        self.grid3d = GrowingGrid()
        self.grid4d = GrowingGrid(ndims=4)
        for (y, line) in enumerate(lines):
            for (x, cell) in enumerate(line.strip()):
                self.grid3d[x,y,0] = cell == '#'
                self.grid4d[x,y,0,0] = cell == '#'

        self.grid3d.calc_bounds()
        self.grid4d.calc_bounds()

        self.grid = self.grid3d

    def cycle(self):
        """
        If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
        If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
        """
        to_flip = []
        for coords in self.grid.iter_bounded():
            if self.grid[coords]:
                if (self.grid.count_active_neighbors(*coords) in [2, 3]):
                    pass
                else:
                    to_flip.append(coords)
            else:
                if self.grid.count_active_neighbors(*coords) == 3:
                    to_flip.append(coords)

        for coord in to_flip:
            self.grid[coord] = not self.grid[coord]

        self.grid.calc_bounds()

    def part1(self):
        self.grid = self.grid3d
        for i in range(6):
            self.cycle()
        return self.grid.count_active()

    def part2(self):
        print('Warning: part 2 takes ~10min or so')
        self.grid = self.grid4d
        for i in range(6):
            print(f'cycle {i}...', end='')
            self.cycle()
            print('done')
        return self.grid.count_active()
