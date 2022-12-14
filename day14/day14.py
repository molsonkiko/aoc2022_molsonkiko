import re
import unittest
import colorama
from colorama import Fore

colorama.init()

SAND_SOURCE = (500, 0)

def render_grid(grid: list[list[float]], xmin, colorize) -> str:
    out = []
    for y, row in enumerate(grid):
        line = []
        curval = 0.0
        for x, loc in enumerate(row):
            if loc == 0.0:
                if colorize and curval != 0.0:
                    curval = 0.0
                    # turn off color
                    line.append(Fore.RESET)
                line.append('.')
            elif loc == 1.0:
                if colorize and curval != 1.0:
                    curval = 1.0
                    # change from previous color to light red
                    line.append(Fore.RESET + Fore.LIGHTRED_EX)
                line.append('#')
            else:
                if colorize and curval != 2.0:
                    curval = 2.0
                    # change from previous color to yellow
                    line.append(Fore.RESET + Fore.YELLOW)
                line.append('o')
            if y == 0 and x == 500 - xmin + 2:
                line[-1] = 'X' # sand source
        if colorize:
            line.append(Fore.RESET)
        out.append(line)
    return '\n'.join(''.join(line) for line in out)

def get_lines(textlines: list[str]) -> list[list[float]]:
    lines = []
    xmin, ymin = 500, 500
    xmax, ymax = 500, -float('inf')
    for line in textlines:
        if not line:
            continue
        nums = [int(x) for x in re.findall('\d+', line)]
        xlast, ylast = nums[:2]
        for ii in range(2, len(nums), 2):
            x, y = nums[ii : ii + 2]
            if x > xmax:
                xmax = x + 1
            if x < xmin:
                xmin = x + 1
            if y > ymax:
                ymax = y + 1
            if y < ymin:
                ymin = y
            newline = ((xlast, ylast), (x, y))
            lines.append(newline)
            xlast, ylast = x, y
    return lines, xmin, ymin, xmax, ymax

def parse_textlines(textlines: list[str], verbose=False) -> list[list[float]]:
    lines, xmin, ymin, xmax, ymax = get_lines(textlines)
    # 0.0 means unblocked, 1.0 means stone, 2.0 means sand
    grid = [[0.0 for _ in range(xmin - 2, xmax + 2)]
            for _ in range(ymax + 3)]
    if verbose:
        print(f'{xmin = }, {ymin = }, {xmax = }, {ymax = }')
        print(f'max grid row = {len(grid) - 1}, max grid x coord = {len(grid[0]) - 1}')
    for (x1, y1), (x2, y2) in lines:
        # offset to leave 1-2 rows on each side
        # and 1 row below the lowest stone
        # and 4 rows above the highest stone
        x1 -= xmin - 2
        y1 -= ymin - 4
        x2 -= xmin - 2
        y2 -= ymin - 4
        if x1 == x2:
            if y1 > y2:
                y2, y1 = y1, y2
            for y in range(y1, y2 + 1):
                grid[y][x1] = 1.0
        else:
            if x1 > x2:
                x1, x2 = x2, x1
            for x in range(x1, x2 + 1):
                grid[y1][x] = 1.0
    return grid, xmin, ymin, xmax, ymax

def Part1(textlines: list[str], verbose=False) -> int:
    '''how much sand can fall in before any further
    sand falls into the abyss below?'''
    grid, xmin, _, _, _ = parse_textlines(textlines, verbose)
    sand_source_x = 500 - xmin + 2
    abyss = len(grid) - 1
    sand_fallen = 0
    falls_through = False
    while not falls_through:
        sand_x = sand_source_x
        sand_y = 0
        while True:
            next_sand_y = sand_y + 1
            if grid[next_sand_y][sand_x] == 0.0:
                # try falling straight down
                sand_y = next_sand_y
            elif grid[next_sand_y][sand_x - 1] == 0.0:
                # next try falling down and to the left
                sand_y = next_sand_y
                sand_x -= 1
            elif grid[next_sand_y][sand_x + 1] == 0.0:
                # next try falling down and to the right
                sand_y = next_sand_y
                sand_x += 1
            else:
                # can't fall, sand piles up here
                grid[sand_y][sand_x] = 2.0
                sand_fallen += 1
                break
            if sand_y == abyss:
                falls_through = True
                break
    if verbose:
        print(render_grid(grid, xmin, True))
    return sand_fallen

def Part2(textlines: list[str], verbose=False) -> int:
    '''how much sand can fall in before the sand source at
    (500, 0) is blocked by sand, assuming the y coordinate
    of the floor is 2 greater than the maximum y coordinate
    of a platform?'''
    lines, _, ymin, _, ymax = get_lines(textlines)
    yfloor = ymax + 2
    xmin = 500 - yfloor - 1
    xmax = 500 + yfloor + 2
    grid = [[0.0 for _ in range(xmin, xmax)] for _ in range(yfloor)] \
        + [[1.0 for _ in range(xmin, xmax)]] # floor
    if verbose:
        print(f'{xmin = }, {ymin = }, {xmax = }, {ymax = }')
        print(f'max grid row = {len(grid) - 1}, max grid x coord = {len(grid[0]) - 1}')
    for (x1, y1), (x2, y2) in lines:
        x1 -= xmin
        x2 -= xmin
        if x1 == x2:
            if y1 > y2:
                y2, y1 = y1, y2
            for y in range(y1, y2 + 1):
                grid[y][x1] = 1.0
        else:
            if x1 > x2:
                x1, x2 = x2, x1
            for x in range(x1, x2 + 1):
                grid[y1][x] = 1.0
    sand_source_x = 500 - xmin
    sand_fallen = 0
    while grid[0][sand_source_x] == 0.0:
        sand_x = sand_source_x
        sand_y = 0
        while True:
            next_sand_y = sand_y + 1
            if grid[next_sand_y][sand_x] == 0.0:
                # try falling straight down
                sand_y = next_sand_y
            elif grid[next_sand_y][sand_x - 1] == 0.0:
                # next try falling down and to the left
                sand_y = next_sand_y
                sand_x -= 1
            elif grid[next_sand_y][sand_x + 1] == 0.0:
                # next try falling down and to the right
                sand_y = next_sand_y
                sand_x += 1
            else:
                # can't fall, sand piles up here
                grid[sand_y][sand_x] = 2.0
                sand_fallen += 1
                break
    if verbose:
        print(render_grid(grid, xmin + 2, True))
    return sand_fallen, grid, xmin


SAMPLE_INPUT = [
    "498,4 -> 498,6 -> 496,6",
    "503,4 -> 502,4 -> 502,9 -> 494,9",
]


class Part1Tests(unittest.TestCase):
    def test_sample_input(self):
        '''
        .......X....
        ............
        .......o....
        ......ooo...
        .....#ooo##.
        ....o#ooo#..
        ...###ooo#..
        .....oooo#..
        ..o.ooooo#..
        .#########..
        ............
        ............
        '''
        self.assertEqual(Part1(SAMPLE_INPUT, True), 24)


class TestPart2(unittest.TestCase):
    def test_sample_input(self):
        ''''
        ............o............
        ...........ooo...........
        ..........ooooo..........
        .........ooooooo.........
        ........oo#ooo##o........
        .......ooo#ooo#ooo.......
        ......oo###ooo#oooo......
        .....oooo.oooo#ooooo.....
        ....oooooooooo#oooooo....
        ...ooo#########ooooooo...
        ..ooooo.......ooooooooo..
        #########################
        '''
        self.assertEqual(Part2(SAMPLE_INPUT, True)[0], 93)

    def test_outcrops_past_triangle_edge(self):
        '''
             4  5    5
             9  0    0
             7  0    5
        0  .....o.....
        1  ....ooo....
        2  ..###ooo...
        3  ....ooo####
        4  ...ooooo..#
        5  ..ooooooo..
        6  ########### floor
        '''
        lines = [
            '497,2 -> 499,2',
            '502,3 -> 505,3 -> 505,4'
        ]
        self.assertEqual(Part2(lines, True)[0], 22)

    def test_bottle(self):
        '''
           4         5        5
           9         0        0
           0         0        9
        0  ..........o.........
        1  .........ooo........
        2  ........#oo#o.......
        3  .......##oo##o......
        4  .......#oooo#oo.....
        5  .......#oooo#ooo....
        6  .......######oooo...
        7  ............oooooo..
        9  ####################
        '''
        lines = [
            '501,2 -> 501,3 -> 502,3 -> 502,6 -> 497,6 -> 497,3 -> 498,3 -> 498,2'
        ]
        self.assertEqual(Part2(lines, True)[0], 33)

if __name__ == '__main__':
    with open('day14_input.txt') as f:
        textlines = re.split('\r?\n', f.read())
    part1_answer = Part1(textlines)
    print(f'part 1 answer = {part1_answer}')
    part2_answer, part2_grid, xmin = Part2(textlines, True)
    with open('part2_output.txt', 'w') as f:
        f.write(render_grid(part2_grid, xmin + 2, False))
    print(f'part 2 answer = {part2_answer}')
    unittest.main()