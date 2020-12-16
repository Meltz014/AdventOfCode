import numpy
from collections import defaultdict
from AoC import AoC
import re

class Solver(AoC):
    example_data = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""

    def parse(self):
        raw = self.read_input_txt(split=False)
        chunks = raw.split('\n\n')
        raw_rules = chunks[0]
        raw_my_ticket = chunks[1]
        raw_nearby = chunks[2]

        # parse rules
        self.rules = {}
        for line in raw_rules.splitlines():
            (field, ranges) = line.split(': ')
            f_ranges = []
            for _range in ranges.split(' or '):
                (s, e) = _range.split('-')
                f_ranges.append(numpy.arange(int(s), int(e)+1))
            self.rules[field] = numpy.concatenate(f_ranges)

        # parse my ticket
        self.my_ticket = raw_my_ticket.splitlines()[1].split(',')
        self.my_ticket = [int(i) for i in self.my_ticket]

        # parse nearby tickets
        self.nearby = []
        self.valid_tickets = []
        for line in raw_nearby.splitlines()[1:]:
            ticket = line.split(',')
            self.nearby.append([int(i) for i in ticket])

    def is_field_valid(self, val):
        all_ranges = self.rules.values()
        if not any(val in r for r in all_ranges):
            return False
        return True

    def part1(self):
        invalid_fields = []
        for ticket in self.nearby:
            valid = True
            for val in ticket:
                if not self.is_field_valid(val):
                    invalid_fields.append(val)
                    valid = False
                    break
            if valid:
                self.valid_tickets.append(ticket)
        return sum(invalid_fields)

    def part2(self):
        # include my ticket in valid list
        self.valid_tickets.insert(0, self.my_ticket)
        # convert to numpy array cause why not
        tickets = numpy.array(self.valid_tickets, dtype=numpy.uint16)

        # determine which field matches with with column
        columns = [None] * len(self.rules)
        while None in columns:
            for (field, ranges) in self.rules.items():
                if field not in columns:
                    valid_columns = numpy.invert(numpy.any(numpy.invert(numpy.isin(tickets, ranges)), axis=0))
                    valid_column_idx, = numpy.where(valid_columns)
                    valid_column_idx = [v for v in valid_column_idx if columns[v] is None]
                    if len(valid_column_idx) == 1:
                        columns[valid_column_idx[0]] = field
                    else:
                        # indeterminate; can't have more than one valid column before making a decision
                        pass

        # Return the product of all fields starting with "departure"
        field_prod = 1
        for (my_val, col) in zip(self.my_ticket, columns):
            if 'departure' in col:
                field_prod *= my_val
        return field_prod