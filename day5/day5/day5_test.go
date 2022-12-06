package day5

import (
	"testing"
)

func testValueExpected(t *testing.T, result string, err error, expected_result string) {
	if err != nil {
		t.Fatalf("Got error %s, expected result %s", err, expected_result)
	}
	if result != expected_result {
		t.Fatalf("Got result %s, expected result %s", result, expected_result)
	}
}

func TestPart1_SampleInput(t *testing.T) {
	input := []string{
		"    [D]    ",
		"[N] [C]    ",
		"[Z] [M] [P]",
		" 1   2   3 ",
		"",
		"move 1 from 2 to 1",
		"move 3 from 1 to 3",
		"move 2 from 2 to 1",
		"move 1 from 1 to 2",
	}
	result, err := Part1(input)
	testValueExpected(t, result, err, "CMZ")
}

func TestPart2_SampleInput(t *testing.T) {
	input := []string{
		"    [D]    ",
		"[N] [C]    ",
		"[Z] [M] [P]",
		" 1   2   3 ",
		"",
		"move 1 from 2 to 1",
		"move 3 from 1 to 3",
		"move 2 from 2 to 1",
		"move 1 from 1 to 2",
	}
	result, err := Part2(input)
	testValueExpected(t, result, err, "MCD")
}
