from collections import deque
import math
import random
import re
import operator
import unittest

def int_in_line(line):
    return int(re.findall('\d+', line)[0])


class Monkey:
    id_: int
    items: deque[int]
    strrep: str
    # monkeys: dict[int, Monkey]
    # operation: function(old: int) -> int
    # worryTest: function(worry: int) -> None

    def __init__(self, lines, monkeys):
        self.id_ = int_in_line(lines[0])
        self.monkeys = monkeys
        monkeys[self.id_] = self
        self.items = deque([int(x) for x in re.findall('\d+', lines[1])])
        op1, funcname, op2 = re.findall('(old|\d+)\s+([\*\+])\s+(old|\d+)', lines[2])[0]
        oper_func = operator.add if funcname == '+' else operator.mul
        if op1 == 'old' and op2 == 'old':
            self.operation = lambda x: oper_func(x, x)
        elif op1 == 'old':
            op2val = int(op2)
            self.operation = lambda x: oper_func(x, op2val)
        elif op2 == 'old':
            op1val = int(op1)
            self.operation = lambda x: oper_func(x, op1val)
        else:
            result = oper_func(int(op1), int(op2))
            self.operation = lambda x: result
        self.test_val = int_in_line(lines[3])
        case1, monkey1 = re.findall('(true|false).+(\d+)', lines[4])[0]
        _, monkey2 = re.findall('(true|false).+(\d+)', lines[5])[0]
        self.monkey1_id = int(monkey1)
        self.monkey2_id = int(monkey2)
        if case1 != 'true':
            self.monkey1_id, self.monkey2_id = self.monkey2_id, self.monkey1_id
        self.strrep = f'Monkey(id_ = {self.id_}, items = {self.items}, operation = (old) => {op1} {funcname} {op2}, test = (worry) => worry % {self.test_val} == 0 ? passItem({self.monkey1_id}) : passItem({self.monkey2_id})'

    def passItem(self, other_monkey_id: int) -> None:
        to_throw = self.items.popleft()
        self.monkeys[other_monkey_id].items.append(to_throw)

    def inspectItemsPart1(self):
        while len(self.items) > 0:
            # first the monkey's worry operation is applied to the worry level
            # of the item.
            # Then your worry is divided by three when the monkey doesn't break it
            self.items[0] = self.operation(self.items[0]) // 3
            if self.items[0] % self.test_val == 0:
                self.passItem(self.monkey1_id)
            else:
                self.passItem(self.monkey2_id)

    def inspectItemsPart2(self, lcm_all_monkeys):
        # worry levels are not divided by 3 anymore!
        while len(self.items) > 0:
            self.items[0] = self.operation(self.items[0]) % lcm_all_monkeys
            if self.items[0] % self.test_val == 0:
                self.passItem(self.monkey1_id)
            else:
                self.passItem(self.monkey2_id)


    def __str__(self):
        return self.strrep

    __repr__ = __str__


def parse_input(lines: list[str]) -> dict[int, Monkey]:
    monkey_lines = []
    monkeys = {}
    for line in lines:
        if not line:
            _ = Monkey(monkey_lines, monkeys)
            monkey_lines = []
        else:
            monkey_lines.append(line)
    return monkeys

def Part1(lines: list[str]):
    monkeys = parse_input(lines)
    # pprint.pprint(monkeys)
    activities = {ii: 0 for ii in monkeys.keys()}
    for round in range(20):
        for ii, monkey in monkeys.items():
            # print({ii: list(monkey.items) for ii, monkey in monkeys.items()})
            activities[ii] += len(monkey.items)
            monkey.inspectItemsPart1()
        # print(f'At end of round {round}, activities = {activites}')
    # print({ii: list(monkey.items) for ii, monkey in monkeys.items()})
    # print(f'Final activities: {activites}')
    second_activity, max_activity = sorted(activities.values())[-2:]
    return second_activity * max_activity

def gcd(a, b):
    if b > a:
        a, b = b, a
    while b > 0:
        # print(f'{a = }, {b = }')
        a, b = b, a % b
    return a

def lcm_pair(a: int, b: int) -> int:
    if b > a:
        a, b = b, a
    return a * (b // gcd(a, b))

def least_common_multiple(ints: list[int]) -> int:
    if not ints:
        raise ValueError("Can't get LCM of zero-length iterable")
    if len(ints) == 1:
        return ints[0]
    sorted_ints = sorted(ints)
    lcm = lcm_pair(sorted_ints[1], sorted_ints[0])
    idx = 2
    while idx < len(sorted_ints):
        lcm = lcm_pair(lcm, sorted_ints[idx])
        idx += 1
    return lcm

def Part2(lines: list[str], verbose=False) -> int:
    monkeys = parse_input(lines)
    if verbose:
        for m in monkeys.values():
            print(m)
    activities = {ii: 0 for ii in monkeys.keys()}
    test_vals = [m.test_val for m in monkeys.values()]
    lcm_all_monkeys = least_common_multiple(test_vals)
    if verbose:
        print(f'{test_vals = }, {lcm_all_monkeys = }')
    for round in range(10_000):
        if verbose and round % 500 == 0:
            print(f'=============\nRound {round}')
            for ii, m in monkeys.items():
                print(f'Monkey {ii} items: {m.items}')
            print(f'Activities: {activities}')
        for ii, monkey in monkeys.items():
            activities[ii] += len(monkey.items)
            monkey.inspectItemsPart2(lcm_all_monkeys)
    second_activity, max_activity = sorted(activities.values())[-2:]
    return second_activity * max_activity


SAMPLE_INPUT = [
    "Monkey 0:",
    "  Starting items: 79, 98",
    "  Operation: new = old * 19",
    "  Test: divisible by 23",
    "    If true: throw to monkey 2",
    "    If false: throw to monkey 3",
    "",
    "Monkey 1:",
    "  Starting items: 54, 65, 75, 74",
    "  Operation: new = old + 6",
    "  Test: divisible by 19",
    "    If true: throw to monkey 2",
    "    If false: throw to monkey 0",
    "",
    "Monkey 2:",
    "  Starting items: 79, 60, 97",
    "  Operation: new = old * old",
    "  Test: divisible by 13",
    "    If true: throw to monkey 1",
    "    If false: throw to monkey 3",
    "",
    "Monkey 3:",
    "  Starting items: 74",
    "  Operation: new = old + 3",
    "  Test: divisible by 17",
    "    If true: throw to monkey 0",
    "    If false: throw to monkey 1",
    "",
]


class LCMTests(unittest.TestCase):
    def test_random_examples(self):
        for ii in range(1000):
            nums = random.choices(range(1_000), k=random.randint(1, 12))
            with self.subTest(nums=nums):
                self.assertEqual(math.lcm(*nums), least_common_multiple(nums))


class Part1Tests(unittest.TestCase):
    def testPart1_sample_input(self):
        self.assertEqual(Part1(SAMPLE_INPUT), 10605)


class TestPart2(unittest.TestCase):
    def testPart2_sample_input(self):
        self.assertEqual(Part2(SAMPLE_INPUT), 2713310158)


if __name__ == '__main__':
    with open('day11_input.txt') as f:
        lines = re.split('\r?\n', f.read())
    part1_answer = Part1(lines)
    print(f'part 1 answer = {part1_answer}')
    part2_answer = Part2(lines)
    print(f'part 2 answer = {part2_answer}')
    unittest.main()