package day2

import (
	"strings"
)

func Part1(lines []string) (result int, err error) {
	score := 0
	for _, line := range lines {
		if len(line) == 0 {
			break
		}
		choices := strings.Split(line, " ")
		they := choices[0]
		switch you := choices[1]; you {
		case "X": // rock
			score += 1
			switch they {
			case "A":
				score += 3 // rock, draw
			case "B": // paper, you lose
			case "C":
				score += 6 // scissors, you win
			}
		case "Y": // paper
			score += 2
			switch they {
			case "A":
				score += 6 // rock, you win
			case "B":
				score += 3 // paper, draw
			case "C": // scissors, you lose
			}
		default: // "Z", scissors
			score += 3
			switch they {
			case "A": // rock, you lose
			case "B":
				score += 6 // paper, you win
			case "C":
				score += 3 // scissors, draw
			}
		}
	}
	return score, nil
}

func Part2(lines []string) (result int, err error) {
	score := 0
	for _, line := range lines {
		if len(line) == 0 {
			break
		}
		choices := strings.Split(line, " ")
		they := choices[0]
		switch you := choices[1]; you {
		case "X": // you must lose
			switch they {
			case "A": // rock, you play scissors
				score += 3
			case "B": // paper, you play rock
				score += 1
			case "C": // scissors, you play paper
				score += 2
			}
		case "Y": // you must draw
			switch they {
			case "A": // rock, you play rock
				score += 4
			case "B": // paper, you play paper
				score += 5
			case "C": // scissors, you play scissors
				score += 6
			}
		default: // you must win
			switch they {
			case "A": // rock, you play paper
				score += 8
			case "B": // paper, you play scissors
				score += 9
			case "C": // scissors, you play rock
				score += 7
			}
		}
	}
	return score, nil
}
