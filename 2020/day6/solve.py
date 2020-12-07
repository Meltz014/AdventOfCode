
def part1(lines):
    # union of each group's answers
    groups = []
    group = set()
    for line in lines:
        line = line.strip()
        if not line:
            # blank line.  Add cur to db and reset
            groups.append(group)
            group = set()
            continue
        group = group.union(set(line))
    # gotta add the last one
    groups.append(group)

    ans = sum([len(group) for group in groups])
    print(f'Part1: {ans}')

def part2(lines):
    # intersection of each group's answers
    groups = []
    group = set()
    group_init = False
    for line in lines:
        line = line.strip()
        if not line:
            # blank line.  Add cur to db and reset
            groups.append(group)
            group = set()
            group_init = False
            continue
        if not group_init:
            group = set(line)
            group_init = True
        else:
            group = group.intersection(set(line))
    # gotta add the last one
    groups.append(group)

    ans = sum([len(group) for group in groups])
    print(f'Part2: {ans}')

def main():
    with open('day6\input.txt') as fid:
        lines = fid.readlines()
    part1(lines)
    part2(lines)

if __name__ == '__main__':
    main()