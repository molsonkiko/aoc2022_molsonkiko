package day7

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

type InputAnswer struct {
	input []string;
	answer int;
};

func TestPart1_SampleInputs(t *testing.T) {
	inputanswers := []InputAnswer{
		{[]string{""}, 0 },
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
