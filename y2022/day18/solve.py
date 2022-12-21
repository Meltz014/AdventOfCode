from AoC import AoC
import numpy as np
import sys
#sys.setrecursionlimit(10**6)


class Solver(AoC):
    example_data = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

    def parse(self):
        raw = self.read_input_txt(split=True)
        points = []
        for line in raw:
            points.append( [int(i) for i in line.split(',')] )
        points = np.array(points)
        maxes = np.max(points, axis=0)
        print(maxes)
        self.grid = np.zeros(maxes+1, dtype=bool)
        self.grid[points[:,0], points[:,1], points[:,2]] = 1
        print(points.shape)

    def part1(self):
        # start with total possible surface area
        sf = 6 * np.count_nonzero(self.grid)
        print(sf)

        # compare each slice, subtract 2 for each common square
        for i in range(self.grid.shape[0]-1):
            common = np.count_nonzero(np.logical_and(self.grid[i,:,:], self.grid[i+1,:,:]))
            sf -= common*2
        for i in range(self.grid.shape[1]-1):
            common = np.count_nonzero(np.logical_and(self.grid[:,i,:], self.grid[:,i+1,:]))
            sf -= common*2
        for i in range(self.grid.shape[2]-1):
            common = np.count_nonzero(np.logical_and(self.grid[:,:,i], self.grid[:,:,i+1]))
            sf -= common*2
        return sf

    def part2(self):
        tot = 0
        
        visited = set()
        sf = 0
        q = []

        def flood(point):
            nonlocal sf
            nonlocal q
            visited.add(point)
            neighbors = [
                (-1, 0, 0),
                (0, -1, 0),
                (0, 0, -1),
                (1, 0, 0),
                (0, 1, 0),
                (0, 0, 1),
            ]
            for (dx, dy, dz) in neighbors:
                new = (point[0]+dx, point[1]+dy, point[2]+dz)
                #print(new)
                if new[0] >= 0 and new[1] >= 0 and new[2] >= 0 and new[0] < self.grid.shape[0] and new[1] < self.grid.shape[1] and new[2] < self.grid.shape[2]:
                    if new not in visited and new not in q:
                        if self.grid[new]:
                            # droplet, count towards surface
                            sf += 1
                        else:
                            # no droplet; continue flood
                            q.append(new)

        # flood from all "air" spaces on edges
        for (y,z) in zip(*np.where(self.grid[0,:,:]==0)):
            q.append((0,y,z))
        for (y,z) in zip(*np.where(self.grid[-1,:,:]==0)):
            q.append((self.grid.shape[0]-1,y,z))
        for (x,z) in zip(*np.where(self.grid[:,0,:]==0)):
            q.append((x,0,z))
        for (x,z) in zip(*np.where(self.grid[:,-1,:]==0)):
            q.append((x,self.grid.shape[1]-1,z))
        for (x,y) in zip(*np.where(self.grid[:,:,0]==0)):
            q.append((x,y,0))
        for (x,y) in zip(*np.where(self.grid[:,:,-1]==0)):
            q.append((x,y,self.grid.shape[2]-1))

        q = list(set(q))

        while q:
            flood(q.pop(0))

        # need to cound all surfaces on edge of box
        sf += np.count_nonzero(self.grid[0,:,:])
        sf += np.count_nonzero(self.grid[-1,:,:])
        sf += np.count_nonzero(self.grid[:,0,:])
        sf += np.count_nonzero(self.grid[:,-1,:])
        sf += np.count_nonzero(self.grid[:,:,0])
        sf += np.count_nonzero(self.grid[:,:,-1])

        return sf