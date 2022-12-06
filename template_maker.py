import os
from pathlib import Path

ROOT = Path(__file__).parent

def make_template_dir(day):
    daydir = ROOT / f'day{day}'
    os.mkdir(daydir)
    with open(daydir / f'day{day}_input.txt', 'w') as f:
        f.write('')
    
    with open(daydir / 'main.go', 'w') as f:
        f.write(f'''package main

import (
	"fmt"
	"os"
	"strings"

	"aoc2022/day{day}/day{day}"
)

func main() {{
	bytes, err := os.ReadFile("day{day}_input.txt")
	if err != nil {{
		panic(err)
	}}
	lines := strings.Split(string(bytes), "\\n")
	part1_answer, err := day{day}.Part1(lines)
	if err != nil {{
		panic(err)
	}}
	fmt.Printf("Part 1 result: %d\\n", part1_answer)
	part2_answer, err := day{day}.Part2(lines)
	if err != nil {{
		panic(err)
	}}
	fmt.Printf("Part 2 result: %d\\n", part2_answer)
}}''')

    daydaydir = daydir / f'day{day}'
    os.mkdir(daydaydir)

    with open(daydaydir / f'day{day}.go', 'w') as f:
        f.write(f'''package day{day}

func Part1(lines []string) (result int, err error) {{
	return 0, nil
}}

func Part2(lines []string) (result int, err error) {{
	return 0, nil
}}''')

    with open(daydaydir / f'day{day}_test.go', 'w') as f:
        f.write(f'''package day{day}

import (
	"testing"
)

func testValueExpected(t *testing.T, result int, err error, expected_result int) {{
	if err != nil {{
		t.Errorf("Got error %s, expected result %d", err, expected_result)
	}}
	if result != expected_result {{
		t.Errorf("Got result %d, expected result %d", result, expected_result)
	}}
}}

type InputAnswer struct {{
	input []string;
	answer int;
}};

func TestPart1_SampleInputs(t *testing.T) {{
	inputanswers := []InputAnswer{{
		{{[]string{{""}}, 0 }},
	}}
	for _, inputanswer := range inputanswers {{
		result, err := Part1(inputanswer.input)
		testValueExpected(t, result, err, inputanswer.answer)
	}}
}}

func TestPart2_SampleInput(t *testing.T) {{
	inputanswers := []InputAnswer{{
		{{[]string{{""}}, 0}},
	}}
	for _, inputanswer := range inputanswers {{
		result, err := Part2(inputanswer.input)
		testValueExpected(t, result, err, inputanswer.answer)
	}}
}}
''')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int, help='the day number')
    args = parser.parse_args()
    make_template_dir(args.day)