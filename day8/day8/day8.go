package day8

func Part1(lines []string) (result int, err error) {
	h := len(lines)
	w := len(lines[0])
	if len(lines[h-1]) < w {
		h--
		lines = lines[:h]
	}
	visibleFromOutside := h*2 + w*2 - 4 // on perimeter
	for ii := 1; ii < h-1; ii++ {
		for jj := 1; jj < w-1; jj++ {
			v := lines[ii][jj]
			visible := 4
			for ii2 := ii - 1; ii2 >= 0; ii2-- {
				if lines[ii2][jj] >= v {
					visible--
					break
				}
			}
			for ii2 := ii + 1; ii2 < h; ii2++ {
				if lines[ii2][jj] >= v {
					visible--
					break
				}
			}
			for jj2 := jj - 1; jj2 >= 0; jj2-- {
				if lines[ii][jj2] >= v {
					visible--
					break
				}
			}
			for jj2 := jj + 1; jj2 < w; jj2++ {
				if lines[ii][jj2] >= v {
					visible--
					break
				}
			}
			if visible > 0 {
				visibleFromOutside++
			}
		}
	}
	return visibleFromOutside, nil
}

func Part2(lines []string) (result int, err error) {
	h := len(lines)
	w := len(lines[0])
	if len(lines[h-1]) < w {
		h--
		lines = lines[:h]
	}
	maxScenicScore := 0
	for ii := 1; ii < h-1; ii++ {
		for jj := 1; jj < w-1; jj++ {
			v := lines[ii][jj]
			scenicScoreParts := make([]int, 4)
			for ii2 := ii - 1; ii2 >= 0; ii2-- {
				scenicScoreParts[0]++
				if lines[ii2][jj] >= v {
					break
				}
			}
			for ii2 := ii + 1; ii2 < h; ii2++ {
				scenicScoreParts[1]++
				if lines[ii2][jj] >= v {
					break
				}
			}
			for jj2 := jj - 1; jj2 >= 0; jj2-- {
				scenicScoreParts[2]++
				if lines[ii][jj2] >= v {
					break
				}
			}
			for jj2 := jj + 1; jj2 < w; jj2++ {
				scenicScoreParts[3]++
				if lines[ii][jj2] >= v {
					break
				}
			}
			scenicScore := scenicScoreParts[0] * scenicScoreParts[1] * scenicScoreParts[2] * scenicScoreParts[3]
			if scenicScore > maxScenicScore {
				maxScenicScore = scenicScore
			}
		}
	}
	return maxScenicScore, nil
}
