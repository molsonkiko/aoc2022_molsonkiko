import re
import unittest

def Part1(lines: list[str], verbose=False):
    nums = [int(line) for line in lines if line]
    if verbose:
        print(f'BEGIN:\n{nums}')
    numcopy = nums[:]
    for ii, shift in enumerate(numcopy):
        swap_with = (ii + shift) % len(nums)
        nums[swap_with], nums[ii] = nums[ii], nums[swap_with]
        if verbose:
            print((f'swap nums[{ii}] = {nums[ii]} with '
                   f'nums[{swap_with}] = {nums[swap_with]}'))
            print(nums)
    zero_pos = nums.index(0)
    tot = 0
    for ii in [1000, 2000, 3000]:
        tot += nums[(zero_pos + ii) % len(nums)]
    return tot

def Part2(lines: list[str]) -> int:
    return 0


SAMPLE_INPUT = [
    "1",
    "2",
    "-3",
    "3",
    "-2",
    "0",
    "4",
]


class Part1Tests(unittest.TestCase):
    def testPart1_sample_input(self):
        self.assertEqual(Part1(SAMPLE_INPUT, True), 3)

    def test_one_to_five(self):
        '''
0 1 2 3 4 -> shift 0 forward 0
0 1 2 3 4 -> shift 1 forward 1
0 2 1 3 4 -> shift 1 forward 2
0 2 4 3 1 -> shift 3 forward 3 (wrap around to index 1)
0 3 4 2 1 -> shift 1 forward 4 (wrap back to index 3)
0 3 4 1 2
0 is at index 0
0 is also at indices 1000, 2000, and 3000 (modulo 5)
so the answer is 0
        '''
        inp = list(map(str, range(5)))
        self.assertEqual(Part1(inp, True), 0)


class TestPart2(unittest.TestCase):
    def testPart2_sample_input(self):
        self.assertEqual(Part2(SAMPLE_INPUT), 0)


if __name__ == '__main__':
    with open('day20_input.txt') as f:
        lines = re.split('\r?\n', f.read())
    part1_answer = Part1(lines)
    print(f'part 1 answer = {part1_answer}')
    part2_answer = Part2(lines)
    print(f'part 2 answer = {part2_answer}')
    unittest.main()