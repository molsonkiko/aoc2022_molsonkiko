import random
import re
import unittest
import colorama
from colorama import Fore

colorama.init()

def show_where_searched_part1(places_tail_visited: dict[tuple[int], int],
                        places_head_visited: dict[tuple[int], int],
                        show_head=True) -> str:
    minx = min(places_head_visited, key=lambda x: x[1])[1]
    maxx = max(places_head_visited, key=lambda x: x[1])[1]
    miny = min(places_head_visited, key=lambda x: x[0])[0]
    maxy = max(places_head_visited, key=lambda x: x[0])[0]
    colors = [Fore.RED, Fore.LIGHTMAGENTA_EX, Fore.BLUE, Fore.CYAN, Fore.GREEN]
    head_not_tail = set(places_head_visited) - set(places_tail_visited)
    out = ''
    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            if show_head and (y, x) in head_not_tail:
                idx = places_head_visited[(y, x)]
                if idx == 1:
                    color = Fore.WHITE
                else:
                    color_idx = idx * 5 // (len(places_head_visited) + 1)
                    color = colors[color_idx]
                out += color + 'H' + Fore.RESET
            elif (y, x) in places_tail_visited:
                idx = places_tail_visited[(y, x)]
                if idx == 0:
                    color = Fore.WHITE
                else:
                    color_idx = idx * 5 // (len(places_head_visited) + 1)
                    color = colors[color_idx]
                out += color + '#' + Fore.RESET
            else:
                out += '.'
        out += '\n'
    return out


def show_where_searched_part2(places_visited: dict[tuple[int], int]) -> str:
    places_head_visited = places_visited[0]
    minx = min(places_head_visited, key=lambda x: x[1])[1]
    maxx = max(places_head_visited, key=lambda x: x[1])[1]
    miny = min(places_head_visited, key=lambda x: x[0])[0]
    maxy = max(places_head_visited, key=lambda x: x[0])[0]
    colors = [Fore.RED, Fore.LIGHTMAGENTA_EX, Fore.BLUE, Fore.CYAN, Fore.GREEN]
    out = ''
    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            visited = False
            for ii, places_ii_visited in places_visited.items():
                if (y, x) in places_ii_visited:
                    visited = True
                    idx = places_ii_visited[(y, x)]
                    if idx == 0:
                        color = Fore.WHITE
                    else:
                        color_idx = idx * 5 // (len(places_ii_visited) + 1)
                        color = colors[color_idx]
                    out += color + str(ii) + Fore.RESET
                    break
            if not visited:
                out += '.'
        out += '\n'
    return out


def Part1(lines: list[str], verbose=False):
    headx, heady = 0, 0
    tailx, taily = 0, 0
    places_tail_visited = {(0, 0): 0}
    places_head_visited = {(0, 0): 0}
    if verbose:
        print('START AT (0, 0)')
    for line in lines:
        if not line:
            continue
        direction, numstr = line.split()
        num = int(numstr)
        if verbose:
            print(f'{line}, {len(places_tail_visited)} places tail visited')
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
                places_tail_visited[(tailx, taily)] = len(places_tail_visited)
            places_head_visited[(headx, heady)] = len(places_head_visited)
            if verbose:
                print(f'head at {(headx, heady)}, tail at {(tailx, taily)}')
    if verbose:
        searched_str = show_where_searched_part1(places_tail_visited, places_head_visited)
        print(searched_str)
    return len(places_tail_visited)


def Part2(lines: list[str], verbose=False, snake_len = 10) -> int:
    locs = [[0, 0] for ii in range(snake_len)]
    places_visited = {ii: {(0, 0): 0} for ii in range(snake_len)}
    for ii, line in enumerate(lines):
        if not line:
            continue
        direction, numstr = line.split()
        num = int(numstr)
        if verbose:
            print(f'{line}, {len(places_visited[snake_len - 1])} places tail visited')
            print(f'snake = {locs}')
        for ii in range(num):
            if direction == 'R':
                locs[0][0] += 1
            elif direction == 'L':
                locs[0][0] -= 1
            elif direction == 'U':
                locs[0][1] += 1
            elif direction == 'D':
                locs[0][1] -= 1
            places_visited[0][tuple(locs[0])] = len(places_visited[0])
            for ii in range(1, snake_len):
                head = locs[ii-1]
                tail = locs[ii]
                if head[0] - tail[0] > 1:
                    if head[1] - tail[1] >= 1:
                        locs[ii][1] += 1
                    elif tail[1] - head[1] >= 1:
                        locs[ii][1] -= 1
                    locs[ii][0] += 1
                elif tail[0] - head[0] > 1:
                    if head[1] - tail[1] >= 1:
                        locs[ii][1] += 1
                    elif tail[1] - head[1] >= 1:
                        locs[ii][1] -= 1
                    locs[ii][0] -= 1
                elif head[1] - tail[1] > 1:
                    if head[0] - tail[0] >= 1:
                        locs[ii][0] += 1
                    elif tail[0] - head[0] >= 1:
                        locs[ii][0] -= 1
                    locs[ii][1] += 1
                elif tail[1] - head[1] > 1:
                    if head[0] - tail[0] >= 1:
                        locs[ii][0] += 1
                    elif tail[0] - head[0] >= 1:
                        locs[ii][0] -= 1
                    locs[ii][1] -= 1
                places_visited[ii][(tuple(locs[ii]))] = len(places_visited[ii])
            if verbose:
                print(f'head at {tuple(locs[0])}, tail at {tuple(locs[-1])}')
    if verbose:
        print(f'snake = {locs}')
        searched_str = show_where_searched_part2(places_visited)
        print(searched_str)
    return len(places_visited[snake_len - 1])

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

    def test_diagonal_down_and_left_then_up_then_right(self):
        '''
          (9)
        HT...TTTTH
        ##...####T
        ::::::::::: (109)
        ##...T###T
        ##...HT##T
        ##...#HT#T
        ##...##HTH
        ##...###HH
        '''
        inp = ['D 1', 'L 1', 'D 1', 'L 1', 'D 1', 'L 1', 'D 1', 'L 1',
                'U 115',
                'R 15']
        self.assertEqual(Part1(inp), 4 + 13 + 114)


TEST2_INPUT2 = [
    "R 5",
    "U 8",
    "L 8",
    "D 3",
    "R 17",
    "D 10",
    "L 25",
    "U 20",
]

RADIUS_6_CIRCLE = [
    'D 6',
    'L 6',
    'U 12',
    'R 12',
    'D 12',
    'L 6',
    'U 5',
    'L 1',
]

RANDOM_INSTRUCTIONS = []
random.seed(15)
for ii in range(25):
    direction = random.choice('RDLU')
    RANDOM_INSTRUCTIONS.append(f'{direction} {random.randint(1, 15)}')
random.seed(None)

class TestPart2(unittest.TestCase):
    def testPart2_sample_input(self):
        self.assertEqual(Part2(SAMPLE_INPUT), 1)

    def test_sample_input_2(self):
        self.assertEqual(Part2(TEST2_INPUT2), 36)

    def test_radius_13_circle_around_start(self):
        '''
        HHHHHHHHHHH
        H.........H
        H.........H
        H.........H
        H.........H
        H...HHHHHHH
        H...H......
        H...H......
        H...H......
        H...H......
        H...H......
        HHHHHHHHHHH
        '''
        self.assertEqual(Part2(RADIUS_6_CIRCLE), 10)

    def test_random_instructions(self):
        self.assertEqual(Part2(RANDOM_INSTRUCTIONS), 79)

    def test_up_10_right_5(self):
        '''
        000000
        023...
        034...
        045...
        056...
        067...
        078...
        089...
        09....
        0.....
        '''
        self.assertEqual(Part2(['U 10', 'R 5']), 4)


if __name__ == '__main__':
    with open('day9_input.txt') as f:
        lines = re.split('\r?\n', f.read())
    part1_answer = Part1(lines)
    print(f'part 1 answer = {part1_answer}')
    part2_answer = Part2(lines) # 2509 is wrong
    print(f'part 2 answer = {part2_answer}')
    unittest.main()