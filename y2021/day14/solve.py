from collections import Counter
from AoC import AoC

class Polymer:
    def __init__(self, p_str):
        pairs = [f'{p_str[i]}{p_str[i+1]}' for i in range(len(p_str)-1)]
        self.char_counter = Counter(p_str)
        self.pairs_counter = Counter(pairs)
        self.pending_pairs = Counter()
        self.pending_chars = Counter()

    def pre_apply_rule(self, pair, val):
        if pair in self.pairs_counter and self.pairs_counter[pair] > 0:
            # new pairs generated
            np_a = pair[0] + val
            np_b = val + pair[1]
            # add the new pairs for each instance of original pair
            self.pending_pairs[np_a] += self.pairs_counter[pair]
            self.pending_pairs[np_b] += self.pairs_counter[pair]
            # add the new char for each instance of original pair
            self.pending_chars[val] += self.pairs_counter[pair]
            # remove original pair
            self.pending_pairs[pair] -= self.pairs_counter[pair]

    def apply(self):
        self.char_counter.update(self.pending_chars)
        self.pairs_counter.update(self.pending_pairs)
        self.pending_chars.clear()
        self.pending_pairs.clear()

    def get_char_counts(self):
        return self.char_counter.most_common()

    def __len__(self):
        return sum(self.char_counter.values())

class Solver(AoC):
    example_data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

    def parse(self):
        raw = self.read_input_txt()
        self.polymer = Polymer(raw[0].strip('\n'))
        self.instructions = {}
        for line in raw[2:]:
            (k, v) = line.strip('\n').split(' -> ')
            self.instructions[k] = v

    def polymerize(self, n):
        for i in range(n):
            for (pair, val) in self.instructions.items():
                self.polymer.pre_apply_rule(pair, val)
            self.polymer.apply()

    def part1(self):
        self.polymerize(10)
        ordered = self.polymer.get_char_counts()
        return ordered[0][1] - ordered[-1][1]


    def part2(self):
        self.polymerize(30)
        ordered = self.polymer.get_char_counts()
        return ordered[0][1] - ordered[-1][1]
