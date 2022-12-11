import re
import unittest

def Part1(lines: list[str]):
    headx, heady = 0, 0
    tailx, taily = 0, 0
    places_visited = set((0, 0))
    # print('START AT (0, 0)')
    for line in lines:
        if not line:
            continue
        direction, numstr = line.split()
        num = int(numstr)
        # print(f'{line}, {len(places_visited)} places visited')
        for ii in range(num):
            old_headx, old_heady = headx, heady
            if direction == 'R':
                headx += 1
            elif direction == 'L':
                headx -= 1
            elif direction == 'U':
                heady += 1
            elif direction == 'D':
                heady -= 1
            if abs(headx - tailx) > 1 or abs(heady - taily) > 1:
                tailx = old_headx
                taily = old_heady
                places_visited.add((tailx, taily))
            # print(f'head at {(headx, heady)}, tail at {(tailx, taily)}')
    return len(places_visited)


def Part2(lines: list[str]) -> int:
    return 0


SAMPLE_INPUT = [
    "R 4",
    "U 4",
    "L 3",
    "D 1",
    "R 4",
    "D 1",
    "L 5",
    "R 2",
]


class Part1Tests(unittest.TestCase):
    def test_sample_input(self):
        self.assertEqual(Part1(SAMPLE_INPUT), 13)

    def test_radius1_circle_around_start(self):
        '''
        H H H
        H T H
        H H H
        '''
        inp = [
            'R 1',
            'U 1',
            'L 2',
            'D 2',
            'R 2',
            'U 1',
            'L 1'
        ]
        self.assertEqual(Part1(inp), 1)

    def test_radius2_circle_around_start(self):
        '''
        H T T T H
        T # # # T
        T # T T H
        T # # # T
        H T T T H
        '''
        inp = [
            'R 2', # tail goes right 1
            'U 2', # tail goes diagonally up-right 1
            'L 4', # tail goes diagonally up-left 1, then left 2
            'D 4', # tail goes diagonally down-left 1, then down 2
            'R 4', # tail goes diagonally down-right 1, then right 2
            'U 2', # tail goes diagonally up-right one
        ]
        self.assertEqual(Part1(inp), 13)

    def test_radius2_circle_around_start_then_back_to_start(self):
        '''
        H T T T H
        T # # # T
        T # T T H
        T # # # T
        H T T T H
        '''
        inp = [
            'R 2', # tail goes right 1
            'U 2', # tail goes diagonally up-right 1
            'L 4', # tail goes diagonally up-left 1, then left 2
            'D 4', # tail goes diagonally down-left 1, then down 2
            'R 4', # tail goes diagonally down-right 1, then right 2
            'U 2', # tail goes diagonally up-right one
            'D 2',
            'L 4',
            'U 4',
            'R 4',
            'D 2',
            'L 2', # back to start
        ]
        self.assertEqual(Part1(inp), 13)

    def test_horizontal_lines(self):
        inp = ['R 5', 'L 5', 'R 5', 'L 5']
        self.assertEqual(Part1(inp), 5)

    def test_vertical_lines(self):
        inp = ['U 5', 'D 5', 'U 5', 'D 5']
        self.assertEqual(Part1(inp), 5)

    def test_diagonal_up_and_right(self):
        '''
        ##HH
        #HT#
        HT##
        T###
        '''
        inp = ['U 1', 'R 1', 'U 1', 'R 1', 'U 1', 'R 1']
        self.assertEqual(Part1(inp), 3)


class TestPart2(unittest.TestCase):
    def testPart2_sample_input(self):
        self.assertEqual(Part2(SAMPLE_INPUT), 0)


if __name__ == '__main__':
    with open('day9_input.txt') as f:
        lines = re.split('\r?\n', f.read())
    part1_answer = Part1(lines)
    print(f'part 1 answer = {part1_answer}')
    part2_answer = Part2(lines)
    print(f'part 2 answer = {part2_answer}')
    unittest.main()