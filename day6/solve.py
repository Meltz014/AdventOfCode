import numpy

class Node():
    def __init__(self):
        self.orbits = None

def count(root):
    if not root.orbits:
        return 0
    return 1 + count(root.orbits)

def path_to_root(node):
    path = []
    while node:
        path.append(node.orbits)
        node = node.orbits
    return path

def main():
    # part 1
    #data = """COM)B B)C C)D D)E E)F B)G G)H D)I E)J J)K K)L"""
    with open('day6\input.txt') as fid:
        data = fid.readlines()

    nodes = {}
    root = None
    for o in data:
        [left, right] = o.strip().split(')')
        if left not in nodes:
            nodes[left] = Node()
        if right not in nodes:
            nodes[right] = Node()

        nodes[right].orbits = nodes[left]

    print(f'Part 1: {sum([count(c) for (k, c) in nodes.items()])}')

    # part 2
    #data = "COM)B B)C C)D D)E E)F B)G G)H D)I E)J J)K K)L K)YOU I)SAN".split()

    # find path to root for YOU and SAN
    you_path = path_to_root(nodes['YOU'])
    san_path = path_to_root(nodes['SAN'])
    l_y = len(you_path)
    l_s = len(san_path)

    """
     |-------------L1-----------|

                    /-------b---|YOU
     |---overlap---|
                    \--------c----------|SAN

     |--------------L2-----------------|

      unique = L1 + L2 - overlap
      overlap = L1 + L2 - unique
      dist = (L1 - overlap) + (L2 - overlap)
    """

    unique = len(set(you_path + san_path))
    overlap = l_y + l_s - unique
    distance = l_y + l_s - overlap*2

    print(f'Part 2: {distance}')

if __name__ == '__main__':
    main()
