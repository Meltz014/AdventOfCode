from copy import deepcopy
from AoC import AoC
import re

class Solver(AoC):
    example_data = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""

    def parse(self):
        lines = self.read_input_txt()

        self.rules = {}
        self.messages = []
        rules_done = False
        for line in lines:
            line = line.strip()
            if not line:
                rules_done = True
                continue
            if not rules_done:
                (rule_num, rule) = line.split(': ')
                # remove quotes (not needed in regex)
                # replace pipe (valid regex, not wanted here yet) with dummy symbol &
                self.rules[rule_num] = rule.replace('"', '').replace('|', '&')
            else:
                self.messages.append(line)
        self.p2_rules = deepcopy(self.rules)

    # Need to resolve each rule into a regex
    def resolve_rule(self, rule, rootid=None):
        if '&' in rule:
            sub_rules = rule.split('&')
            sub_resolved = [self.resolve_rule(s.strip()) for s in sub_rules]
            resolved = '(' + '|'.join(sub_resolved) + ')'
        else:
            sub_rules = rule.split(' ')
            sub_resolved = []
            for sub_rule in sub_rules:
                if sub_rule.isnumeric():
                    r = self.resolve_rule(self.rules[sub_rule], rootid=sub_rule)
                else:
                    # should already be resolved
                    r = sub_rule.strip()
                sub_resolved.append(r)
            resolved = ''.join(sub_resolved)
        if rootid is not None:
            self.rules[rootid] = resolved
        return resolved


    def part1(self):
        self.resolve_rule(self.rules['0'], rootid='0')
        pattern = re.compile(f'^{self.rules["0"]}$')
        matches = [re.match(pattern, m) for m in self.messages]
        tot = len(matches) - matches.count(None)
        return tot

    def part2(self):
        self.rules = self.p2_rules
        # add recursive rules to 8 and 11
        self.rules['8'] = '42 +'
        # just hardcode a fixed number of recursions.  The strings are small enough that this should work
        self.rules['11'] = '( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 | ( 42 ( 42 31 ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) ) 31 ) )'
        self.rules['11'].replace('|', '&')
        self.resolve_rule(self.rules['0'], rootid='0')
        print(self.rules['0'])
        pattern = re.compile(f'^{self.rules["0"]}$')
        matches = [re.match(pattern, m) for m in self.messages]
        tot = len(matches) - matches.count(None)
        return tot

