package main

import (
	"fmt"
	"os"
	"strings"

	"aoc2022/day2/day2"
)

func main() {
	bytes, err := os.ReadFile("day2_input.txt")
	if err != nil {
		panic(err)
	}
	lines := strings.Split(string(bytes), "\n")
	max_calories, err := day2.Part1(lines)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Part 1 result: %d\n", max_calories)
	top_three_total, err := day2.Part2(lines)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Part 2 result: %d\n", top_three_total)
}
