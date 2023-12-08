from AoC import AoC
import re

class Solver(AoC):
    example_data = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

    def parse(self):
        self.raw = self.read_input_txt(split=True)
        self.cards = []
        for line in self.raw:
            line = line.split(': ')[1]
            winning, have = line.split('|')
            winning = [int(a) for a in re.split(r'\s+', winning.strip())]
            have = [int(a) for a in re.split(r'\s+', have.strip())]
            self.cards.append([winning, have, 1])

        print(self.cards)

    def part1(self):
        total = 0
        for (i, (winning, have, _)) in enumerate(self.cards):
            score = 2 ** (len(set(winning) & set(have))-1)
            if score >= 1:
                total += score
            print(f'Card {i}: {set(winning) & set(have)}: score {score}')
        return total

    def part2(self):
        for (i, (winning, have, copies)) in enumerate(self.cards):
            matches = len(set(winning) & set(have))
            print(f'Card {i}: {set(winning) & set(have)}: matches {matches}')
            if matches:
                for _ in range(copies):
                    # add copies of next 5 cards
                    for ii in range(i+1, i+matches+1):
                        if ii < len(self.cards):
                            self.cards[ii][2] += 1

        total = sum([card[2] for card in self.cards])
        return total

