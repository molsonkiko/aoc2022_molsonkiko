package day3

import (
	"fmt"
)

// c must be a lowercase or uppercase ascii letter
func priorityOfChar(c byte) int {
	if 'a' <= c && c <= 'z' {
		return int(c) - 96 // a-z is 1-26
	}
	if 'A' <= c && c <= 'Z' {
		return int(c) - 38 // A-Z is 27-52
	}
	return -1
}

func sharedCharInLine(line string) (priority int, err error) {
	halflen := len(line) / 2
	if halflen == 0 {
		return 0, nil
	}
	first_half := line[:halflen]
	first_half_unique := map[byte]int{}
	for ii := 0; ii < halflen; ii++ {
		c := first_half[ii]
		first_half_unique[c] = 0
	}
	second_half := line[halflen:]
	for ii := 0; ii < halflen; ii++ {
		c := second_half[ii]
		_, c_in_first_half := first_half_unique[c]
		if c_in_first_half {
			// this is a shared character, so add its priority
			priority := priorityOfChar(c)
			if priority < 0 {
				return -1, fmt.Errorf("invalid character %d", c)
			}
			return priority, nil
		}
	}
	return -1, fmt.Errorf("no shared character between halves")
}

func Part1(lines []string) (result int, err error) {
	priority_sum := 0
	for _, line := range lines {
		priority, err := sharedCharInLine(line)
		if err != nil {
			if priority < 0 { // no shared character between halves
				continue
			}
			return 0, err
		}
		priority_sum += priority
	}
	return priority_sum, nil
}

func Part2(lines []string) (result int, err error) {
	priority_sum := 0
	uniques := make([]map[byte]int, 3)
	for ii, line := range lines {
		mod := ii % 3
		uniques[mod] = map[byte]int{}
		for jj := 0; jj < len(line); jj++ {
			uniques[mod][line[jj]] = 0
		}
		if err != nil {
			return 0, err
		}
		if mod == 2 {
			shared_first_and_second := map[byte]int{}
			for c := range uniques[1] {
				_, c_in_first := uniques[0][c]
				if c_in_first {
					shared_first_and_second[c] = 0
				}
			}
			shared_in_all := byte(0)
			for c := range uniques[2] {
				_, c_in_first_and_second := shared_first_and_second[c]
				if c_in_first_and_second {
					shared_in_all = c
					break
				}
			}
			if shared_in_all == 0 {
				return 0, fmt.Errorf("no character shared in lines %s", lines[ii-2:ii+1])
			}
			priority := priorityOfChar(shared_in_all)
			if priority < 0 {
				return 0, fmt.Errorf("invalid character %d", shared_in_all)
			}
			priority_sum += priority
		}
	}
	return priority_sum, nil
}
