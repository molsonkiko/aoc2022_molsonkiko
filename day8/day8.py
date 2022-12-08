import re
import unittest

def make_grid(lines: list[str]) -> list[list[int]]:
    grid = []
    for line in lines:
        if line:
            grid.append([int(x) for x in line])
    return grid

def Part1(lines: list[str]):
    grid = make_grid(lines)
    h = len(grid)
    w = len(grid[0])
    # print('\n'.join(lines))
    visible_from_outside = h * 2 + w * 2 - 4 # all on outside of grid
    for ii in range(1, h - 1):
        for jj in range(1, w - 1):
            v = grid[ii][jj]
            visible = 4
            for ii2 in range(ii - 1, -1, -1):
                if grid[ii2][jj] >= v:
                    visible -= 1
                    break
            for ii2 in range(ii + 1, h):
                if grid[ii2][jj] >= v:
                    visible -= 1
                    break
            for jj2 in range(jj - 1, -1, -1):
                if grid[ii][jj2] >= v:
                    visible -= 1
                    break
            for jj2 in range(jj + 1, w):
                if grid[ii][jj2] >= v:
                    visible -= 1
                    break
            if visible > 0:
                # print(f'grid[{ii}][{jj}] is visible from outside')
                visible_from_outside += 1
    return visible_from_outside


def Part2(lines: list[str]) -> int:
    grid = make_grid(lines)
    h = len(grid)
    w = len(grid[0])
    # print('\n'.join(lines))
    max_scenic_score = 0
    for ii in range(1, h - 1):
        for jj in range(1, w - 1):
            v = grid[ii][jj]
            scenic_score_parts = [0, 0, 0, 0]
            for ii2 in range(ii - 1, -1, -1):
                scenic_score_parts[0] += 1
                if grid[ii2][jj] >= v:
                    break
            for ii2 in range(ii + 1, h):
                scenic_score_parts[1] += 1
                if grid[ii2][jj] >= v:
                    break
            for jj2 in range(jj - 1, -1, -1):
                scenic_score_parts[2] += 1
                if grid[ii][jj2] >= v:
                    break
            for jj2 in range(jj + 1, w):
                scenic_score_parts[3] += 1
                if grid[ii][jj2] >= v:
                    break
            scenic_score = (scenic_score_parts[0] * scenic_score_parts[1]
                * scenic_score_parts[2] * scenic_score_parts[3])
            if scenic_score > max_scenic_score:
                # print(f'grid[{ii}][{jj}] has the best scenic score of {scenic_score} ({scenic_score_parts})')
                max_scenic_score = scenic_score
    return max_scenic_score


SAMPLE_INPUT = [
    "30373",
    "25512",
    "65332",
    "33549",
    "35390",
]


class Part1Tests(unittest.TestCase):
    def testPart1_sample_input(self):
        self.assertEqual(Part1(SAMPLE_INPUT), 21)


class TestPart2(unittest.TestCase):
    def testPart2_sample_input(self):
        self.assertEqual(Part2(SAMPLE_INPUT), 8)


if __name__ == '__main__':
    with open('day8_input.txt') as f:
        lines = re.split('\r?\n', f.read())
    part1_answer = Part1(lines)
    print(f'part 1 answer = {part1_answer}')
    part2_answer = Part2(lines)
    print(f'part 2 answer = {part2_answer}')
    unittest.main()