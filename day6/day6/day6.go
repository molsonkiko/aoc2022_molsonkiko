package day6

func nDifferentChars(last_n []byte, c byte, n int) (different bool, last_n_new []byte) {
	last_n = append(last_n, c)
	if len(last_n) < n {
		return false, last_n
	}
	uniques := map[byte]int{}
	for _, b := range last_n {
		if _, b_in_uniques := uniques[b]; b_in_uniques {
			return false, last_n[1:]
		}
		uniques[b] = 0
	}
	return true, last_n[1:]
}

func Part1(lines []string) (result int, err error) {
	line := lines[0]
	last_three := []byte{}
	different := false
	for ii := 0; ii < len(line); ii++ {
		c := line[ii]
		different, last_three = nDifferentChars(last_three, c, 4)
		if different {
			return ii + 1, nil
		}
	}
	return len(line), nil
}

func Part2(lines []string) (result int, err error) {
	line := lines[0]
	last_three := []byte{}
	different := false
	for ii := 0; ii < len(line); ii++ {
		c := line[ii]
		different, last_three = nDifferentChars(last_three, c, 14)
		if different {
			return ii + 1, nil
		}
	}
	return len(line), nil
}
