package day20

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
	input []string
	answer int
}

var sampleInput = []string{
    "",
}

func TestPart1_SampleInputs(t *testing.T) {
	inputanswers := []InputAnswer{
		{sampleInput, 0 },
	}
	for _, inputanswer := range inputanswers {
		result, err := Part1(inputanswer.input)
		testValueExpected(t, result, err, inputanswer.answer)
	}
}

func TestPart2_SampleInput(t *testing.T) {
	inputanswers := []InputAnswer{
		{sampleInput, 0},
	}
	for _, inputanswer := range inputanswers {
		result, err := Part2(inputanswer.input)
		testValueExpected(t, result, err, inputanswer.answer)
	}
}
