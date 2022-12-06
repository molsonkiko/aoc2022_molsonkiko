import re

def Part1(lines, debug=False):
    stacks_dict = {}
    adding_crates = True
    for line in lines:
        if adding_crates:
            for ii, c in enumerate(line):
                if '1' <= c <= '9' and line[0] == ' ':
                    adding_crates = False
                    # reverse the stacks and order them by their order in the file
                    stacks = [x[1] for x in sorted(stacks_dict.items(), key = lambda x: x[0])]
                    for ii in range(len(stacks)):
                        stacks[ii] = stacks[ii][::-1]
                    if debug:
                        print(f'stacks are initially\n{["".join(x) for x in stacks]}')
                    break
                div, mod = divmod(ii, 4)
                if mod == 1:
                    if div == len(stacks_dict):
                        stacks_dict[div] = []
                    if 'A' <= c <= 'Z':
                        stacks_dict[div].append(c)
        elif line:
            count, from_, to_ = map(int, re.findall('\d+', line))
            for ii in range(count):
                stacks[to_ - 1].append(stacks[from_ - 1].pop())
            if debug:
                print(f'After moving {count} from {from_} to {to_}, stacks are:\n{["".join(x) for x in stacks]}')
    return ''.join(stack[-1] for stack in stacks)

def Part2(lines, debug=False):
    stacks_dict = {}
    adding_crates = True
    for line in lines:
        if adding_crates:
            for ii, c in enumerate(line):
                if '1' <= c <= '9' and line[0] == ' ':
                    adding_crates = False
                    # reverse the stacks and order them by their order in the file
                    stacks = [x[1] for x in sorted(stacks_dict.items(), key = lambda x: x[0])]
                    for ii in range(len(stacks)):
                        stacks[ii] = stacks[ii][::-1]
                    if debug:
                        print(f'stacks are initially\n{["".join(x) for x in stacks]}')
                    break
                div, mod = divmod(ii, 4)
                if mod == 1:
                    if div == len(stacks_dict):
                        stacks_dict[div] = []
                    if 'A' <= c <= 'Z':
                        stacks_dict[div].append(c)
        elif line:
            count, from_, to_ = map(int, re.findall('\d+', line))
            stacks[to_ - 1].extend(stacks[from_ - 1][-count:])
            for ii in range(count):
                stacks[from_ - 1].pop()
            if debug:
                print(f'After moving {count} from {from_} to {to_}, stacks are:\n{["".join(x) for x in stacks]}')
    return ''.join(stack[-1] for stack in stacks)

def test_part1():
    sample_inp = [
        "    [D]        ",
		"[N] [C]        ",
		"[Z] [M] [P] [Q]",
		" 1   2   3   4",
		"",
		"move 1 from 2 to 1",
		"move 3 from 1 to 3",
		"move 2 from 2 to 1",
		"move 1 from 1 to 2",
        "move 2 from 3 to 4",
        "move 1 from 4 to 1",
    ]
    part1_result = Part1(sample_inp, debug=True)
    expected = 'NMDZ'
    if part1_result != expected:
        print(f'part 1 test failed, expected {expected}, got {part1_result}')

def test_part2():
    sample_inp = [
        "    [D]        ",
		"[N] [C]        ",
		"[Z] [M] [P] [Q]",
		" 1   2   3   4",
		"",
		"move 1 from 2 to 1",
		"move 3 from 1 to 3",
		"move 2 from 2 to 1",
		"move 1 from 1 to 2",
        "move 2 from 3 to 4",
        "move 1 from 4 to 1",
    ]
    part1_result = Part2(sample_inp, debug=True)
    expected = 'DCZN'
    if part1_result != expected:
        print(f'part 1 test failed, expected {expected}, got {part1_result}')

if __name__ == '__main__':
    with open('day5_input.txt') as f:
        inp = f.read().split('\n')
    test_part1()
    test_part2()
    part1_answer = Part1(inp)
    print(f'part 1 answer = {part1_answer}')
    part2_answer = Part2(inp)
    print(f'part 2 answer = {part2_answer}')