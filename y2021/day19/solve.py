from re import X
from AoC import AoC
import numpy as np

class Scanner:
    def __init__(self, beacons):
        self.max_idx = (2000,2000,2000)
        self.origin = (1000,1000,1000)
        self._beacons = [(x+self.origin[0], y+self.origin[1], z+self.origin[2]) for (x,y,z) in beacons]
        self.axis_positive = [1,1,1]
        self.origin_offset = (0,0,0)
    
    @property
    def beacons(self):
        b = []
        for (x,y,z) in self._beacons:
            b.append(((x-self.origin[0])*self.axis_positive[0],
                      (y-self.origin[1])*self.axis_positive[1],
                      (z-self.origin[2])*self.axis_positive[2]))
        return b

    def add_beacons(self, new):
        for (x,y,z) in new:
            beacon = ((x+self.origin[0])*self.axis_positive[0],
                      (y+self.origin[1])*self.axis_positive[1],
                      (z+self.origin[2])*self.axis_positive[2])
            if beacon not in self._beacons:
                self._beacons.append(beacon)
            else:
                raise Exception('Probably a bug here')

    def rotate(self, normal):
        """normal: axis normal to plane of rotation"""
        def rot_pt(pt):
            if normal == 0:
                return (pt[0], self.max_idx[2]-pt[2], pt[1])
            elif normal == 1:
                return (pt[2], pt[1], self.max_idx[0]-pt[0])
            else:
                return (self.max_idx[1]-pt[1], pt[0], pt[2])

        self._beacons = [rot_pt(pt) for pt in self._beacons]
        self.origin = rot_pt(self.origin)

    def flip(self, axis):
        self.axis_positive[axis] *= -1

    def translate(self, point):
        """move origin by point vector"""
        self.origin_offset = point
        self.origin = (self.origin[0]+point[0],
                       self.origin[1]+point[1],
                       self.origin[2]+point[2])

    def reset_origin(self):
        self.origin = (1000, 1000, 1000)

    def permute_orientations(self):
        yield
        self.rotate(0)
        yield
        self.rotate(0)
        yield
        self.rotate(0)
        yield
        self.rotate(0)
        self.rotate(1)
        yield
        self.rotate(2)
        yield
        self.rotate(2)
        yield
        self.rotate(2)
        yield
        self.rotate(2)
        self.rotate(0)
        yield
        self.rotate(1)
        yield
        self.rotate(1)
        yield
        self.rotate(1)
        yield
        self.rotate(1)
        self.rotate(0)
        yield
        self.rotate(2)
        yield
        self.rotate(2)
        yield
        self.rotate(2)
        yield
        self.rotate(2)
        self.rotate(0)
        yield
        self.rotate(1)
        yield
        self.rotate(1)
        yield
        self.rotate(1)
        yield
        self.rotate(1)
        self.rotate(2)
        self.rotate(2)
        self.rotate(2)
        yield
        self.rotate(0)
        yield
        self.rotate(0)
        yield
        self.rotate(0)
        yield
        self.rotate(0)
        self.rotate(2)
        self.rotate(2)
        self.rotate(0)




class Solver(AoC):
    example_datax = """--- scanner 0 ---
0,2,0
4,1,0
3,3,0

--- scanner 1 ---
-1,-1,0
-5,0,0
-2,1,0"""

    example_data = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""

    def parse(self):
        self.scanners = []
        raw = self.read_input_txt()
        beacons = []
        for line in raw:
            if not line.strip('\n'):
                continue
            if '---' == line[0:3]:
                if beacons:
                    self.scanners.append(Scanner(beacons))
                beacons = []
                continue
            point = [int(x) for x in line.strip('\n').split(',')]
            beacons.append(point)
        self.scanners.append(Scanner(beacons))

    def get_overlapping_beacons(self, s0, s1):
        s0b = set(s0.beacons)
        s1b = set(s1.beacons)
        return list(s0b & s1b), list(s1b-s0b)

    def part1(self):
        scanner0 = self.scanners.pop(0)
        self.scanners_absolute = [(0,0,0)]
        # pick any beacon to get relative dist from
        scanner0.translate(scanner0.beacons[0])
        s0_bidx = 0
        while self.scanners:
            overlappers = []
            for (si, scanner) in enumerate(self.scanners):
                overlaps = False
                for _ in scanner.permute_orientations():
                    if not overlaps:
                        # check overlap
                        points = scanner.beacons.copy()
                        for point in points:
                            scanner.reset_origin()
                            scanner.translate(point)
                            overlap, new = self.get_overlapping_beacons(scanner0, scanner)
                            if len(overlap) >= 12:
                                scanner0.add_beacons(new)
                                s_abs = (scanner0.origin_offset[0]-scanner.origin_offset[0],
                                         scanner0.origin_offset[1]-scanner.origin_offset[1],
                                         scanner0.origin_offset[2]-scanner.origin_offset[2])
                                self.scanners_absolute.append(s_abs)
                                overlaps = True
                                break
                        scanner.reset_origin()
                if overlaps:
                    overlappers.append(si)
            if overlappers:
                for o in sorted(overlappers, reverse=True):
                    self.scanners.pop(o)
            s0_bidx += 1
            s0_bidx %= len(scanner0.beacons)
            print(f'bidx: {s0_bidx}')
            scanner0.reset_origin()
            scanner0.translate(scanner0.beacons[s0_bidx])
            print(f'scanners left: {len(self.scanners)}')

        return len(scanner0.beacons)

    def part2(self):
        max_dist = 0
        for s0 in self.scanners_absolute:
            for s1 in self.scanners_absolute:
                if s1 is s0:
                    continue
                dist = abs(s1[0]-s0[0]) + abs(s1[1]-s0[1]) + abs(s1[2]-s0[2])
                if dist > max_dist:
                    max_dist = dist
        return max_dist