from AoC import AoC
import numpy as np

"""
  x       x               x       x 
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

          x       x       x       x  
  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
 """



class Solver(AoC):
    example_data = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

    def parse(self):
        raw = self.read_input_txt()
        self.samples = []
        self.outputs = []
        for line in raw:
            s, o = line.strip('\n').split(' | ')
            self.samples.append([set(samp) for samp in s.split()])
            self.outputs.append([set(samp) for samp in o.split()])

    def part1(self):
        count = 0
        for out in self.outputs:
            for o in out:
                if len(o) in [2,4,3,7]:
                    count += 1
        return count

    def part2(self):
        # need to deduce which segment set goes to which digit
        full_sum = 0
        for (sample, output) in zip(self.samples, self.outputs):
            digits_per_set = {}
            set_per_digit = {}
            # find 1,4,7,8
            for s in sample:
                if len(s) == 2:
                    digits_per_set[''.join(sorted(s))] = 1
                    set_per_digit[1] = s
                elif len(s) == 4:
                    digits_per_set[''.join(sorted(s))] = 4
                    set_per_digit[4] = s
                elif len(s) == 3:
                    digits_per_set[''.join(sorted(s))] = 7
                    set_per_digit[7] = s
                elif len(s) == 7:
                    digits_per_set[''.join(sorted(s))] = 8
                    set_per_digit[8] = s

            # find 3.
            for s in sample:
                if len(s^set_per_digit[7]) == 2:
                    digits_per_set[''.join(sorted(s))] = 3
                    set_per_digit[3] = s
                    break
            # find 9
            for s in sample:
                if len(s^set_per_digit[3]) == 1:
                    digits_per_set[''.join(sorted(s))] = 9
                    set_per_digit[9] = s
                    break
            # find 0
            for s in sample:
                if len(s^set_per_digit[7]) == 3 and s not in [set_per_digit[9], set_per_digit[4]]:
                    digits_per_set[''.join(sorted(s))] = 0
                    set_per_digit[0] = s
                    break
            # find 6
            for s in sample:
                if len(s) == 6 and s not in [set_per_digit[9], set_per_digit[0]]:
                    digits_per_set[''.join(sorted(s))] = 6
                    set_per_digit[6] = s
                    break
            # find 5 and 2
            for s in sample:
                if len(set_per_digit[9]-s) == 2 and s not in set_per_digit.values():
                    digits_per_set[''.join(sorted(s))] = 2
                    set_per_digit[2] = s
            for s in sample:
                if len(set_per_digit[9]-s) == 1 and s not in set_per_digit.values():
                    digits_per_set[''.join(sorted(s))] = 5
                    set_per_digit[5] = s
            out = int(''.join([str(digits_per_set[''.join(sorted(s))]) for s in output]))
            full_sum += out

        return full_sum