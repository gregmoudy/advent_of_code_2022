# --- Day 12: Hill Climbing Algorithm ---
# You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

# You ask the device for a heightmap of the surrounding area (your puzzle input). 
# The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, 
# where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

# Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). 
# Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

# You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move exactly one square up, down, left, or right. 
# To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; 
# that is, if your current elevation is m, you could step to elevation n, but not to elevation o. 
# (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

# For example:

# Sabqponm
# abcryxxl
# accszExk
# acctuvwj
# abdefghi
# Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, 
# but eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

# v..v<<<<
# >v.vv<<^
# .>vv>E^^
# ..v>>>^^
# ..>>>>>^
# In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>). 
# The location that should get the best signal is still E, and . marks unvisited squares.

# This path reaches the goal in 31 steps, the fewest possible.

# What is the fewest steps required to move from your current position to the location that should get the best signal?

# --- Part Two ---
# As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. 
# The beginning isn't very scenic, though; perhaps you can find a better starting point.

# To maximize exercise while hiking, the trail should start as low as possible: elevation a. The goal is still the square marked E. 
# However, the trail should still be direct, taking the fewest steps to reach its goal. 
# So, you'll need to find the shortest path from any square at elevation a to the square marked E.

# Again consider the example from above:

# Sabqponm
# abcryxxl
# accszExk
# acctuvwj
# abdefghi
# Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at elevation a). 
# If you start at the bottom-left square, you can reach the goal most quickly:

# ...v<<<<
# ...vv<<^
# ...v>E^^
# .>v>>>^^
# >^>>>>>^
# This path reaches the goal in only 29 steps, the fewest possible.

# What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?

import heapq
import string
import timeit


HEIGHT_MAP = None
POS_START = None
POS_END = None


def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
    
    global HEIGHT_MAP
    global POS_START
    global POS_END

    HEIGHT_MAP = list()
    POS_START = (0, 0)
    POS_END = (0, 0)

    for y, line in enumerate(lines):
        height_map_current_row = list()
        for x, char in enumerate(line):

            if char == 'S':
                POS_START = (x, y)
                h = 0

            elif char == 'E':
                POS_END = (x, y)
                h = 25

            else:
                h = string.ascii_letters.index(char)

            height_map_current_row.append(h)
        
        HEIGHT_MAP.append(height_map_current_row)



def get_valid_move_positions(x, y, started_from_end = False):
    global HEIGHT_MAP

    height_map_width = len(HEIGHT_MAP[0])
    height_map_height = len(HEIGHT_MAP)

    for x_i, y_i in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        x_adj = x + x_i
        y_adj = y + y_i

        if not (0 <= x_adj < height_map_width and 0 <= y_adj < height_map_height):
            continue

        if not started_from_end:
            if HEIGHT_MAP[y_adj][x_adj] <= HEIGHT_MAP[y][x] + 1:
                yield x_adj, y_adj

        else:
            if HEIGHT_MAP[y_adj][x_adj] >= HEIGHT_MAP[y][x] - 1:
                yield x_adj, y_adj



def path_find(heap, started_from_end = False):
    # Dijkstra's Algorithm
    visited = [[False] * len(HEIGHT_MAP[0]) for _ in range(len(HEIGHT_MAP))]

    while True:
        steps, x, y = heapq.heappop(heap)

        if visited[y][x]:
            continue

        visited[y][x] = True

        if not started_from_end:
            if (x, y) == POS_END:
                print(steps)
                break

        else:
            if HEIGHT_MAP[y][x] == 0:
                print(steps)
                break

        for x_adj, y_adj in get_valid_move_positions(x, y, started_from_end = started_from_end):
            heapq.heappush(heap, (steps + 1, x_adj, y_adj))



def process_data():
    heap = [(0, POS_START[0], POS_START[1])]
    path_find(heap)

    heap = [(0, POS_END[0], POS_END[1])]
    path_find(heap, started_from_end = True)



def run():
    print('DAY 12')

    read_input('./day_12_input.txt')
    process_data() # 408 / 399



if __name__ == '__main__':
    start_time = timeit.default_timer()
    run()
    print('Runtime: {} seconds.'.format(round(timeit.default_timer() - start_time, 5)))
