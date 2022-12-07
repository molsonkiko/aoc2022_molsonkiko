import json
import pprint
import re
import unittest

class Dir:
    name: str
    files: dict[str, int]
    #dirs: dict[str, Dir]
    #parent: Dir

    def __init__(self, name, files, dirs, parent) -> None:
        self.name = name
        self.files = files
        self.dirs = dirs
        self.parent = parent

    def __str__(self):
        if self.parent is None:
            return f'Dir(name = /, files = {self.files}, dirs = {self.dirs}, parent = /)'
        return f'Dir(name = {self.name}, files = {json.dumps(self.files, indent=4)}, dirs = {pprint.pformat(self.dirs)}, parent = {self.parent.name})'

    __repr__ = __str__


def dir_size_part1(curdir: Dir, sizes: dict[str, int], dirs_under_100k: int) -> int:
    sizes[curdir.name] = sum(curdir.files.values())
    for d in curdir.dirs.values():
        dirs_under_100k = dir_size_part1(d, sizes, dirs_under_100k)
        sizes[curdir.name] += sizes[d.name]
    if sizes[curdir.name] > 1e5:
        return dirs_under_100k
    # print(f'dir {curdir} has size less than 100k, {sizes[curdir.name]}')
    return dirs_under_100k + sizes[curdir.name]

def dir_size_part2(curdir: Dir, sizes: dict[str, int], smallest_dir_large_enough: float, large_enough: int) -> int:
    totsize = sum(curdir.files.values())
    for d in curdir.dirs.values():
        smallest_dir_large_enough = dir_size_part2(d, sizes, smallest_dir_large_enough, large_enough)
        totsize += sizes[d.name]
    sizes[curdir.name] = totsize
    if smallest_dir_large_enough > totsize >= large_enough:
        return totsize
    # print(f'dir {curdir} has size less than 100k, {sizes[curdir.name]}')
    return smallest_dir_large_enough

def create_filesystem(lines) -> Dir:
    ii = 0
    ROOT = Dir("/", {}, {}, None)
    curdir = ROOT
    while ii < len(lines) and lines[ii]:
        line = lines[ii]
        # print(line)
        if line[0] == '$':
            if line[2:4] == 'cd':
                subdirname = line[5:]
                if subdirname == '/':
                    curdir = ROOT
                elif subdirname == '..' and curdir is not ROOT:
                    curdir = curdir.parent
                else:
                    curdir = curdir.dirs[subdirname]
                # print(f'changing dir from {old_dir} to {curdir}')
                ii += 1
            elif line[2:4] == 'ls':
                ii += 1
                while ii < len(lines) and lines[ii] and lines[ii][0] != '$':
                    line = lines[ii]
                    # print(line)
                    part1, part2 = line.split()
                    if re.fullmatch('\d+', part1):
                        # print(f'adding file {part2} with size {part1} to dir {curdir}')
                        curdir.files[part2] = int(part1)
                    else:
                        # print(f'adding dir {part2} to dir {curdir}')
                        subdirname = f'{curdir.name}{part2}/'
                        curdir.dirs[part2] = Dir(subdirname, {}, {}, curdir)
                    ii += 1
    return ROOT

def Part1(lines: list[str]):
    ROOT = create_filesystem(lines)    
    # print(f'finally, root = {pprint.pformat(ROOT)}')
    dirs_under_100k = dir_size_part1(ROOT, {}, 0)
    return dirs_under_100k

def Part2(lines: list[str]) -> int:
    ROOT = create_filesystem(lines)
    sizes = {}
    dir_size_part1(ROOT, sizes, 0)
    large_enough = sizes['/'] - 40000000
    smallest_dir_large_enough = dir_size_part2(ROOT, {}, float('inf'), large_enough)
    return smallest_dir_large_enough

class Part1Tests(unittest.TestCase):
    def testPart1_sample_input(self):
        inp = [
            "$ cd /",
            "$ ls",
            "dir a",
            "14848514 b.txt",
            "8504156 c.dat",
            "dir d",
            "$ cd a",
            "$ ls",
            "dir e",
            "29116 f",
            "2557 g",
            "62596 h.lst",
            "$ cd e",
            "$ ls",
            "584 i",
            "$ cd ..",
            "$ cd ..",
            "$ cd d",
            "$ ls",
            "4060174 j",
            "8033020 d.log",
            "5626152 d.ext",
            "7214296 k",
            "",
        ]
        self.assertEqual(Part1(inp), 95437)

    def testPart1_dirs_with_only_subdirs(self):
        inp = [
            '$ cd /',
            '$ ls',
            'dir a',
            'dir b',
            '$ cd a',
            '$ ls',
            'dir ac',
            '$ cd ac',
            '$ ls',
            'dir acd',
            '$ cd acd',
            '$ ls',
            '100 acd.txt',
            '$ cd ..',
            '$ cd /',
            '$ cd b',
            '$ ls',
            'dir ba',
            '10000000 big.txt',
            '$ cd ba',
            '$ ls',
            '100000000 big2.txt',
            ''
        ]
        self.assertEqual(Part1(inp), 300)


class TestPart2(unittest.TestCase):
    def testPart2_sample_input(self):
        inp = [
            "$ cd /",
            "$ ls",
            "dir a",
            "14848514 b.txt",
            "8504156 c.dat",
            "dir d",
            "$ cd a",
            "$ ls",
            "dir e",
            "29116 f",
            "2557 g",
            "62596 h.lst",
            "$ cd e",
            "$ ls",
            "584 i",
            "$ cd ..",
            "$ cd ..",
            "$ cd d",
            "$ ls",
            "4060174 j",
            "8033020 d.log",
            "5626152 d.ext",
            "7214296 k",
            "",
        ]
        self.assertEqual(Part2(inp), 24933642)

if __name__ == '__main__':
    with open('day7_input.txt') as f:
        lines = re.split('\r?\n', f.read())
    part1_answer = Part1(lines)
    print(f'part 1 answer = {part1_answer}')
    part2_answer = Part2(lines)
    print(f'part 2 answer = {part2_answer}')
    unittest.main()