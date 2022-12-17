from AoC import AoC
import re
import numpy as np
import matplotlib.pyplot as plt

def manhattan(p1, p2):
    return np.absolute(p2-p1).sum()

class Solver(AoC):
    example_data = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

    def parse(self):
        raw = self.read_input_txt(split=True)
        self.sensors = []
        self.beacons = []
        self.dist = []
        for line in raw:
            sx, sy, bx, by = re.findall(r'-?\d+', line)
            sensor = np.array([int(sx), int(sy)])
            beacon = np.array([int(bx), int(by)])
            self.dist.append(manhattan(beacon,sensor))
            self.sensors.append(sensor)
            self.beacons.append(beacon)
        print(self.sensors)
        print(self.beacons)
        print(self.dist)

    def part1(self):
        tot = 0
        minx = min( min(self.sensors, key=lambda s: s[0])[0], min(self.beacons, key=lambda b: b[0])[0] ) - max(self.dist)
        maxx = max( max(self.sensors, key=lambda s: s[0])[0], max(self.beacons, key=lambda b: b[0])[0] ) + max(self.dist)
        miny = min( min(self.sensors, key=lambda s: s[1])[1], min(self.beacons, key=lambda b: b[1])[1] ) - max(self.dist)
        maxy = max( max(self.sensors, key=lambda s: s[1])[1], max(self.beacons, key=lambda b: b[1])[1] ) + max(self.dist)
        print(minx, maxx, miny, maxy)

        if self._use_example:
            y = 10
        else:
            y = 2000000

        # get rid of all sensors not in range of y
        sensors = []
        beacons = []
        dist = []
        for (s, b, d) in zip(self.sensors, self.beacons, self.dist):
            if abs(s[1]-y) < d:
                sensors.append(s)
                beacons.append(b)
                dist.append(d)

        # find range on this row seen by each sensor
        ranges = []
        for (s, b, d) in zip(sensors, beacons, dist):
            dy = abs(y-s[1])
            dx = d-dy
            ranges.append((s[0]-dx, s[0]+dx))

        ranges.sort(key=lambda r: r[1])
        print(ranges)
        tot = 0
        prev = ranges[0][0]
        for (x1,x2) in ranges:
            if x1 > prev:
                tot += x2-x1
            else:
                tot += x2-prev
            prev = x2

        return tot # 4951427

    def part2(self):
        tot = 0
        print('Warning: takes over a minute!')
        if self._use_example:
            size = 20
        else:
            size = 4000000

        found = False
        for y in range(size):
            # get rid of all sensors not in range of y
            sensors = []
            beacons = []
            dist = []
            for (s, b, d) in zip(self.sensors, self.beacons, self.dist):
                if abs(s[1]-y) < d:
                    sensors.append(s)
                    beacons.append(b)
                    dist.append(d)

            # find range on this row seen by each sensor
            ranges = []
            existing = []
            for (s, b, d) in zip(sensors, beacons, dist):
                dy = abs(y-s[1])
                dx = d-dy
                ranges.append((s[0]-dx, s[0]+dx))
                if b[1] == y:
                    existing.append((b[0], b[1]))
                if s[1] == y:
                    existing.append((s[0], s[1]))

            ranges.sort(key=lambda r: r[0])
            #print(ranges)
            tot = ranges[0][0]
            x=0
            for (x1,x2) in ranges:
                if x1 > (tot+1):
                    x = x1-1
                    if (x,y) in existing:
                        # already a beacon/sensor here, move on
                        tot = x2
                        continue
                    print(x,y)
                    found = True
                    break
                tot = max(x2, tot)
            if found:
                break

        return int(x) * 4000000 + y