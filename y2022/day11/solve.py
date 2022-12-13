from AoC import AoC
import re
from operator import add, mul

ops = {
    '+': add,
    '*': mul
}
lcm = 0
class Monkey():
    def __init__(self, items, op, val, test):
        self.items = items
        self.op = op
        self.val = val
        self.test = test
        self.if_true = None  # set to other monkey obj
        self.if_false = None
        self.inspected = 0

    def do_test(self, item):
        return (item % self.test) == 0

    def throw_to(self, item, other):
        other.items.append(item)

    def inspect(self, p2=False):
        while self.items:
            self.inspected += 1
            item = self.items.pop(0)
            if self.val == 'old':
                item = item ** 2
            else:
                item = ops[self.op](item, self.val)
            if not p2:
                item //= 3
            item %= lcm
            self.throw_to(item, self.if_true if self.do_test(item) else self.if_false)


class Solver(AoC):
    example_data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

    def parse(self):
        raw = self.read_input_txt(split=True)
        self.monkeys = []
        test_idx = []
        all_tests = []
        global lcm
        while raw:
            line = raw.pop(0).strip()
            if re.match(r'Monkey \d', line):
                items = [int(i) for i in re.findall(r'\d+', raw.pop(0))]
                mobj = re.search(r'old ([+*]) (.*?)\n', raw.pop(0))
                op = mobj.group(1)
                val = mobj.group(2)
                if val.isnumeric():
                    val = int(val)
                test = int(re.search(r'divisible by (\d+)', raw.pop(0)).group(1))
                all_tests.append(test)
                if_true = int(re.search(r'throw to monkey (\d+)', raw.pop(0)).group(1))
                if_false = int(re.search(r'throw to monkey (\d+)', raw.pop(0)).group(1))
                test_idx.append((if_true, if_false))
                self.monkeys.append(Monkey(items, op, val, test))

        # need to populate test true/false refs
        for (i, (if_true, if_false)) in enumerate(test_idx):
            self.monkeys[i].if_true = self.monkeys[if_true]
            self.monkeys[i].if_false = self.monkeys[if_false]

        # get lcm for optimizaion
        lcm = 1
        for t in all_tests:
            lcm = lcm * t

    def part1(self):
        tot = 0
        for i in range(20):
            for monkey in self.monkeys:
                monkey.inspect()
        sorted_monkeys = sorted(self.monkeys, key=lambda m: m.inspected, reverse=True)
        return sorted_monkeys[0].inspected * sorted_monkeys[1].inspected

    def part2(self):
        tot = 0
        # reparse
        self.parse()
        for i in range(10000):
            for monkey in self.monkeys:
                monkey.inspect(p2=True)
        sorted_monkeys = sorted(self.monkeys, key=lambda m: m.inspected, reverse=True)
        return sorted_monkeys[0].inspected * sorted_monkeys[1].inspected
