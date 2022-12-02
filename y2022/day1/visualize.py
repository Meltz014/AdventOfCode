from y2022.day1.solve import Solver as Base
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Solver(Base):

    def visualize(self):
        self.parse()
        #lens = np.array([len(e) for e in self.elves])
        #mask = np.arange(lens.max()) < lens[:,None]
        #out = np.zeros(mask.shape)
        #out[mask] = np.concatenate(self.elves)
        #print(out)
        df = pd.DataFrame(self.elves)
        array = df.fillna(0).values
        print(array)
        print(df)
        #df.plot.bar(stacked=True)
        print()
        s = df.T.sum().sort_values(ascending=False)
        print(s)
        print(s.index)
        print(s.values)
        sorted_df = df.loc[s.index]
        sorted_df.index = s.values

        fig, axes = plt.subplots(nrows=2, ncols=1)


        sorted_df.plot.bar(stacked=True, ax=axes[0], title='All Elves', legend=False)
        sorted_df.head(n=10).plot.bar(stacked=True, ax=axes[1], title='Top 10 Elves', legend=False)
        plt.show()
