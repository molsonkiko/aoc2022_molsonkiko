package main

import (
	"fmt"
	"os"
	"regexp"

	"aoc2022/day17/day17"
)

func main() {
	bytes, err := os.ReadFile("day17_input.txt")
	if err != nil {
		panic(err)
	}
    newline, _ := regexp.Compile(`\r?\n`)
	lines := newline.Split(string(bytes), -1)
	part1_answer, err := day17.Part1(lines)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Part 1 result: %d\n", part1_answer)
	part2_answer, err := day17.Part2(lines)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Part 2 result: %d\n", part2_answer)
}