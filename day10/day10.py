import re
import unittest

def Part1(lines: list[str]):
    x = 1
    cycles = 0
    interesting_values = {20: 0, 60: 0, 100: 0, 140: 0, 180: 0, 220: 0}
    last_amount = 0
    for line in lines:
        if not line:
            continue
        parts = line.split()
        if cycles in interesting_values:
            interesting_values[cycles] = (x - last_amount) * cycles
        if len(parts) == 1: # noop
            cycles += 1
            last_amount = 0
            continue
        cycles += 2
        if cycles - 1 in interesting_values: # in the middle of the cycle
            interesting_values[cycles - 1] = x * (cycles - 1)
        last_amount = int(parts[1])
        x += last_amount
    if cycles in interesting_values:
        interesting_values[cycles] = (x - last_amount) * cycles
    return sum(interesting_values.values())


def draw_pixel(pixels, cycles, x):
    distance = x % 40 - cycles % 40
    if abs(distance) <= 1:
        # print('drawing #')
        pixels[cycles] = '#'

def Part2(lines: list[str]) -> int:
    pixels = ['.' for ii in range(240)]
    x = 1
    cycles = 0
    for line in lines:
        # print(f'line = {line}')
        if not line:
            continue
        # print((f'{line = }, {cycles % 40 = }, '
        #       f'sprite from {(x - 1) % 40}:{(x + 1) % 40}'))
        draw_pixel(pixels, cycles, x)
        parts = line.split()
        if len(parts) == 1: # noop
            cycles += 1
            continue
        cycles += 2
        draw_pixel(pixels, cycles - 1, x)
        x += int(parts[1])
    # break it into 6 40-char rows
    screen = '\n'.join(''.join(pixels[ii:ii+40]) for ii in range(0, 240, 40))
    return screen


with open('day10_sample_input.txt') as f:
    SAMPLE_INPUT = re.split('\r?\n', f.read())


class Part1Tests(unittest.TestCase):
    def testPart1_sample_input(self):
        self.assertEqual(Part1(SAMPLE_INPUT), 13140)


class TestPart2(unittest.TestCase):
    maxDiff = None

    def testPart2_sample_input(self):
        correct_output = (
            '##..##..##..##..##..##..##..##..##..##..\n'
            '###...###...###...###...###...###...###.\n'
            '####....####....####....####....####....\n'
            '#####.....#####.....#####.....#####.....\n'
            '######......######......######......####\n'
            '#######.......#######.......#######.....')
        self.assertEqual(Part2(SAMPLE_INPUT), correct_output)


if __name__ == '__main__':
    with open('day10_input.txt') as f:
        lines = re.split('\r?\n', f.read())
    part1_answer = Part1(lines)
    print(f'part 1 answer = {part1_answer}')
    part2_answer = Part2(lines)
    print(f'part 2 answer =\n{part2_answer}')
    unittest.main()