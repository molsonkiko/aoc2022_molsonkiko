package main

import (
	"fmt"
	"os"
	"strings"

	"aoc2022/day7/day7"
)

func main() {
	bytes, err := os.ReadFile("day7_input.txt")
	if err != nil {
		panic(err)
	}
	lines := strings.Split(string(bytes), "\n")
	part1_answer, err := day7.Part1(lines)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Part 1 result: %d\n", part1_answer)
	part2_answer, err := day7.Part2(lines)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Part 2 result: %d\n", part2_answer)
}