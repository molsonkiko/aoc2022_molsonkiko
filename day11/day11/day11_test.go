package day11

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

var sampleInput = []string{
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
}

func TestPart1_SampleInputs(t *testing.T) {
	inputanswers := []InputAnswer{
		{sampleInput, 10605},
	}
	for _, inputanswer := range inputanswers {
		result, err := Part1(inputanswer.input)
		testValueExpected(t, result, err, inputanswer.answer)
	}
}

func TestPart2_SampleInput(t *testing.T) {
	inputanswers := []InputAnswer{
		{sampleInput, 2713310158},
	}
	for _, inputanswer := range inputanswers {
		result, err := Part2(inputanswer.input)
		testValueExpected(t, result, err, inputanswer.answer)
	}
}
