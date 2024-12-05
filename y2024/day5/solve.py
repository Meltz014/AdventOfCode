from AoC import AoC
import re

class Solver(AoC):
    example_data = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


    def parse(self):
        raw = self.read_input_txt()
        self.rules = []
        self.tests = []
        parsing_rules = True
        self.debug(raw)
        for line in raw:
            if line == '\n':
                parsing_rules = False
                continue
            if parsing_rules:
                rulea, ruleb = line.strip().split('|')
                self.rules.append((int(rulea), int(ruleb)))
            else:
                self.tests.append([int(t) for t in line.strip().split(',')])

        for rule in sorted(self.rules):
            self.debug(rule)
        self.debug(self.tests)

    def part1(self):
        """
        """
        total = 0
        self.p2_total = 0

        def get_rule_order(test):
            rule_order = []
            # first order the rules
            for l, r in sorted(self.rules):
                if l not in test or r not in test:
                    continue
                self.debug(f'rule: {l,r}')
                if r not in rule_order:
                    rule_order.append(r)
                r_loc = rule_order.index(r)
                if l not in rule_order:
                    # insert right before r
                    rule_order.insert(r_loc, l)
                else:
                    # make sure l <- r
                    l_loc = rule_order.index(l)
                    if l_loc > r_loc:
                        rule_order.pop(l_loc)
                        rule_order.insert(r_loc, l)
            return rule_order


        # sort each test and see if it changed
        # capture middle number of each correctly ordered test
        for test in self.tests:
            rule_order = get_rule_order(test)
            self.debug(f'test:       {test}')
            self.debug(f'rule_order: {rule_order}')
            if rule_order == test:
                # correctly ordered
                total += test[len(test)//2]
            else:
                # incorrectly ordered
                self.p2_total += rule_order[len(rule_order)//2]

        return total

    def part2(self):
        """
        Actually computed as part of part1
        """
        return self.p2_total
