package main

import (
	"fmt"
	"os"
	"strings"

	"aoc2022/day5/day5"
)

func main() {
	bytes, err := os.ReadFile("day5_input.txt")
	if err != nil {
		panic(err)
	}
	lines := strings.Split(string(bytes), "\n")
	part1_answer, err := day5.Part1(lines)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Part 1 result: %s\n", part1_answer)
	part2_answer, err := day5.Part2(lines)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Part 2 result: %s\n", part2_answer)
}
