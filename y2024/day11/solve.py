from AoC import AoC
from tqdm import tqdm
from functools import cache

"""
None of this Linked List nonsense is required, but it's kept here for historical context
"""

class Node():
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

    def insert(self, next):
        next.next = self.next
        self.next = next
        next.prev = self

class LL():
    def __init__(self, head):
        self.head = head
        self.length = 0
        self.tail = head

        for node in self:
            self.length += 1
            self.tail = node

    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next

    def append(self, value):
        next = Node(value)
        self.tail.insert(next)
        self.tail = next
        self.length += 1

    def push(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node
        self.head.prev = None
        self.length += 1
        return

    def print(self):
        for n in self:
            print(f'{n.value} -> ', end='')
        print()

@cache
def blink_stone(stone):
    if stone == 0:
        return [1]
    stone_str = str(stone)
    l = len(stone_str)
    if l % 2 == 0:
        half_l = l//2
        return [int(stone_str[:half_l]), int(stone_str[half_l:])] 
    return [stone * 2024]


class Solver(AoC):
    example_data_0 = """0 1 10 99 999"""
    example_data = """125 17"""


    def parse(self):
        self.raw = [int(i) for i in self.read_input_txt()[0].strip().split()]

    def do_the_thing(self, n):
        tqdm_total = n
        ll = LL(Node(self.raw[0]))
        for i in self.raw[1:]:
            ll.append(i)
        ll.print()

        pbar = tqdm(total=tqdm_total, ncols=100)
        for blink in range(n):
            n_i = 0
            for node in ll:
                new_nodes = blink_stone(node.value)
                #self.debug(f'blinked {node.value} -> {new_nodes}')
                node.value = new_nodes[0]
                if len(new_nodes) == 2:
                    node.value = new_nodes[1]
                    #self.debug(f'inserting {new_nodes[0]} before {node.value}')
                    new = Node(new_nodes[0])
                    if n_i > 0:
                        new.prev = node.prev
                        node.prev = new
                        new.prev.next = new
                        new.next = node
                        ll.length += 1
                    elif n_i == 0:
                        ll.push(new_nodes[0])
                        n_i += 1

                    #ll.insert(n_i, new_nodes[0])
                    n_i += 1
                n_i += 1
            
            #self.debug(f'after {blink+1} blinks: {ll.length}')
            #if self._debug:
            #    ll.print()
            pbar.update(1)
        pbar.close()
        return ll.length

    def part1(self):
        """
        """
        return self.do_the_thing(25)

    def part2(self):
        """
        """

        n = 75
        @cache
        def blink_r(v, n):
            tot = 0
            for new_v in blink_stone(v):
                #self.debug(f'{v} -> {new_v}')
                if n > 0:
                    tot += blink_r(new_v, n-1)
                else:
                    tot += 1
            return tot
        
        total = 0
        for i in self.raw:
            total += blink_r(i, n-1)
        return total
