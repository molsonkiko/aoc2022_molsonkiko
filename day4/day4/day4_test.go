package day4

import (
	"testing"
)

func testValueExpected(t *testing.T, result int, err error, expected_result int) {
	if err != nil {
		t.Fatalf("Got error %s, expected result %d", err, expected_result)
	}
	if result != expected_result {
		t.Fatalf("Got result %d, expected result %d", result, expected_result)
	}
}

func TestPart1_SampleInput(t *testing.T) {
	input := []string{
		"2-4,6-8",
		"2-3,4-5",
		"5-7,7-9",
		"2-8,3-7",
		"6-6,4-6",
		"2-6,4-8",
	}
	result, err := Part1(input)
	testValueExpected(t, result, err, 2)
}

func TestPart1_NoShared(t *testing.T) {
	input := []string{
		"1-4,5-6",
	}
	result, err := Part1(input)
	testValueExpected(t, result, err, 0)
}

func TestPart1_SharedButNotEnclosing(t *testing.T) {
	input := []string{
		"1-4,3-5",
	}
	result, err := Part1(input)
	testValueExpected(t, result, err, 0)
}

func TestPart1_LeftEnclosesRight(t *testing.T) {
	input := []string{
		"1-4,2-3",
	}
	result, err := Part1(input)
	testValueExpected(t, result, err, 1)
}

func TestPart1_RightEnclosesLeft(t *testing.T) {
	input := []string{
		"2-3,1-4",
	}
	result, err := Part1(input)
	testValueExpected(t, result, err, 1)
}

func TestPart2_SampleInput(t *testing.T) {
	input := []string{
		"2-4,6-8",
		"2-3,4-5",
		"5-7,7-9",
		"2-8,3-7",
		"6-6,4-6",
		"2-6,4-8",
	}
	result, err := Part2(input)
	testValueExpected(t, result, err, 4)
}

func TestPart2_NoShared(t *testing.T) {
	input := []string{
		"1-4,5-6",
	}
	result, err := Part2(input)
	testValueExpected(t, result, err, 0)
}

func TestPart2_SharedButNotEnclosing(t *testing.T) {
	input := []string{
		"1-4,3-5",
	}
	result, err := Part2(input)
	testValueExpected(t, result, err, 1)
}

func TestPart2_LeftEnclosesRight(t *testing.T) {
	input := []string{
		"1-4,2-3",
	}
	result, err := Part2(input)
	testValueExpected(t, result, err, 1)
}

func TestPart2_RightEnclosesLeft(t *testing.T) {
	input := []string{
		"2-3,1-4",
	}
	result, err := Part2(input)
	testValueExpected(t, result, err, 1)
}
