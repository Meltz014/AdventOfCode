import numpy
from collections import defaultdict
import math
import time

patterns = {}

max_x = 0
max_y = 0
KEYS  = 'abcdefghijklmnopqrstuvwxyz'
DOORS = KEYS.upper()

class Node():
    def __init__(self, x, y, val=None):
        self.x = x
        self.y = y
        self.key = None
        self.door = None
        if val and val in KEYS:
            self.key = val
        elif val and val in DOORS:
            self.door = val

        self.n = None
        self.s = None
        self.e = None
        self.w = None

    def __repr__(self):
        if self.key:
            s = f'Key: {self.key}'
        elif self.door:
            s = f'Door: {self.door}'
        else:
            s = ' empty'
        return f'<Node {self.x, self.y}: {s}>'

    @property
    def neighbors(self):
        return [n for n in [self.n, self.s, self.e, self.w] if n]

def _builder(node, grid, keys=None, doors=None):
    if keys is None:
        keys = []
    if doors is None:
        doors = []

    if node.key:
        keys.append(node)
    if node.door:
        doors.append(node)

    if not grid[node.x, node.y]['node']:
        grid[node.x, node.y]['node'] = node
    # N
    if node.y > 0:
        x = node.x
        y = node.y-1
        if grid[x, y]['val'] != '#':
            if grid[x, y]['node']:
                node.n = grid[x, y]['node']
            else:
                node.n = Node(x, y, grid[x, y]['val'])
                (keys, doors) = _builder(node.n, grid, keys=keys, doors=doors)
    # S
    if node.y < max_y:
        x = node.x
        y = node.y+1
        if grid[x, y]['val'] != '#':
            if grid[x, y]['node']:
                node.s = grid[x, y]['node']
            else:
                node.s = Node(x, y, grid[x, y]['val'])
                (keys, doors) = _builder(node.s, grid, keys=keys, doors=doors)
    # E
    if node.x > 0:
        x = node.x-1
        y = node.y
        if grid[x, y]['val'] != '#':
            if grid[x, y]['node']:
                node.e = grid[x, y]['node']
            else:
                node.e = Node(x, y, grid[x, y]['val'])
                (keys, doors) = _builder(node.e, grid, keys=keys, doors=doors)
    # W
    if node.x < max_x:
        x = node.x+1
        y = node.y
        if grid[x, y]['val'] != '#':
            if grid[x, y]['node']:
                node.w = grid[x, y]['node']
            else:
                node.w = Node(x, y, grid[x, y]['val'])
                (keys, doors) = _builder(node.w, grid, keys=keys, doors=doors)

    return (keys, doors)

def build_graph(data):
    global max_x, max_y
    grid = {}
    start = None
    for (y, row) in enumerate(data):
        if y > max_y:
            max_y = y
        for (x, c) in enumerate(row):
            if x > max_x:
                max_x = x
            grid[x,y] = {'val': c, 'node': None}
            if c == '@':
                start = (x,y)

    if not start:
        raise(Exception('Start not found!'))

    root = Node(start[0], start[1])
    (keys, doors) = _builder(root, grid)
    return root, keys, doors

def visible_keys(root, open_doors=None):
    if open_doors is None:
        open_doors = []
    queue = []
    visited = []
    visible = []
    prev = {}

    queue.append(root)
    while queue:
        node = queue.pop(0)
        for neigh in node.neighbors:
            if neigh not in visited and (not neigh.door or neigh.door in open_doors):
                queue.append(neigh)
                visited.append(neigh)
                prev[neigh] = node
                if neigh.key:
                    visible.append(neigh)

    return (visible, prev)

def traverse_key(root):
    # (node, visited_keys, prev_path)
    queue = [(root, [], {})]
    
    while queue:
        (cur_node, cur_visited_keys, cur_prev_path) = queue.pop(0)
        (vis, inner_prev_path) = visible_keys(cur_node)
        

def main():
    with open(r'day18\test1.txt') as fid:
        data = fid.readlines()
    root, keys, doors = build_graph(data)

    (vis, prev) = visible_keys(root)

    print(root)

if __name__ == '__main__':
    main()
