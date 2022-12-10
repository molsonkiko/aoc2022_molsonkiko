package day10

import (
	"regexp"
	"strconv"
	"strings"
)

func Part1(lines []string) (result int, err error) {
	x := 1
	cycles := 0
	interesting_values := map[int]int{
		20:  0,
		60:  0,
		100: 0,
		140: 0,
		180: 0,
		220: 0,
	}
	last_amount := 0
	whitespace, _ := regexp.Compile(`\s+`)
	for _, line := range lines {
		if len(line) == 0 {
			continue
		}
		if _, contains_cycles := interesting_values[cycles]; contains_cycles {
			interesting_values[cycles] = (x - last_amount) * cycles
		}
		parts := whitespace.Split(line, -1)
		if len(parts) == 1 { // noop
			cycles++
			last_amount = 0
			continue
		}
		cycles += 2
		_, contains_cycles_min1 := interesting_values[cycles-1]
		if contains_cycles_min1 {
			interesting_values[cycles-1] = x * (cycles - 1)
		}
		last_amount, _ := strconv.ParseInt(parts[1], 10, 32)
		x += int(last_amount)
	}
	if _, contains_cycles := interesting_values[cycles]; contains_cycles {
		interesting_values[cycles] = (x - last_amount) * cycles
	}
	total_signal := 0
	for _, signal := range interesting_values {
		total_signal += signal
	}
	return total_signal, nil
}

func drawPixel(pixels []byte, cycles int, x int) {
	distance := x%40 - cycles%40
	if distance == 0 || distance == 1 || distance == -1 {
		pixels[cycles] = '#'
	}
}

func Part2(lines []string) (result string, err error) {
	pixels := make([]byte, 240)
	for ii := 0; ii < 240; ii++ {
		pixels[ii] = '.'
	}
	x := 1
	cycles := 0
	whitespace, _ := regexp.Compile(`\s+`)
	for _, line := range lines {
		if len(line) == 0 {
			continue
		}
		parts := whitespace.Split(line, -1)
		drawPixel(pixels, cycles, x)
		if len(parts) == 1 {
			cycles++
			continue
		}
		cycles += 2
		drawPixel(pixels, cycles-1, x)
		last_amount_i64, _ := strconv.ParseInt(parts[1], 10, 32)
		x += int(last_amount_i64)
	}
	var sb strings.Builder
	for ii := 0; ii < 240; ii += 40 {
		sb.WriteString(string(pixels[ii : ii+40]))
		sb.WriteByte('\n')
	}
	return sb.String(), nil
}
