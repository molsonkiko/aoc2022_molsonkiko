package day5

import (
	"regexp"
	"sort"
	"strconv"
	"strings"
)

func stackCrates(lines []string) (stacks [][]byte, last_line int) {
	stack_dict := map[int][]byte{}
	for line_num, line := range lines {
		for ii := 1; ii < len(line); ii++ {
			c := line[ii]
			if '1' <= c && c <= '9' && line[0] == ' ' {
				// we're at the end of the stacks, but they're
				// ordered top->bottom and not necessarily
				// from left to right
				keys := []int{}
				for k := range stack_dict {
					keys = append(keys, k)
				}
				sort.Ints(keys)
				for ii, k := range keys {
					// reverse each stack and add them to stacks
					// in the order in which they were presented in the file
					stack := stack_dict[k]
					stacks = append(stacks, []byte{})
					for jj := len(stack) - 1; jj >= 0; jj-- {
						stacks[ii] = append(stacks[ii], stack[jj])
					}
				}
				return stacks, line_num + 2
				// there's a blank line after the numbers and then the
				// first instruction
			}
			if ii%4 == 1 {
				stacknum := ii / 4
				if stacknum == len(stack_dict) {
					stack_dict[stacknum] = make([]byte, 0)
				}
				if 'A' <= c && c <= 'Z' {
					stack_dict[stacknum] = append(stack_dict[stacknum], c)
				}
			}
		}
	}
	return [][]byte{}, len(lines)
}

// a line like "move 4 from 1 to 5"
func parseInstructionLine(line string) (count int, from int, to int, err error) {
	intRegex, _ := regexp.Compile(`\d+`)
	count_to_from := intRegex.FindAll([]byte(line), -1)
	if len(count_to_from) < 3 {
		return -1, 0, 0, nil
	}
	count_, err := strconv.ParseInt(string(count_to_from[0]), 10, 32)
	if err != nil {
		return 0, 0, 0, err
	}
	from_idx, err := strconv.ParseInt(string(count_to_from[1]), 10, 32)
	if err != nil {
		return 0, 0, 0, err
	}
	to_idx, err := strconv.ParseInt(string(count_to_from[2]), 10, 32)
	if err != nil {
		return 0, 0, 0, err
	}
	return int(count_), int(from_idx) - 1, int(to_idx) - 1, nil
}

func Part1(lines []string) (result string, err error) {
	stacks, first_instruction_line := stackCrates(lines)
	for ii := first_instruction_line; ii < len(lines); ii++ {
		count, from_idx, to_idx, err := parseInstructionLine(lines[ii])
		if err != nil {
			return "", err
		}
		if count < 0 {
			break
		}
		from := stacks[from_idx]
		lf_min_ct := len(from) - count
		// boxes are added from top to bottom
		for jj := len(from) - 1; jj >= lf_min_ct; jj-- {
			stacks[to_idx] = append(stacks[to_idx], from[jj])
		}
		stacks[from_idx] = from[:lf_min_ct]
	}
	var sb strings.Builder
	for _, stack := range stacks {
		sb.WriteByte(stack[len(stack)-1])
	}
	return sb.String(), nil
}

func Part2(lines []string) (result string, err error) {
	stacks, first_instruction_line := stackCrates(lines)
	for ii := first_instruction_line; ii < len(lines); ii++ {
		count, from_idx, to_idx, err := parseInstructionLine(lines[ii])
		if err != nil {
			return "", err
		}
		if count < 0 {
			break
		}
		from := stacks[from_idx]
		lf_min_ct := len(from) - count
		// boxes are added from bottom to top
		for jj := lf_min_ct; jj < len(from); jj++ {
			stacks[to_idx] = append(stacks[to_idx], from[jj])
		}
		stacks[from_idx] = from[:lf_min_ct]
	}
	var sb strings.Builder
	for _, stack := range stacks {
		sb.WriteByte(stack[len(stack)-1])
	}
	return sb.String(), nil
}
