package day3

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
		"vJrwpWtwJgWrhcsFMMfFFhFp",
		"jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
		"PmmdzqPrVvPwwTWBwg",
		"wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
		"ttgJtRGJQctTZtZT",
		"CrZsJsPPZsGzwwsLwLmpwMDw",
	}
	result, err := Part1(input)
	testValueExpected(t, result, err, 157)
}

func TestPart1_NoShared(t *testing.T) {
	input := []string{
		"aA",
	}
	result, err := Part1(input)
	testValueExpected(t, result, err, 0)
}

func TestPart1_OneSharedLowercase(t *testing.T) {
	input := []string{
		"BccA",
	}
	result, err := Part1(input)
	testValueExpected(t, result, err, 3)
}

func TestPart1_OneSharedUppercase(t *testing.T) {
	input := []string{
		"rbEfEa",
	}
	result, err := Part1(input)
	testValueExpected(t, result, err, 31)
}

func TestPart1_OneSharedUppercaseMultiInstance(t *testing.T) {
	input := []string{
		"rbZZfZqa",
	}
	result, err := Part1(input)
	testValueExpected(t, result, err, 52)
}

func TestPart1_OneSharedLowercaseMultiInstance(t *testing.T) {
	input := []string{
		"rBzzfzQa",
	}
	result, err := Part1(input)
	testValueExpected(t, result, err, 26)
}

func TestPart2_SampleInput(t *testing.T) {
	input := []string{
		"vJrwpWtwJgWrhcsFMMfFFhFp",
		"jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
		"PmmdzqPrVvPwwTWBwg",
		"wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
		"ttgJtRGJQctTZtZT",
		"CrZsJsPPZsGzwwsLwLmpwMDw",
	}
	result, err := Part2(input)
	testValueExpected(t, result, err, 70)
}
