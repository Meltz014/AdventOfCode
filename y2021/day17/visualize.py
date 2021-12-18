from .solve import Solver as Base
import itertools
import matplotlib.pyplot as plt
import numpy as np

def velocities(vi, a, t):
    return np.arange(vi, vi+(t*a), a)

class Solver(Base):

    def visualize(self):
        self.parse()

        max_y = -1 * min(self.target[1])
        min_y = min(self.target[1])
        max_x = max(self.target[0])+1
        min_x = int((min(self.target[0])*2)**0.5)
        is_valid = 0
        t = 50
        all_pts = list(itertools.product(range(min_x, max_x), range(min_y, max_y)))
        valid_pts = np.zeros((len(all_pts),2), np.int16)
        invalid_pts = np.zeros((len(all_pts),2), np.int16)
        v_i = 0
        i_i = 0
        for (x,y) in all_pts:
            if self.is_valid_vi(x,y):
                valid_pts[v_i,:] = [x,y]
                v_i += 1
            else:
                invalid_pts[i_i,:] = [x,y]
                i_i += 1
        print(len(all_pts))
        print(v_i)
        print(i_i)
        plt.scatter(valid_pts[:v_i,0], valid_pts[:v_i,1], c='g', marker='.')
        plt.scatter(invalid_pts[:i_i,0], invalid_pts[:i_i,1], c='r', marker='.')
        plt.show()

