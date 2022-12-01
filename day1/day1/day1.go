package day1

import (
	"sort"
	"strconv"
)

func Part1(lines []string) (result int, err error) {
	max_calories := 0
	current_elf_calories := 0
	for _, line := range lines {
		if len(line) == 0 {
			if current_elf_calories > max_calories {
				max_calories = current_elf_calories
			}
			current_elf_calories = 0
			continue
		}
		calorie_num, err := strconv.ParseInt(line, 10, 32)
		if err != nil {
			return -1, err
		}
		current_elf_calories += int(calorie_num)
	}
	return max_calories, nil
}

func Part2(lines []string) (result int, err error) {
	top_three := []int{0, 0, 0}
	current_elf_calories := 0
	for _, line := range lines {
		if len(line) == 0 {
			top_three = append(top_three, current_elf_calories)
			sort.Ints(top_three)
			top_three = top_three[1:]
			current_elf_calories = 0
			continue
		}
		calorie_num, err := strconv.ParseInt(line, 10, 32)
		if err != nil {
			return -1, err
		}
		current_elf_calories += int(calorie_num)
	}
	top_three_total := 0
	for _, calories := range top_three {
		top_three_total += calories
	}
	return top_three_total, nil
}
