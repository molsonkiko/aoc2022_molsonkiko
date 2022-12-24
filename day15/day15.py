from dataclasses import dataclass
import re
import unittest

class Shape:
    def __init__(self):
        raise NotImplementedError("The Shape class should only be inherited, not instantiated.")

    @property
    def area(self) -> int:
        raise NotImplementedError

    def overlap(self, other):
        '''returns one or more shapes that define the overlap between this shape and another shape.
        If no overlap, return an empty list'''
        raise NotImplementedError

    def overlap_area(self, other) -> int:
        '''return the total area of all shapes in the overlap between self and other'''
        return sum(shape.area for shape in self.overlap(other))


'''
shape like this
...#...
..###..
.#####.
..###..
...#...
'''
@dataclass
class Diamond(Shape):
    x: int
    y: int
    radius: int

    @property
    def area(self) -> int:
        return (self.radius + 1) * (self.radius + 1) + \
               (self.radius * self.radius)

    def distance(self, other) -> int:
        return manhattan_distance(self.x, self.y, other.x, other.y)
    
    def overlap(self, other):
        '''
        other: another Shape

        make one or more shapes containing the overlap between the two
        
        If no overlap, return [].
        
        Cases (C and D are the centers of diamonds 1 and 2, resp.):

1. x-aligned or y-aligned overlap
    1a. Aligned overlap by one or two squares

    Result: one or two points
```
r1 * r2 - dist = 2, overlap = 2
..........
...1..2...
..111222..
.11CXXD22.
..111222..
...1..2...
..........
```
    1b. Aligned overlap by >= 3 squares

    Result: diamond
```
r1 + r2 - dist = 3, overlap = 5
..........
...1.2....
..11X22...
.11XXX22..
..11X22...
...1.2....
..........
```
    1c. Aligned overlap by even number of squares >= 4

    Result: a dimaond and two adjacent diagonal line segments
```
r1 + r2 - dist = 4, overlap = 8
........
...12...
..1XX2..
.1XXXX2.
..1XX2..
...12...
```
2. Unaligned overlap (self.x != other.x and self.y != other.y)

Result: some number of parallel adjacent lines

Example 1 (self.radius + other.radius - dist = 0)
```
r1 + r2 - dist = 0, overlap = 3
..............
........1.....
.......111....
......11111...
.....111C111..
......X1111...
.....22X11....
....22D2X.....
.....222......
......2.......
```
Example 2 (self.radius + other.radius - dist = 1)
```
r1 + r2 - dist = 1, overlap = 6
..........1.....
.........111....
........11111...
.......1X1C111..
.......2XX111...
......222XX1....
.....222D2X2....
......22222.....
.......222......
........2.......
```
Example 3 (self.radius + other.radius - dist = 2)
```
r1 + r2 - dist = 2, overlap = 8
..............
.........1....
......2.111...
.....22X1111..
....22XXXC111.
...222DXXX11..
....2222X11...
.....222.1....
......2.......
..............
```
Example 4 (self.radius + other.radius - dist = 3)
```
r1 + r2 - dist = 3, overlap = 12
..............
........1.....
.......111....
.....211111...
....2XX11111..
...2XXXXC1111.
..222XXXX111..
...222XX111...
....222111....
.....2..1.....
```
NOTE: We DO NOT need to consider the case where one diamond is
contained in another, because the structure of the problem makes that impossible.
        '''
        dist = self.distance(other)
        if dist > self.radius + other.radius:
            return []
        # special case when two diamonds are aligned on one axis:
        # overlap area is also a diamond
        if self.x == other.x:
            if other.y > self.y:
                close_to_other = self.y + self.radius
                close_to_self = other.y - other.radius

    def overlap_area(self, other):
        return super().overlap_area(other)


class LineSegment(Shape):
    x1: int
    y1: int
    x2: int
    y2: int

    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        '''
Can represent horizontal, vertical, or 45-degree line segments.

OK
```
..#..
..#..
..#..
```
OK
```
....
####
....
```
OK
```
#..
.#.
..#
```
NOT OK
```
.#....
...#..
.....#
```
        '''
        diffx = abs(x1 - x2)
        diffy = abs(y1 - y2)
        if diffx != 0 and diffy != 0 and diffy != diffx:
            raise ValueError("LineSegment type only supports 45-degree, vertical, and horizontal line segments")
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def area(self) -> int:
        xdiff = self.x1 - self.x2
        if xdiff != 0:
            return abs(xdiff) + 1
        return abs(self.y1 - self.y2) + 1

    @property
    def rise(self) -> int:
        return self.x2 - self.x1
    
    @property
    def run(self) -> int:
        return self.y2 - self.y1

    @property
    def slope(self) -> float:
        if self.run == 0:
            return float('inf')
        return self.rise / self.run

    def overlap(self, other: Shape) -> list[Shape]:
        '''
Example:
>>> self =  LineSegment(x1=1, y1=6, x2=7, y2=0)
>>> other = LineSegment(x1=0, y1=2, x2=5, y2=7)
    xx   x x
    os   o s
    11   2 2
yo2 .....o.. 7
ys1 .s..o... 6
    ..so.... 5
    ..os.... 4
    .o..s... 3
yo1 o....s.. 2
    ......s. 1
ys2 .......s 0
    0 2 4 6
        '''
        if isinstance(other, Diamond):
            raise NotImplementedError
        if isinstance(other, LineSegmentBundle):
            raise NotImplementedError
        xs1, xs2 = self.x1, self.x2
        if xs1 > xs2:
            xs1, xs2 = xs2, xs1
        xo1, xo2 = self.x1, self.x2
        if xo1 > xo2:
            xo1, xo2 = xo2, xo1
        ys1, ys2 = self.y1, self.y2
        if ys1 > ys2:
            ys1, ys2 = ys2, ys1
        yo1, yo2 = other.y1, other.y2
        if yo1 > yo2:
            yo1, yo2 = yo2, yo1
        allx = sorted([xs1, xs2, xo1, xo2])
        # Since sorted() is a stable sort, the possible allx arrangements are:
        # xs1 xs2 xo1 xo2 (overlap 0 or 1)
        # xs1 xo1 xs2 xo2 (overlap > 1, no containment)
        # xs1 xo1 xo2 xs2 (self contains other)
        # xo1 xs1 xs2 xo2 (other contains self)
        # xo1 xs1 xo2 xs2 (overlap > 1, no containment)
        # xo1 xo2 xs1 xs2 (overlap 0 or 1)
        ally = sorted([ys1, ys2, yo1, yo2])
        # ally has the same arrangement patterns as allx, subsituting y for x
        if ys2 < yo1 or yo2 < ys1 or xs2 < xo1 or xo2 < xs1:
            # if all of self is above all of other
            # or all of other is above all of self
            # or all of other is left of self
            # or all of other is right of self,
            # there is no overlap
            return []
        # self is vertical
        if self.run == 0:
            # other is also vertical
            if other.run == 0:
                if ally[1] == ys2:
                    # ys1 ys2 yo1 yo2 (overlap 0 or 1, but we ruled out 0 earlier)
                    return [LineSegment(xs1, ys2, xs1, ys2)]
                if ally[1] == yo2:
                    # yo1 yo2 ys1 ys2 (overlap 1, because 0 ruled out)
                    return [LineSegment(xs1, ys1, xs1, ys1)]
                if ally[1] == yo1:
                    # ys1 yo1 ys2 yo2 (overlap > 1, no containment)
                    if ally[2] == ys2:
                        return [LineSegment(xs1, yo1, xs1, ys2)]
                    # ys1 yo1 yo2 ys2 (self contains other)
                    return [LineSegment(xs1, yo1, xs1, yo2)]
                # ally[1] is ys1
                # yo1 ys1 ys2 yo2 (other contains self)
                if ally[2] == ys2:
                    return [LineSegment(xs1, ys1, xs1, ys2)]
                # yo1 ys1 yo2 ys2 (overlap > 1, no containment)
                return [LineSegment(xs1, ys1, xs1, yo2)]
            # other is not vertical
            if other.rise == 0:
                # other is horizontal
                return [LineSegment(xs1, yo1, xs1, yo1)]
            # other is 45-degree
            # .o....
            # ..os..
            # ...X..
            # ...so.
            # ......
            y_intersect = other.y2 + other.slope * (self.x2 - other.x2)
            return [LineSegment(xs1, y_intersect, xs1, y_intersect)]
        # other is vertical, self not vertical
        if other.run == 0:
            if self.rise == 0:
                # self is horizontal
                return [LineSegment(xo1, ys1, xo1, ys1)]
            # self is 45-degree
            y_intersect = self.y2 + self.slope * (other.x2 - self.x2)
            return [LineSegment(xo1, y_intersect, xo1, y_intersect)]
        # self is horizontal, other not vertical
        if self.rise == 0:
            # other is also horizontal
            if other.rise == 0:
                if allx[1] == xs2:
                    # xs1 xs2 yo1 yo2 (overlap 1 or 0, but we ruled out 0 earlier)
                    return [LineSegment(xs2, ys1, xs2, ys1)]
                if allx[1] == xo2:
                    # xo1 xo2 xs1 xs2 (overlap 1, because 0 ruled out earlier)
                    return [LineSegment(xo2, ys1, xo2, ys1)]
                if allx[1] == xo1:
                    # xs1 xo1 xs2 xo2 (overlap > 1, containment)
                    if allx[2] == xs2:
                        return [LineSegment(xo1, ys1, xs2, yo2)]
                    # xs1 xo1 xo2 xs2 (overlap > 1, self contains other)
                    return [LineSegment(xo1, ys1, xo2, ys2)]
                # allx[1] is ys1
                # xo1 xs1 xs2 xo2 (other contains self)
                if allx[2] == xs2:
                    return [LineSegment(xs1, ys1, xs2, ys1)]
                # xo1 xs1 xo2 xs2 (overlap > 1, no containment)
                return [LineSegment(xs1, ys1, xo2, ys1)]
            # other is 45-degree
            # .o....
            # ..o...
            # ..sXs.
            # ....o.
            # ......
            x_intersect = other.x1 + (self.y1 - other.y1) / other.slope
            return [LineSegment(x_intersect, ys1, x_intersect, ys1)]
        # both are 45-degree
        # four cases-
        # 1. overlap
        # .o...
        # ..X..
        # ...X.
        # ....s
        # 2. intersection
        # .o.s.
        # ..X..
        # .s.o.
        # 3. No intersection because of integer requirement
        # .os.
        # .so.
        # s..o
        # 4. Parallel with overlapping x and y ranges
        # .o....
        # ..o...
        # .s.o..
        # ..s.o.
        # 5. Opposite slopes, non-intersecting, overlapping x and y ranges
        # .o....
        # ..o...
        # .s.o..
        # s...o.
        other_y_at_self_y1 = other.y1 + other.slope * (self.x1 - other.x1)
        # need to check if they overlap, because of cases 4 and 5 above
        if other_y_at_self_y1 != self.y1:
            # self has a different y from other when other.x = self.x1
            return []
        if self.slope == other.slope:
            # they overlap (Case 1)
            if self.slope > 0:
                # in this case xs1 and ys1 are always part of the same point
                # because positive slope implies that the point with the
                # greater x also has the greater y
                #     x xx x
                #     s os o
                #     1 12 2
                # yo2 .....o
                #     ....o.
                # ys2 ...X..
                # yo1 ..X...
                #     .s....
                # ys1 s.....
                if xs2 == allx[1]:
                    # xs1 xs2 xo1 xo2
                    return [LineSegment(xs2, ys2, xo1, yo1)]
                if xo1 == allx[1]:
                    if xs2 == allx[2]:
                        return [LineSegment(xo1, yo1, xs2, ys2)]
                    return [LineSegment(xo1, yo1, xo2, yo2)]
                if xs1 == allx[1]:
                    if xs2 == allx[2]:
                        return [LineSegment(xs1, ys1, xs2, ys2)]
                    return [LineSegment(xs1, ys1, xo2, yo2)]
                # xo2 == allx[1]
                return [LineSegment(xo2, yo2, xs1, ys1)]
            # both slopes are negative
            # now xs1 and ys2 are part of the same point
            #     x xx x
            #     o so s 
            #     1 12 2
            # yo2 o.....
            #     .o....
            # ys2 ..X...
            # yo1 ...X..
            #     ....s.
            # ys1 .....s
            if xs2 == allx[1]:
                return [LineSegment(xs2, ys1, xo1, yo2)]
            if xo1 == allx[1]:
                if xs2 == allx[2]:
                    return [LineSegment(xo1, yo2, xs2, ys1)]
                return [LineSegment(xo1, yo2, xo2, yo1)]
            if xs1 == allx[1]:
                if xs2 == allx[2]:
                    return [LineSegment(xs1, ys2, xs2, ys1)]
                return [LineSegment(xs1, ys2, xo2, yo1)]
            return [LineSegment(xo2, yo1, xs1, ys2)]
        # one has + slope, other has - slope
        #     xx  xx
        #     os  os 
        #     11  22
        # yo2 o.....
        # ys2 .o...s
        #     ..o.s.
        #     ...X..
        # yo1 ..s.o.
        # ys1 .s....
        # need to solve this system of two equations
        # self  : ax + by - c = 0
        # other : qx + ry - s = 0
        # (a - q)x + (b - r)y - c + s = 0
        # self.slope = a / b
        # other.slope = q / r
        # c / a = self.x_intercept = -self.y1 / self.slope
        #         

    def overlap_area(self, other: Shape):
        return super().overlap_area(other)


class LineSegmentBundle(Shape):
    pass


def parse_lines(lines: list[str]) -> tuple[list[tuple[int]]]:
    sensor_locs = []
    beacon_locs = []
    for line in lines:
        sens_x, sens_y, beac_x, beac_y = map(int, 
            re.findall('-?\d+', line))
        sensor_locs.append((sens_x, sens_y))
        beacon_locs.append((beac_x, beac_y))
    return sensor_locs, beacon_locs

def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x2 - x1) + abs(y2 - y1)

def sensor_coverage(sensors: list[tuple[int]], 
        beacons: list[tuple[int]]) -> list[Diamond]:
    out = []
    for (sx, sy), (bx, by) in zip(sensors, beacons):
        dist = manhattan_distance(sx, sy, bx, by)
        coverage = Diamond(sx, sy, dist)
        out.append(coverage)
    return out

def total_coverage_area(coverages: list[Diamond]) -> int:
    '''
    Compute the total area covered by any number of diamonds,
    counting overlap areas only once.
``` 
               1    1    2    2
     0    5    0    5    0    5
-2 ..........#.................
-1 .........###................
 0 ....S...#####...............
 1 .......#######........S.....
 2 ......#########S............
 3 .....###########SB..........
 4 ....#############...........
 5 ...###############..........
 6 ..#################.........
 7 .#########S#######S#........
 8 ..#################.........
 9 ...###############..........
10 ....B#########X##...........
11 ..S..########XXX............
12 ......######XXX##...........
13 .......####XXX####..........
14 ........##XXX#S####...S.....
15 B........##X######..........
16 ..........#SB####...........
17 .............###S..........B
18 ....S.........#.............
19 ............................
20 ............S......S........
21 ............................
22 .......................B....-
```
    '''
    tot_cov_area = 0
    for ii in range(len(coverages)):
        cov1 = coverages[ii]
        tot_cov_area += cov1.area
        # now subtract the overlap with other coverage areas
        for jj in range(ii + 1, len(coverages)):
            tot_cov_area -= cov1.overlap_area(coverages[jj])
        

def Part1(lines: list[str]):
    coverages = sensor_coverage(*parse_lines(lines))


def Part2(lines: list[str]) -> int:
    return 0


SAMPLE_INPUT = [
    "Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
    "Sensor at x=9, y=16: closest beacon is at x=10, y=16",
    "Sensor at x=13, y=2: closest beacon is at x=15, y=3",
    "Sensor at x=12, y=14: closest beacon is at x=10, y=16",
    "Sensor at x=10, y=20: closest beacon is at x=10, y=16",
    "Sensor at x=14, y=17: closest beacon is at x=10, y=16",
    "Sensor at x=8, y=7: closest beacon is at x=2, y=10",
    "Sensor at x=2, y=0: closest beacon is at x=2, y=10",
    "Sensor at x=0, y=11: closest beacon is at x=2, y=10",
    "Sensor at x=20, y=14: closest beacon is at x=25, y=17",
    "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
    "Sensor at x=16, y=7: closest beacon is at x=15, y=3",
    "Sensor at x=14, y=3: closest beacon is at x=15, y=3",
    "Sensor at x=20, y=1: closest beacon is at x=15, y=3",
]


class Part1Tests(unittest.TestCase):
    def testPart1_sample_input(self):
        self.assertEqual(Part1(SAMPLE_INPUT), 0)


class TestPart2(unittest.TestCase):
    def testPart2_sample_input(self):
        self.assertEqual(Part2(SAMPLE_INPUT), 0)


if __name__ == '__main__':
    with open('day15_input.txt') as f:
        lines = re.split('\r?\n', f.read())
    part1_answer = Part1(lines)
    print(f'part 1 answer = {part1_answer}')
    part2_answer = Part2(lines)
    print(f'part 2 answer = {part2_answer}')
    unittest.main()