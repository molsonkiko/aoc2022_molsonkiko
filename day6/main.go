package main

import (
	"fmt"
	"os"
	"strings"

	"aoc2022/day6/day6"
)

func main() {
	bytes, err := os.ReadFile("day6_input.txt")
	if err != nil {
		panic(err)
	}
	lines := strings.Split(string(bytes), "\n")
	part1_answer, err := day6.Part1(lines)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Part 1 result: %d\n", part1_answer)
	part2_answer, err := day6.Part2(lines)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Part 2 result: %d\n", part2_answer)
}