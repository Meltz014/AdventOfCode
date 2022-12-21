from AoC import AoC
import re

class Solver(AoC):
    example_data = """1
2
-3
3
-2
0
4"""

    def parse(self):
        raw = self.read_input_numeric()
        #self.seq = list(raw)
        #print(len(set(self.seq)) == len(self.seq))
        print(raw)
        self.seq = [(n, i) for i,n in enumerate(raw)]
        print(self.seq)
        self.zero = None
        for item in self.seq:
            if item[0] == 0:
                self.zero = item
                break

    def mix(self):
        l = len(self.seq)
        for item in sorted(self.seq, key=lambda x: x[1]):
            if item[0] % (l-1) == 0:
                continue
            old = self.seq.index(item)
            new = old + item[0]
            #if new <= 0:
            #    new -= 1
            #if new >= l:
            #    new += 1
            new %= (l-1)
            self.seq.pop(old)
            self.seq.insert(new, item)
            #input()

    def part1(self):
        tot = 0
        l = len(self.seq)
        self.mix()
        zi = self.seq.index(self.zero)
        print(zi)
        zi += 1000
        zi %= l
        print(zi, self.seq[zi][0])
        tot += self.seq[zi][0]
        zi += 1000
        zi %= l
        print(zi, self.seq[zi][0])
        tot += self.seq[zi][0]
        zi += 1000
        zi %= l
        print(zi, self.seq[zi][0])
        tot += self.seq[zi][0]
        return tot

    def part2(self):
        tot = 0
        key = 811589153
        l = len(self.seq)
        # put in original order
        self.seq.sort(key=lambda x: x[1])
        # apply key
        for (i, (n, ii)) in enumerate(self.seq):
            self.seq[i] = (n * key, ii)
        
        # mix 10 times
        for i in range(10):
            self.mix()

        zi = self.seq.index(self.zero)
        print(zi)
        zi += 1000
        zi %= l
        print(zi, self.seq[zi][0])
        tot += self.seq[zi][0]
        zi += 1000
        zi %= l
        print(zi, self.seq[zi][0])
        tot += self.seq[zi][0]
        zi += 1000
        zi %= l
        print(zi, self.seq[zi][0])
        tot += self.seq[zi][0]
        return tot