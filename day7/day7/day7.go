package day7

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

type dir struct {
	name   string
	files  map[string]int
	dirs   map[string]dir
	parent *dir
}

func (d dir) String() string {
	if d.parent == nil {
		return fmt.Sprintf("dir{name: /, files: %#q, dirs: %q, parent: /}",
			d.files, d.dirs)
	}
	return fmt.Sprintf("dir{name: %s, files: %#q, dirs: %q, parent: %s}",
		d.name, d.files, d.dirs, d.parent.name)
}

func dirSizePart1(current_dir dir, sizes map[string]int, totDirSizeBelow100k int) int {
	// fmt.Printf("Getting size for dir %q\n", current_dir)
	tot_size := 0
	for _, size := range current_dir.files {
		tot_size += size
	}
	for _, d := range current_dir.dirs {
		totDirSizeBelow100k = dirSizePart1(d, sizes, totDirSizeBelow100k)
		tot_size += sizes[d.name]
	}
	sizes[current_dir.name] = tot_size
	if tot_size > 100_000 {
		return totDirSizeBelow100k
	}
	return totDirSizeBelow100k + tot_size
}

func dirSizePart2(current_dir dir, sizes map[string]int, smallestSizeLargeEnough int, largeEnough int) int {
	// fmt.Printf("Getting size for dir %q\n", current_dir)
	tot_size := 0
	for _, size := range current_dir.files {
		tot_size += size
	}
	for _, d := range current_dir.dirs {
		smallestSizeLargeEnough = dirSizePart2(d, sizes, smallestSizeLargeEnough, largeEnough)
		tot_size += sizes[d.name]
	}
	sizes[current_dir.name] = tot_size
	if smallestSizeLargeEnough > tot_size && tot_size >= largeEnough {
		return tot_size
	}
	return smallestSizeLargeEnough
}

func createFileSystem(lines []string) dir {
	ii := 0
	root := dir{
		name:   "/",
		files:  map[string]int{},
		dirs:   map[string]dir{},
		parent: nil,
	}
	current_dir := &root
	intRegex, _ := regexp.Compile(`^\d+$`)
	for ii < len(lines) {
		line := lines[ii]
		if len(line) == 0 {
			break
		}
		// fmt.Printf("root = %q\n", root)
		// fmt.Println(line)
		if line[0] == '$' {
			if line[2:4] == "cd" {
				// change directory
				rel_dirname := line[5:]
				// old_dirname := current_dir.name
				if rel_dirname == "/" {
					current_dir = &root
				} else if rel_dirname == ".." && current_dir.parent != nil {
					parent := *current_dir.parent
					current_dir = &parent
				} else {
					subdir := current_dir.dirs[rel_dirname]
					current_dir = &subdir
				}
				ii++
				// fmt.Printf("Changing dir from %s to %s\n", old_dirname, current_dir.name)
			} else if line[2:4] == "ls" {
				// find subsequent lines until the first that starts with '$'
				ii++
				next_line := lines[ii]
				for len(next_line) > 0 && next_line[0] != '$' {
					// fmt.Println(next_line)
					parts := strings.Split(next_line, " ")
					rel_name := parts[1]
					if intRegex.MatchString(parts[0]) {
						size, _ := strconv.ParseInt(parts[0], 10, 32)
						current_dir.files[rel_name] = int(size)
						// fmt.Printf("Adding file %s with size %d to dir %s\n", rel_name, size, current_dir.name)
					} else {
						subdirname := current_dir.name + parts[1] + "/"
						current_dir_true := *current_dir
						subdir := dir{subdirname, map[string]int{}, map[string]dir{}, &current_dir_true}
						current_dir.dirs[rel_name] = subdir
						// fmt.Printf("Adding dir %q to dir %s\n", subdir, current_dir.name)
					}
					ii++
					next_line = lines[ii]
				}
			}
		}
	}
	return root
}

// find sum of directory sizes where each directory has size <= 1e5
func Part1(lines []string) (result int, err error) {
	root := createFileSystem(lines)
	// fmt.Printf("root = %#q\n", root)
	sizes := map[string]int{}
	dirSizeBelow100k := dirSizePart1(root, sizes, 0)
	return dirSizeBelow100k, nil
}

func Part2(lines []string) (result int, err error) {
	root := createFileSystem(lines)
	sizes := map[string]int{}
	dirSizePart1(root, sizes, 0)
	largeEnough := sizes["/"] - 40000000
	return dirSizePart2(root, map[string]int{}, 1<<31-1, largeEnough), nil
}
