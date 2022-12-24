import json
import random
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

def compare_lists(left, right, verbose=False) -> int:
    '''return 1 if left > right, -1 if left < right, 0 if equal'''
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
        if isinstance(v1, list) or isinstance(v2, list):
            result = compare_lists(v1, v2, verbose)
            if result != 0:
                return result
        elif v1 > v2:
            if verbose:
                print(f'{left[ii - 1] = }, {right[ii - 1] = }, left wins because it is larger number')
            return 1 # left side has greater numeric value
        elif v2 > v1:
            if verbose:
                print(f'{left[ii - 1] = }, {right[ii - 1] = }, right wins because it is larger number')
            return -1
    if ii == len(left) and ii < len(right):
        if verbose:
            print(f'{len(left) = }, {len(right) = }, right wins b/c longer')
        return -1 # if left is exhausted, right wins
    elif ii == len(right) and ii < len(left):
        if verbose:
            print(f'{len(left) = }, {len(right) = }, left wins b/c longer')
        return 1 # if right is exhausted, left wins
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
            if compare_lists(*pair, verbose) == -1:
                correctly_ordered_pairs += pair_number
            pair = []
            continue
        pair.append(parse_list(line))
    return correctly_ordered_pairs


def insertion_sort(l: list, start: int, end: int, comparator) -> None:
    for ii in range(start, end):
        for jj in range(ii - 1, start - 1, -1):
            if comparator(l[jj], l[jj + 1]) <= 0:
                break
            l[jj], l[jj + 1] = l[jj + 1], l[jj]


def merge(l: list, start: int, mid: int, end: int, comparator) -> None:
    # print(f'merging {l[start:mid] = } and {l[mid:end] = }')
    aux = l[start:mid]
    left = 0
    right = mid
    overall = start
    while left < mid - start and right < end:
        comp = comparator(aux[left], l[right])
        if comp <= 0:
            l[overall] = aux[left]
            left += 1
        else:
            # the element on the right is less
            l[overall] = l[right]
            right += 1
        overall += 1
    while left < mid - start:
        l[overall] = aux[left]
        left += 1
        overall += 1
    # print(f'after merge, {l[start:end] = }')
    # otherwise don't need to do anything, because everything
    # right of the right pointer is already in place


def merge_sort(l: list, start: int = 0, end: int = -1, comparator = None):
    if comparator is None:
        comparator = default_comparator
    if end < 0:
        end = len(l)
    if end - start <= 16:
        insertion_sort(l, start, end, comparator)
        return
    # print(f'merge sorting {l[start:end] = }')
    mid = (start + end) // 2
    merge_sort(l, start, mid, comparator)
    merge_sort(l, mid, end, comparator)
    merge(l, start, mid, end, comparator)


def default_comparator(left, right):
    if left < right:
        return -1
    if left == right:
        return 0
    return 1


def is_sorted(l: list, comparator=None):
    if comparator is None:
        comparator=default_comparator
    for ii in range(len(l) - 1):
        if comparator(l[ii], l[ii + 1]) > 0:
            return False
    return True


def Part2(lines: list[str]) -> int:
    lists = [parse_list(line) for line in lines if line]
    divider_packet1 = [[2]]
    divider_packet2 = [[6]]
    lists += [divider_packet1, divider_packet2]
    merge_sort(lists, comparator=compare_lists)
    pack1_idx = lists.index(divider_packet1) + 1
    pack2_idx = lists.index(divider_packet2) + 1
    return pack1_idx * pack2_idx


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


class MergeSortTests(unittest.TestCase):
    def test_is_sorted_ints(self):
        self.assertTrue(is_sorted([1,2,3,4,5]))
        self.assertFalse(is_sorted([1, 5, 3]))

    def test_is_sorted_ints_nonstandard_comparator(self):
        comp = lambda x, y: default_comparator(len(x), len(y))
        self.assertFalse(is_sorted(['a', 'bb', 'ccc', 'dd'], comp))
        self.assertTrue(is_sorted(['a', 'bb', 'cc', 'ddd'], comp))

    def test_merge_left_longer_than_right_default_comp(self):
        l1 = [1,2,4,6,9,11]
        l2=[3,5, 7, 8, 10]
        l1p2 = l1 + l2
        merge(l1p2, 0, 6, 11, default_comparator)
        self.assertEqual(l1p2, list(range(1, 12)))

    def test_merge_right_longer_than_left_default_comp(self):
        l1 = [1,2,4,6]
        l2=[3,5, 7, 8, 9]
        l1p2 = l1 + l2
        merge(l1p2, 0, 4, 9, default_comparator)
        self.assertEqual(l1p2, list(range(1, 10)))

    def test_merge_right_empty(self):
        l = [1]
        merge(l, 0, 1, 1, default_comparator)
        self.assertEqual(l, [1])

    def test_merge_left_empty(self):
        l = [1]
        merge(l, 0, 0, 1, default_comparator)
        self.assertEqual(l, [1])

    def test_insertion_sort_default_comp(self):
        l = list(range(15))
        insertion_sort(l, 0, len(l), default_comparator)
        self.assertEqual(l, sorted(l))

    def test_insertion_sort_nonstandard_comp(self):
        comp = lambda x, y: default_comparator(len(x), len(y))
        words = ['augrnowu', 'foo', 'barr', 'baz', 'blah']
        sorted_by_comp = ['foo', 'baz', 'barr', 'blah', 'augrnowu']
        insertion_sort(words, 0, len(words), comp)
        self.assertEqual(words, sorted_by_comp)

    def test_insertion_sort_partial_array(self):
        l = [0, 2, 1, 3]
        insertion_sort(l, 1, 3, default_comparator)
        self.assertEqual(l, [0, 1, 2, 3])
    
    def test_insertion_sort_start_equals_end_minus_1(self):
        l = [0, 3, 2, 1]
        insertion_sort(l, 0, 1, default_comparator)
        self.assertEqual(l, [0, 3, 2, 1])
    
    def test_merge_sort_on_int_arrays_default_comp_even_length(self):
        nums = list(range(40))
        random.shuffle(nums)
        merge_sort(nums)
        self.assertEqual(nums, list(range(40)))

    def test_merge_sort_on_int_arrays_default_comp_odd_length(self):
        nums = list(range(35))
        random.shuffle(nums)
        merge_sort(nums)
        self.assertEqual(nums, list(range(35)))

    def test_merge_sort_comp_by_length_even_length_array(self):
        lowercase = 'abcdefghi'
        words = [lowercase[ii] * (1 + ii // 3) for ii in range(9)] \
            + [lowercase[ii].upper() * (1 + ii // 3) for ii in range(9)]
        comp = lambda x, y: default_comparator(len(x), len(y))
        merge_sort(words, comparator=comp)
        correct = sorted(words, key=len)
        self.assertEqual(words, correct)

    def test_merge_sort_comp_by_length_odd_length_array(self):
        lowercase = 'abcdefghij'
        words = [lowercase[ii] * (1 + ii // 3) for ii in range(10)] \
            + [lowercase[ii].upper() * (1 + ii // 3) for ii in range(9)]
        comp = lambda x, y: default_comparator(len(x), len(y))
        merge_sort(words, comparator=comp)
        correct = sorted(words, key=len)
        self.assertEqual(words, correct)
        


class Part1Tests(unittest.TestCase):
    def testPart1_sample_input(self):
        self.assertEqual(Part1(SAMPLE_INPUT), 13)


class TestPart2(unittest.TestCase):
    def testPart2_sample_input(self):
        self.assertEqual(Part2(SAMPLE_INPUT), 140)


if __name__ == '__main__':
    with open('day13_input.txt') as f:
        lines = re.split('\r?\n', f.read())
    part1_answer = Part1(lines) # 6101
    print(f'part 1 answer = {part1_answer}')
    part2_answer = Part2(lines)
    print(f'part 2 answer = {part2_answer}')
    unittest.main()