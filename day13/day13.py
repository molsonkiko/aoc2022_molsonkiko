import json
import re
import unittest

intarr = list[int | list[int]]
intarr = list[int | intarr]
intarr = list[int | intarr]

def parse_list(list_str: str) -> intarr:
    '''simple parser for the subset of JSON that includes only
    arrays and integers'''
    depth = 0
    out = []
    parents = [None]
    cur_list = out
    ii = 0
    while ii < len(list_str):
        char = list_str[ii]
        # print(f'{char = }, {cur_list = }')
        if char == '[':
            if depth > 0:
                cur_list.append([])
                parents.append(cur_list)
                cur_list = cur_list[-1]
            depth += 1
        elif char == ']':
            depth -= 1
            cur_list = parents.pop()
            if depth == 0:
                break
        elif '0' <= char <= '9':
            numstr = ''
            while ii < len(list_str) and '0' <= list_str[ii] <= '9':
                numstr += list_str[ii]
                ii += 1
            ii -= 1
            cur_list.append(int(numstr))
        ii += 1
    return out

def right_gt_left(left, right, verbose=False) -> int:
    '''return 1 if right > left, -1 if left < right, 0 if equal'''
    ii = 0
    if verbose:
        print('==============')
        print(f'{left = }')
        print(f'{right = }')
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]
    while ii < len(left) and ii < len(right):
        v1, v2 = left[ii], right[ii]
        ii += 1
        v1_int = isinstance(v1, int) or len(v1) != 1
        v2_int = isinstance(v2, int) or len(v2) != 1
        v1_depth, v2_depth = 0, 0
        while not (v1_int and v2_int):
            if not v1_int:
                v1 = v1[0]
                v1_depth += 1
            if not v2_int:
                v2 = v2[0]
                v2_depth += 1
            v1_int = isinstance(v1, int) or len(v1) != 1
            v2_int = isinstance(v2, int) or len(v2) != 1
        if isinstance(v1, list):
            if isinstance(v2, list):
                # nested empty lists are compared by nesting depth
                if len(v1) == 0 and len(v2) == 0:
                    if v1_depth > v2_depth:
                        if verbose:
                            print(f'{left[ii -1 ] = }, {right[ii - 1] = }, left wins b/c deeper')
                        return -1
                    if v1_depth < v2_depth:
                        if verbose:
                            print(f'{left[ii -1 ] = }, {right[ii - 1] = }, right wins b/c deeper')
                        return 1
                    if verbose:
                        print(f'{left[ii -1 ] = }, {right[ii - 1] = }, tie b/c equal depth')
                    return 0
                else:
                    result = right_gt_left(v1, v2, verbose)
                    if result != 0:
                        return result
            else:
                result = right_gt_left(v1, v2, verbose)
                if result != 0:
                    return result
        elif isinstance(v2, list):
            # empty list on right, number on left
            # number is greater, so this is bad
            result = right_gt_left(v1, v2, verbose)
            if result != 0:
                return result
        elif v1 > v2:
            if verbose:
                print(f'{left[ii - 1] = }, {right[ii - 1] = }, left wins because it is larger number')
            return -1 # right side should be greater
        elif v2 > v1:
            if verbose:
                print(f'{left[ii - 1] = }, {right[ii - 1] = }, right wins because it is larger number')
            return 1
    if ii == len(left) and ii < len(right):
        if verbose:
            print(f'{len(left) = }, {len(right) = }, right wins b/c longer')
        return 1 # if left is exhausted, that's good
    elif ii == len(right) and ii < len(left):
        if verbose:
            print(f'{len(left) = }, {len(right) = }, left wins b/c longer')
        return -1 # if right is exhausted, that's bad
    # both are elementwise equal
    if verbose:
        print(f'{len(left) = }, {len(right) = }, both same')
    return 0


def Part1(lines: list[str], verbose=False):
    pair = []
    correctly_ordered_pairs = 0
    pair_number = 0
    for ii, line in enumerate(lines):
        if not line:
            pair_number += 1
            if verbose:
                print(f'Pair {pair_number}')
            if right_gt_left(*pair, verbose) == 1:
                correctly_ordered_pairs += pair_number
            pair = []
            continue
        pair.append(parse_list(line))
    return correctly_ordered_pairs
    

def Part2(lines: list[str]) -> int:
    return 0


SAMPLE_INPUT = [
    "[1,1,3,1,1]",
    "[1,1,5,1,1]",
    "",
    "[[1],[2,3,4]]",
    "[[1],4]",
    "",
    "[9]",
    "[[8,7,6]]",
    "",
    "[[4,4],4,4]",
    "[[4,4],4,4,4]",
    "",
    "[7,7,7,7]",
    "[7,7,7]",
    "",
    "[]",
    "[3]",
    "",
    "[[[]]]",
    "[[]]",
    "",
    "[1,[2,[3,[4,[5,6,7]]]],8,9]",
    "[1,[2,[3,[4,[5,6,0]]]],8,9]",
    "",
]

class ParseListTests(unittest.TestCase):
    def test_on_sample_input(self):
        with open('day13_input.txt') as f:
            lines = re.split('\r?\n', f.read())
        # make sure my parser works correctly by comparing to
        # the builtin JSON module, which I know is right
        for line in lines:
            if line:
                with self.subTest(line = line):
                    self.assertEqual(json.loads(line), parse_list(line))


class Part1Tests(unittest.TestCase):
    def testPart1_sample_input(self):
        self.assertEqual(Part1(SAMPLE_INPUT, False), 13)


class TestPart2(unittest.TestCase):
    def testPart2_sample_input(self):
        self.assertEqual(Part2(SAMPLE_INPUT), 0)


if __name__ == '__main__':
    with open('day13_input.txt') as f:
        lines = re.split('\r?\n', f.read())
    part1_answer = Part1(lines) # 5969 is too low
    print(f'part 1 answer = {part1_answer}')
    part2_answer = Part2(lines)
    print(f'part 2 answer = {part2_answer}')
    unittest.main()