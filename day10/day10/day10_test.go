package day10

import (
	"os"
	"regexp"
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
	sampleBytes, err := os.ReadFile("..\\day10_sample_input.txt")
	if err != nil {
		t.Fatalf("File not found")
		return
	}
	rex, _ := regexp.Compile("\r?\n")
	inp := rex.Split(string(sampleBytes), -1)
	inputanswers := []InputAnswer{
		{inp, 13140},
	}
	for _, inputanswer := range inputanswers {
		result, err := Part1(inputanswer.input)
		testValueExpected(t, result, err, inputanswer.answer)
	}
}

// can't unit test part 2 easily, because it relies on what series
// of inputs will look subjectively like a series of letters
