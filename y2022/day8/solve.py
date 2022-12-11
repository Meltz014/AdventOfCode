from AoC import AoC
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

class Solver(AoC):
    example_data = """30373
25512
65332
33549
35390"""

    def parse(self):
        raw = self.read_input_txt(split=True)
        trees = []
        for line in raw:
            line = line.strip()
            trees.append([int(i) for i in line])
        self.trees = np.array(trees)
        #print(self.trees)
        #plt.imshow(self.trees)
        #plt.show()


    def part1(self):
        """
        find "visible" trees
        """
        visible = set()
        # from top
        maxes = np.ones(self.trees.shape[1], dtype=np.int64)*-1
        for (i, row) in enumerate(self.trees):
            #display(maxes)
            for j in np.where(row>maxes)[0]:
                visible.add((i,j))
            maxes[row>maxes] = row[row>maxes]
        # from bottom
        maxes = np.ones(self.trees.shape[1], dtype=np.int64)*-1
        for (i, row) in enumerate(self.trees[::-1,:]):
            #display(maxes)
            for j in np.where(row>maxes)[0]:
                visible.add((self.trees.shape[0]-(i+1),j))
            maxes[row>maxes] = row[row>maxes]
        # from left
        ttrees = self.trees.transpose()
        maxes = np.ones(ttrees.shape[0], dtype=np.int64)*-1
        for (j, row) in enumerate(ttrees):
            for i in np.where(row>maxes)[0]:
                visible.add((i,j))
            maxes[row>maxes] = row[row>maxes]
        # from right
        ttrees = self.trees.transpose()
        maxes = np.ones(ttrees.shape[0], dtype=np.int64)*-1
        for (j, row) in enumerate(ttrees[::-1,:]):
            for i in np.where(row>maxes)[0]:
                visible.add((i,ttrees.shape[0]-(j+1)))
            maxes[row>maxes] = row[row>maxes]

        #print(sorted(list(visible)))
        return len(visible)


    def part2(self):
        """
        Highest scenic score - num visible trees in each direction multiplied together
        """
        tot = 0
        scores = np.zeros_like(self.trees)
        for i in range(self.trees.shape[0]):
            for j in range(self.trees.shape[1]):
                visible = 0
                score = 1
                tree = self.trees[i,j]
                ## up
                for ii in range(1,i+1):
                    visible += 1
                    if tree <= self.trees[i-ii,j]:
                        break
                score *= visible
                visible = 0
                ## down
                for ii in range(1,self.trees.shape[0]-i):
                    visible += 1
                    if tree <= self.trees[i+ii,j]:
                        break
                score *= visible
                visible = 0
                ## left
                for jj in range(1,j+1):
                    visible += 1
                    if tree <= self.trees[i,j-jj]:
                        break
                score *= visible
                visible = 0
                ## right
                for jj in range(1,self.trees.shape[1]-j):
                    visible += 1
                    if tree <= self.trees[i,j+jj]:
                        break
                score *= visible
                visible = 0
                scores[i,j] = score
        plt.imshow(scores, norm=LogNorm(vmin=0.0001, vmax=np.max(scores)))
        plt.show()

        return np.max(scores)