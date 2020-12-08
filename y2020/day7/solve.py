import re

test_data = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

def contains(tree, content, target):
    for (_, bag) in content:
        if bag == target:
            return True
        else:
            if contains(tree, tree[bag], target):
                return True
    return False

def part1(tree):
    # look for bags containing a target
    target = 'shiny gold'
    count = 0
    for (bag, content) in tree.items():
        count += int(contains(tree, content, target))
    print(f'Part1: {count}')

def count_children(tree, contents):
    count = 1 # include self
    for (quant, bag) in contents:
        count += quant * count_children(tree, tree[bag])
    return count

def part2(tree):
    target = 'shiny gold'
    print(f'Part2 {count_children(tree, tree[target])-1}')

def main():

    with open('day7\input.txt') as fid:
        tree = {}
        root_pattern = re.compile(r'(\w+\s\w+)\sbags\scontain\s(no\sother\sbags|.*)\.')
        child_pattern = re.compile(r'\s*(\d+)\s(\w+\s\w+).*')
        for line in fid:
            line = line.strip()
            mobj = root_pattern.match(line)
            (root_key, contains) = mobj.groups()
            children = []
            if 'no other' not in contains:
                for child in contains.split(','):
                    child_mobj = child_pattern.match(child)
                    (quant, name) = child_mobj.groups()
                    children.append((int(quant), name))
            tree[root_key] = children

    part1(tree)
    part2(tree)

if __name__ == '__main__':
    main()