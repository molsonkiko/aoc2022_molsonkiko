from collections import deque
import heapq
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


def render_path(grid: list[list[int]], backtrace: tuple[tuple[int]], visited: set[tuple[int]]) -> str:
    text = '\n'
    lenback = len(backtrace)
    setback = set(backtrace)
    colors = [Fore.RED, Fore.LIGHTMAGENTA_EX, Fore.BLUE, Fore.CYAN, Fore.GREEN]
    cur_color = ''
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
                if cur_color != color:
                    cur_color = color
                    row += Fore.RESET + color
            elif (ii, jj) in visited:
                if cur_color != Fore.LIGHTYELLOW_EX:
                    cur_color = Fore.LIGHTYELLOW_EX
                    row += Fore.RESET + Fore.LIGHTYELLOW_EX
            else:
                if cur_color != '':
                    cur_color = ''
                    row += Fore.RESET
            row += elt
        text += row + Fore.RESET + '\n'
        cur_color = ''
    return text


def Part1(lines: list[str], show_path = True, verbose=False) -> int:
    '''shortest path from the designated starting point to the end'''
    grid, start, end, imax, jmax = parse_lines(lines)
    if verbose:
        for row in grid:
            print(row)
    # in the A* algorithm, the distance to start is also known as
    # the g-score
    distances_to_start = {start: 0}
    # in the A* algorithm, the estimated distance from a node to the end
    # plus the distance to start is also known as the f-score
    def cost_func(loc):
        '''penalize distance from end, reward climbing higher'''
        return manhattan_distance(loc, end) - grid[loc[0]][loc[1]]
    next_locs = [(cost_func(start), start)]
    came_from = {} # allows a backtrace to the start
    enqueued = {start}
    visited = {start: 1} # not required for algorithm, but useful for visualization
    while next_locs:
        f_score, loc = heapq.heappop(next_locs)
        if loc == end:
            break
        enqueued.remove(loc)
        visited.setdefault(loc, 0)
        visited[loc] += 1
        dist_to_start = distances_to_start[loc]
        ii, jj = loc
        val = grid[ii][jj]
        if verbose:
            print((f'{ii = }, {jj = }, {val = }, '
                   f'{dist_to_start = }, {f_score = }, {len(next_locs) = }'))
        for next_ii, next_jj in {(ii - 1, jj), (ii + 1, jj), 
                                 (ii, jj - 1), (ii, jj + 1)}:
            next_loc = (next_ii, next_jj)
            if (0 <= next_ii <= imax) and (0 <= next_jj <= jmax) \
            and grid[next_ii][next_jj] <= val + 1:
                # gscore of current + d(current, neighbor)
                tentative_start_dist = dist_to_start + 1
                old_start_dist = distances_to_start.get(next_loc)
                # update distance to start and f score of next_loc if the newly found
                # distance is less than the previous estimate
                if (not old_start_dist) or tentative_start_dist < old_start_dist:
                    distances_to_start[next_loc] = tentative_start_dist
                    came_from[next_loc] = loc
                    f_score_next = tentative_start_dist + cost_func(next_loc)
                    if next_loc not in enqueued:
                        enqueued.add(next_loc)
                        heapq.heappush(next_locs, (f_score_next, next_loc))
    prev = end
    backtrace = [end]
    while prev != start:
        prev = came_from[prev]
        backtrace.append(prev)
    if show_path or verbose:
        print(render_path(grid, backtrace[::-1], visited))
        print(f'locations visited: {sum(visited.values())}')
    return len(backtrace) - 1

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
        print(render_path(grid, backtrace + (loc,), visited))
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
    part1_answer = Part1(lines, True, False)
    print(f'part 1 answer = {part1_answer}')
    part2_answer = Part2(lines)
    print(f'part 2 answer = {part2_answer}')
    unittest.main()