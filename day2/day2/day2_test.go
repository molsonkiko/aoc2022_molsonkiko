package day2

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
	lines := []string{"A Y", "B X", "C Z"}
	result, err := Part1(lines)
	testValueExpected(t, result, err, 15)
}

func TestPart1_Empty(t *testing.T) {
	lines := []string{""}
	result, err := Part1(lines)
	testValueExpected(t, result, err, 0)
}

func TestPart1_YouRockTheyScissors(t *testing.T) {
	lines := []string{"C X", "C X"}
	result, err := Part1(lines)
	testValueExpected(t, result, err, 14)
}

func TestPart1_YouPaperTheyPaper(t *testing.T) {
	lines := []string{"B Y", "B Y"}
	result, err := Part1(lines)
	testValueExpected(t, result, err, 10)
}

func TestPart2_TheyScissorsYouLose(t *testing.T) {
	lines := []string{"C X", "C X"}
	result, err := Part2(lines)
	testValueExpected(t, result, err, 4)
}

func TestPart2_TheyPaperYouDraw(t *testing.T) {
	lines := []string{"B Y", "B Y"}
	result, err := Part2(lines)
	testValueExpected(t, result, err, 10)
}

func TestPart2_SampleInput(t *testing.T) {
	lines := []string{"A Y", "B X", "C Z"}
	result, err := Part2(lines)
	testValueExpected(t, result, err, 12)
}
