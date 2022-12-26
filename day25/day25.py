import re
import unittest

def snafu_int(snafu: str) -> int:
    '''SNAFU is base 5, but rotated by 2, so that the multipliers
    in a given fives place are as follows:
    = : -2
    - : -1
    0 : 0
    1 : 1
    2 : 2'''
    tot = 0
    for ii, char in enumerate(reversed(snafu)):
        mult = '=-012'.index(char) - 2
        tot += 5 ** ii * mult
    return tot

def int_snafu(num: int) -> str:
    '''convert an integer to SNAFU (described above)
    '''
    out = ''
    carry = 0
    while num > 0:
        num, mod = divmod(num, 5)
        carry, mod = divmod(mod + carry, 3)
        if carry:
            out += '=-0'[mod]
        else:
            out += str(mod)
    if carry:
        out += '1'
    return out[::-1]


def int_parse(num: int, base: int = 10) -> str:
    '''convert int to str to make sure I understand'''
    out = ''
    while num > 0:
        num, mod = divmod(num, base)
        out += str(mod)
    return out[::-1]


def Part1(lines: list[str]) -> str:
    result = sum(snafu_int(line) for line in lines if line)
    return int_snafu(result)
    


def Part2(lines: list[str]) -> int:
    return 0


SAMPLE_INPUT = [
    "1=-0-2",
    "12111",
    "2=0=",
    "21",
    "2=01",
    "111",
    "20012",
    "112",
    "1=-1=",
    "1-12",
    "12",
    "1=",
    "122",
]

SNAFU_INT_EXAMPLES = [
        (1, "1"),
        (2, "2"),
        (3, "1="),
        (4, "1-"),
        (5, "10"),
        (6, "11"),
        (7, "12"),
        (8, "2="),
        (9, "2-"),
        (10, "20"),
        (15, "1=0"),
        (19, "1--"),
        (20, "1-0"),
        (32, "112"),
        (33, "12="),
        (34, "12-"),
        (35, "120"),
        (38, "2=="),
        (40, "2=0"),
        (43, "2-="),
        (51, "201"),
        (124, "100-"),
        (163, "12=="),
        (2022, "1=11-2"),
        (12345, "1-0---0"),
    (314159265, "1121-1110-1=0"),
]


class Part1Tests(unittest.TestCase):
    def test_snafu_int(self):
        for num, snafu in SNAFU_INT_EXAMPLES:
            with self.subTest(num=num, snafu=snafu):
                self.assertEqual(snafu_int(snafu), num)

    def testPart1_sample_input(self):
        self.assertEqual(Part1(SAMPLE_INPUT), '2=-1=0')

    def test_int_snafu(self):
        for num, snafu in SNAFU_INT_EXAMPLES:
            with self.subTest(num=num, snafu=snafu):
                self.assertEqual(int_snafu(num), snafu)


class TestPart2(unittest.TestCase):
    def testPart2_sample_input(self):
        self.assertEqual(Part2(SAMPLE_INPUT), 0)


if __name__ == '__main__':
    with open('day25_input.txt') as f:
        lines = re.split('\r?\n', f.read())
    part1_answer = Part1(lines) # 29698499442451 is the numeric value
    print(f'part 1 answer = {part1_answer}')
    part2_answer = Part2(lines)
    print(f'part 2 answer = {part2_answer}')
    unittest.main()