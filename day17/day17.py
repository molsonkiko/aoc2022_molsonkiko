'''Tetris!'''
import re
import time
import unittest

def render_room(room: list[list[bool]]):
    out = ''
    for ii in range(-1, -len(room) - 1, -1):
        row = room[ii]
        out += '|'
        for jj in range(len(row)):
            out += '#' if row[jj] else '.'
        out += '|\n'
    out += '+-------+'
    return out

def Part1(lines: list[str], tot_shapes = 2022, verbose=False):
    '''
The tunnels eventually open into a very tall, narrow chamber. 
Large, oddly-shaped rocks are falling into the chamber from above, 
presumably due to all the rumbling. 
If you can't work out where the rocks will fall next, you might be crushed!

The five types of rocks have the following peculiar shapes, 
where # is rock and . is empty space:

####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##

The rocks fall in the order shown above: first the - shape, 
then the + shape, and so on. Once the end of the list is reached, 
the same order repeats: the - shape falls first, sixth, 11th, 16th, etc.

The rocks don't spin, but they do get pushed around by jets of hot gas 
coming out of the walls themselves. A quick scan reveals the effect the 
jets of hot gas will have on the rocks as they fall (your puzzle input).

For example, suppose this was the jet pattern in your cave:

>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>

In jet patterns, < means a push to the left, 
while > means a push to the right. 
The pattern above means that the jets will push a falling rock right,
then right, then right, then left, then left, then right, and so on.
If the end of the list is reached, it repeats.

The tall, vertical chamber is exactly seven units wide.
Each rock appears so that its left edge is two units away 
from the left wall and its bottom edge is three units above the
highest rock in the room (or the floor, if there isn't one).

After a rock appears, it alternates between being pushed by a jet 
of hot gas one unit (in the direction indicated by the next symbol in the
jet pattern) and then falling one unit down.
If any movement would cause any part of the rock to move into the
walls, floor, or a stopped rock, the movement instead does not occur.
If a downward movement would have caused a falling rock to move
into the floor or an already-fallen rock, the falling rock 
stops where it is (having landed on something) 
and a new rock immediately begins falling.

QUESTION:
How many units tall will the tower of 
rocks be after 2022 rocks have stopped falling?
    '''
    gusts = lines[0]
    shape_order = [
        [[True, True, True, True]], # long horizontal
        [[False, True, False], # cross shape
         [True, True, True],
         [False, True, False]],
        [[False, False, True], # backwards L
         [False, False, True],
         [True, True, True]],
        [[True], # long vertical
         [True],
         [True],
         [True]],
        [[True, True], # box
         [True, True]]
    ]
    room = []
    gust_num = 0
    for shape_num in range(tot_shapes):
        if verbose and shape_num < 10:
            print(f'BLOCK {shape_num}\n=====================\n=====================')
            print(f'Room =\n{render_room(room)}')
        shape = shape_order[shape_num % 5]
        h = len(shape)
        w = len(shape[0])
        top = -1
        bottom = top - h
        right = 2 + w
        left = 2
        for _ in range(3 + h):
            room.append([False, False, False, False, False, False, False])
        # place the rock in its initial location
        for ii in range(h):
            for jj in range(w):
                room[top - ii][left + jj] = shape[ii][jj]
        # begin gusting
        while True:
            direction = gusts[gust_num % len(gusts)]
            gust_num += 1
            if verbose and shape_num < 10:
                print(f'{direction = }, {left = }, {right = }, {top = }, {bottom = }, {len(room) = }')
            if direction == '>': # move right
                if right < 7:
                    new_left = left + 1
                    can_move_right = True
                    for ii in range(h):
                        for jj in range(w - 1):
                            # you can't move right if a square that was previously
                            # unfilled by the shape would now become filled by
                            # the shape but is already occupied
                            if (shape[ii][jj] and not shape[ii][jj + 1]) and room[top - ii][new_left + jj]:
                                can_move_right = False
                                break
                    for ii in range(h):
                        if shape[ii][w - 1] and room[top - ii][left + w]:
                            can_move_right = False
                            break
                    if can_move_right:
                        left += 1
                        right += 1
                        for ii in range(h):
                            for jj in range(1, w - 1):
                                # empty any squares that were filled by the object
                                # but are now empty
                                should_change = shape[ii][jj + 1] ^ shape[ii][jj]
                                if should_change:
                                    room[top - ii][left + jj] = shape[ii][jj]
                        # now fill leading edge
                        for ii in range(h):
                            if shape[ii][w - 1]:
                                room[top - ii][right - 1] = True
                        # now empty trailing edge
                        for ii in range(h):
                            if shape[ii][0]:
                                room[top - ii][left] = False
            elif left > 0: # move left
                can_move_left = True
                new_left = left - 1
                for ii in range(h):
                    for jj in range(1, w):
                        # you can't move left if a square that was previously
                        # unfilled by the shape would now become filled by
                        # the shape but is already occupied
                        if (shape[ii][jj] and not shape[ii][jj - 1]) and room[top - ii][new_left + jj]:
                            can_move_left = False
                            break
                for ii in range(h):
                    if shape[ii][0] and room[top - ii][new_left]:
                        can_move_left = False
                        break
                if can_move_left:
                    left -= 1
                    right -= 1
                    for ii in range(h):
                        for jj in range(1, w - 1):
                            # empty any squares that were filled by the object
                            # but are now empty
                            should_change = shape[ii][jj - 1] ^ shape[ii][jj]
                            if should_change:
                                room[top - ii][left + jj] = shape[ii][jj]
                    # now fill leading edge
                    for ii in range(h):
                        if shape[ii][0]:
                            room[top - ii][left] = True
                    # now empty trailing edge
                    for ii in range(h):
                        if shape[ii][w - 1]:
                            room[top - ii][right - 1] = False
            can_move_down = True
            new_top = top - 1
            if bottom >= -len(room):
                for ii in range(h - 1):
                    for jj in range(w):
                        if (shape[ii][jj] and not shape[ii + 1][jj]) and room[new_top - ii][left + jj]:
                            can_move_down = False
                            break
                for jj in range(w):
                    if shape[h - 1][jj] and room[bottom][left + jj]:
                        can_move_down = False
                        break
            else:
                break
            if can_move_down:
                top -= 1
                bottom -= 1
                for ii in range(1, h - 1):
                    for jj in range(w):
                        # empty any squares that were filled by shape but are now empty
                        should_change = shape[ii - 1][jj] ^ shape[ii][jj]
                        if should_change:
                            room[top - ii][left + jj] = shape[ii - 1][jj]
                for jj in range(w):
                    # fill leading edge
                    if shape[h - 1][jj]:
                        room[bottom + 1][jj] = True
                # empty trailing edge
                for jj in range(w):
                    if shape[0][jj]:
                        room[top][jj] = False
            else:
                break
        # remove empty rows from the top
        while not any(room[-1]):
            room.pop()
    if verbose:
        print(f'BLOCK {tot_shapes - 1}\n=====================\n=====================')
        print(f'Top 40 rows of room =\n{render_room(room[-40:])}')
    return len(room)

def Part2(lines: list[str]) -> int:
    return 0


SAMPLE_INPUT = [
    ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
]


class Part1Tests(unittest.TestCase):
    def testPart1_sample_input(self):
        self.assertEqual(Part1(SAMPLE_INPUT, 2022, True), 3068)

    def test_10_drops_sample_input(self):
        '''
|....#..|
|....#..|
|....##.|
|....##.|
|..####.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+
        '''
        self.assertEqual(Part1(SAMPLE_INPUT, 10, True), 17)

    def test_15_drops_blows_only_right(self):
        '''
|.....##|
|.....##|
|......#|
|......#|
|......#|
|......#|
|......#|
|......#|
|....###|
|.....#.|
|....###|
|.....#.|
|...####|
|.....##|
|.....##|
|......#|
|......#|
|......#|
|......#|
|......#|
|......#|
|....###|
|.....#.|
|....###|
|.....#.|
|...####|
|.....##|
|.....##|
|......#|
|......#|
|......#|
|......#|
|......#|
|......#|
|....###|
|.....#.|
|....###|
|.....#.|
|...####|
+-------+
        '''
        self.assertEqual(Part1(['>'], 15, True), 39)

    def test_13_drops_blow_only_left(self):
        '''
|..#....|
|..#....|
|###....|
|.#.....|
|###....|
|.#.....|
|####...|
|##.....|
|##.....|
|#......|
|#......|
|#.#....|
|#.#....|
|###....|
|.#.....|
|###....|
|.#.....|
|####...|
|##.....|
|##.....|
|#......|
|#......|
|#.#....|
|#.#....|
|###....|
|.#.....|
|###....|
|.#.....|
|####...|
+-------+
        '''
        self.assertEqual(Part1(['<'], 13, True), 29)

    def test_7_drops_blows_22_left_then_60_right(self):
        '''
|##.....|
|##.....|
|#......|
|#......|
|#.#....|
|#.#....|
|###..#.|
|.#..###|
|###..#.|
|.#.####|
|####...|
+-------+
        '''
        inp = ['<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>']
        self.assertEqual(Part1(inp, 7, True), 11)



class TestPart2(unittest.TestCase):
    def testPart2_sample_input(self):
        self.assertEqual(Part2(SAMPLE_INPUT), 0)


if __name__ == '__main__':
    with open('day17_input.txt') as f:
        lines = re.split('\r?\n', f.read())
    part1_answer = Part1(lines, verbose=True)
    print(f'part 1 answer = {part1_answer}')
    part2_answer = Part2(lines)
    print(f'part 2 answer = {part2_answer}')
    unittest.main()