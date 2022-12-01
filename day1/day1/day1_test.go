package day1

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

func TestPart1_NoElves(t *testing.T) {
	lines := []string{""}
	result, err := Part1(lines)
	testValueExpected(t, result, err, 0)
}

func TestPart1_OneElf(t *testing.T) {
	lines := []string{"100", "50", "15", ""}
	result, err := Part1(lines)
	testValueExpected(t, result, err, 165)
}

func TestPart1_ElfOneRow(t *testing.T) {
	lines := []string{"100", ""}
	result, err := Part1(lines)
	testValueExpected(t, result, err, 100)
}

func TestPart1_TwoElves(t *testing.T) {
	lines := []string{"100", "", "150", ""}
	result, err := Part1(lines)
	testValueExpected(t, result, err, 150)
}

func TestPart2_TwoElves(t *testing.T) {
	lines := []string{"100", "", "150", ""}
	result, err := Part2(lines)
	testValueExpected(t, result, err, 250)
}

func TestPart2_OneElf(t *testing.T) {
	lines := []string{"100", "10", ""}
	result, err := Part2(lines)
	testValueExpected(t, result, err, 110)
}

func TestPart2_FourElves_TopThreeAtStart(t *testing.T) {
	lines := []string{"100", "", "150", "75", "", "125", "", "75", ""}
	result, err := Part2(lines)
	testValueExpected(t, result, err, 450)
}

func TestPart2_FourElves_MaxAtEnd(t *testing.T) {
	lines := []string{"100", "", "60", "", "125", "", "75", "150", ""}
	result, err := Part2(lines)
	testValueExpected(t, result, err, 450)
}

func TestPart2_FiveElves_MaxAtEnd(t *testing.T) {
	lines := []string{"50", "5", "", "100", "", "60", "", "125", "", "75", "150", ""}
	result, err := Part2(lines)
	testValueExpected(t, result, err, 450)
}
