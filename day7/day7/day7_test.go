package day7

import (
	"testing"
)

func testValueExpected(t *testing.T, result int, err error, expected_result int) {
	if err != nil {
		t.Errorf("Got error %s, expected result %d", err, expected_result)
	}
	if result != expected_result {
		t.Errorf("Got result %d, expected result %d", result, expected_result)
	}
}

type InputAnswer struct {
	input  []string
	answer int
}

func TestPart1_SampleInputs(t *testing.T) {
	inputanswers := []InputAnswer{
		{
			[]string{
				"$ cd /",
				"$ ls",
				"dir a",
				"14848514 b.txt",
				"8504156 c.dat",
				"dir d",
				"$ cd a",
				"$ ls",
				"dir e",
				"29116 f",
				"2557 g",
				"62596 h.lst",
				"$ cd e",
				"$ ls",
				"584 i",
				"$ cd ..",
				"$ cd ..",
				"$ cd d",
				"$ ls",
				"4060174 j",
				"8033020 d.log",
				"5626152 d.ext",
				"7214296 k",
				"",
			}, 95437},
	}
	for _, inputanswer := range inputanswers {
		result, err := Part1(inputanswer.input)
		testValueExpected(t, result, err, inputanswer.answer)
	}
}

func TestPart2_SampleInput(t *testing.T) {
	inputanswers := []InputAnswer{
		{[]string{""}, 0},
	}
	for _, inputanswer := range inputanswers {
		result, err := Part2(inputanswer.input)
		testValueExpected(t, result, err, inputanswer.answer)
	}
}
