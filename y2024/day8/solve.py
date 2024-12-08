from AoC import AoC

class Solver(AoC):
    example_data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

    def parse(self):
        self.tests = []
        self.data = []
        raw = self.read_input_txt()
        for line in raw:
            t, d = line.strip().split(':')
            self.tests.append(int(t))
            self.data.append([int(n) for n in d.split()])

        self.debug(self.tests)
        self.debug(self.data)

    def part1(self):
        """
        """
        total = 0

        def is_valid(test, first, rest):
            _prod = first * rest[0]
            _sum = first + rest[0]
            if len(rest) == 1:
                if _prod == test or _sum == test:
                    return True
                else:
                    return False
            else:
                ret = False
                #if _prod < test:
                #    ret = is_valid(test, _prod, rest[1:])
                #if not ret and _sum < test:
                #    ret = is_valid(test, _sum, rest[1:])
                return is_valid(test, _prod, rest[1:]) or is_valid(test, _sum, rest[1:])

        for test, data in zip(self.tests, self.data):
            if is_valid(test, data[0], data[1:]):
                self.debug(test, 'is valid')
                total += test

        return total

    def part2(self):
        """
        """
        total = 0

        def is_valid(test, first, rest):
            _prod = first * rest[0]
            _sum = first + rest[0]
            _concat = int(str(first) + str(rest[0]))
            if len(rest) == 1:
                if _prod == test or _sum == test or _concat == test:
                    return True
                else:
                    return False
            else:
                ret = False
                #if _prod < test:
                #    ret = is_valid(test, _prod, rest[1:])
                #if not ret and _sum < test:
                #    ret = is_valid(test, _sum, rest[1:])
                return is_valid(test, _prod, rest[1:]) or is_valid(test, _sum, rest[1:]) or is_valid(test, _concat, rest[1:])

        for test, data in zip(self.tests, self.data):
            if is_valid(test, data[0], data[1:]):
                self.debug(test, 'is valid')
                total += test

        return total
