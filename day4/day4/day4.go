package day4

import (
	"regexp"
	"strconv"
)

func Part1(lines []string) (result int, err error) {
	enclosings := 0
	intregex, err := regexp.Compile(`\d+`)
	if err != nil {
		return 0, err
	}
	for _, line := range lines {
		numstrs := intregex.FindAll([]byte(line), -1)
		if len(numstrs) < 4 {
			continue
		}
		nums := make([]int64, 4)
		for ii := 0; ii < 4; ii++ {
			numstr := string(numstrs[ii])
			nums[ii], err = strconv.ParseInt(numstr, 10, 32)
			if err != nil {
				return 0, err
			}
		}
		if (nums[0] <= nums[2] && nums[3] <= nums[1]) || // left encloses right
			(nums[2] <= nums[0] && nums[1] <= nums[3]) { // right encloses left
			enclosings++
		}
	}
	return enclosings, nil
}

func Part2(lines []string) (result int, err error) {
	overlaps := 0
	intregex, err := regexp.Compile(`\d+`)
	if err != nil {
		return 0, err
	}
	for _, line := range lines {
		numstrs := intregex.FindAll([]byte(line), -1)
		if len(numstrs) < 4 {
			continue
		}
		nums := make([]int64, 4)
		for ii := 0; ii < 4; ii++ {
			numstr := string(numstrs[ii])
			nums[ii], err = strconv.ParseInt(numstr, 10, 32)
			if err != nil {
				return 0, err
			}
		}
		if !((nums[0] < nums[2] && nums[1] < nums[2]) || // left is fully below right
			(nums[0] > nums[3] && nums[1] > nums[3])) { // left is fully above right
			overlaps++
		}
	}
	return overlaps, nil
}
