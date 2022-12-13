from collections import deque
import re
import unittest
import colorama
from colorama import Fore

colorama.init()

LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'

def parse_lines(lines: list[str]):
    grid = []
    for ii, line in enumerate(lines):
        if not line:
            break
        row = []
        for jj, char in enumerate(line):
            if char == 'S':
                start = (ii, jj)
                row.append(0)
            elif char == 'E':
                end = (ii, jj)
                row.append(27)
            else:
                row.append(ord(char) - 96) # a:1, ..., z:26
        grid.append(row)
    return grid, start, end, len(grid) - 1, len(grid[0]) - 1
            

def manhattan_distance(loc, end):
    return abs(end[0] - loc[0]) + abs(end[1] - loc[1])


def render_path(grid: list[list[int]], backtrace: tuple[tuple[int]]) -> str:
    text = ''
    lenback = len(backtrace)
    setback = set(backtrace)
    colors = [Fore.RED, Fore.LIGHTMAGENTA_EX, Fore.BLUE, Fore.CYAN, Fore.GREEN]
    for ii in range(len(grid)):
        row = ''
        for jj in range(len(grid[0])):
            val = grid[ii][jj]
            if val == 0:
                elt = 'S'
            elif val == 27:
                elt = 'E'
            else:
                elt = LOWERCASE[val - 1]
            if (ii, jj) in setback:
                idx = backtrace.index((ii, jj))
                color = colors[int(idx * 5 / lenback)]
                row += color + elt + Fore.RESET
            else:
                row += elt
        text += row + '\n'
    return text


def Part1(lines: list[str], show_path = True, verbose=False) -> int:
    '''shortest path from the designated starting point to the end'''
    grid, start, end, imax, jmax = parse_lines(lines)
    if verbose:
        for row in grid:
            print(row)
    next_locs = deque([((), start)])
    visited = set()
    enqueued = {start}
    while True:
        backtrace, loc = next_locs.popleft()
        visited.add(loc)
        enqueued.remove(loc)
        if loc == end:
            break
        ii, jj = loc
        val = grid[ii][jj]
        if verbose:
            print((f'{ii = }, {jj = }, {val = }, dist = {manhattan_distance(loc, end)}, '
                  f'{len(visited) = } {len(next_locs) = }, {len(backtrace) = }'))
        for next_ii, next_jj in {(ii - 1, jj), (ii + 1, jj), 
                                 (ii, jj - 1), (ii, jj + 1)}:
            next_loc = (next_ii, next_jj)
            if (0 <= next_ii <= imax) and (0 <= next_jj <= jmax) \
            and grid[next_ii][next_jj] <= val + 1 \
            and next_loc not in visited \
            and next_loc not in enqueued:
                next_locs.append((backtrace + (loc,), next_loc))
                enqueued.add(next_loc)
    if show_path or verbose:
        print(render_path(grid, backtrace + (end,)))
    return len(backtrace)

def Part2(lines: list[str], show_path = True, verbose = False) -> int:
    '''shortest path from end to the lowest elevation'''
    grid, _, start, imax, jmax = parse_lines(lines)
    # we basically start at what was the end in part 1,
    # and change some traversal rules
    next_locs = deque([((), start)])
    visited = set()
    enqueued = {start}
    while True:
        backtrace, loc = next_locs.popleft()
        visited.add(loc)
        enqueued.remove(loc)
        ii, jj = loc
        val = grid[ii][jj]
        if val == 1:
            break
        if verbose:
            print((f'{ii = }, {jj = }, {val = }, dist = {manhattan_distance(loc, start)}, '
                  f'{len(visited) = } {len(next_locs) = }, {len(backtrace) = }'))
        for next_ii, next_jj in {(ii - 1, jj), (ii + 1, jj), 
                                 (ii, jj - 1), (ii, jj + 1)}:
            next_loc = (next_ii, next_jj)
            if (0 <= next_ii <= imax) and (0 <= next_jj <= jmax) \
            and grid[next_ii][next_jj] >= val - 1 \
            and next_loc not in visited \
            and next_loc not in enqueued:
                next_locs.append((backtrace + (loc,), next_loc))
                enqueued.add(next_loc)
    if show_path or verbose:
        print(render_path(grid, backtrace + (loc,)))
    return len(backtrace)


SAMPLE_INPUT = [
    "Sabqponm",
    "abcryxxl",
    "accszExk",
    "acctuvwj",
    "abdefghi",
    "",
]

WINDING_PATH = [
    'SabzE',
    'aaaaz',
    'bcdey',
    'ihgfx',
    'iiiix',
    'imiiw', # add plateau to test if detours ignored
    'iiiiw',
    'jklmw',
    'ponmv',
    'qrstu',
]

WRAPAROUND = [
    'bcdddbcdefghijkl',
    'aaaSmmccmmmmponm',
    'dddabzzzzznoqrst',
    'ddccczEzxzyxwvuu',
]

BIG_OPEN = [
    'Saaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    'aaaEzyxwvutsrqponmlkjihgfedcbaaaaaaaaaaaaaa',
    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
]


class Part1Tests(unittest.TestCase):
    def test_sample_input(self):
        self.assertEqual(Part1(SAMPLE_INPUT), 31)

    def test_winding_path(self):
        self.assertEqual(Part1(WINDING_PATH), 34)

    def test_wrap_around(self):
        self.assertEqual(Part1(WRAPAROUND), 39)

    def test_big_open(self):
        self.assertEqual(Part1(BIG_OPEN), 57)


class TestPart2(unittest.TestCase):
    def test_sample_input(self):
        self.assertEqual(Part2(SAMPLE_INPUT), 29)

    def test_winding_path(self):
        self.assertEqual(Part2(WINDING_PATH), 33)

    def test_wraparound(self):
        self.assertEqual(Part2(WRAPAROUND), 36)
    
    def test_big_open(self):
        self.assertEqual(Part2(BIG_OPEN), 26)


if __name__ == '__main__':
    with open('day12_input.txt') as f:
        lines = re.split('\r?\n', f.read())
    part1_answer = Part1(lines)
    print(f'part 1 answer = {part1_answer}')
    part2_answer = Part2(lines)
    print(f'part 2 answer = {part2_answer}')
    unittest.main()