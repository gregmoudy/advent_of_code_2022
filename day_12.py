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


import string
import timeit

#string.ascii_letters.index('a')


def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
    
    height_map = list()
    pos_start = (0, 0)
    pos_end = (0, 0)

    for y, line in enumerate(lines):
        height_map_current_row = list()
        for x, char in enumerate(line):

            if char == 'S':
                pos_start = (x, y)
                h = 0

            elif char == 'E':
                pos_end = (x, y)
                h = 25

            else:
                h = string.ascii_letters.index(char)

            height_map_current_row.append(h)
        
        height_map.append(height_map_current_row)

    return height_map, pos_start, pos_end



def run():
    height_map_sample, pos_start_sample, pos_end_sample = read_input('./day_12_input_sample.txt')
    height_map, pos_start, pos_end = read_input('./day_12_input.txt')

    print('DAY 12')

    # Part 1 Answer
    #answer_1_sample = process_data(input_data_sample)
    #print(f'Answer 1 Sample: {answer_1_sample}') # 10605
    #answer_1 = process_data(input_data)
    #print(f'Figure out which monkeys to chase by counting how many items they inspect over 20 rounds. What is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans? : {answer_1}') # 110888

    # Part 2 Answer
    #answer_2_sample = process_data(input_data_sample, rounds = 10000)
    #print(f'Answer 2 Sample: {answer_2_sample}') # 
    #answer_2 = process_data(input_data, rounds = 10000)
    #print(f'Starting again from the initial state in your puzzle input, what is the level of monkey business after 10000 rounds? : {answer_2}') # 



if __name__ == '__main__':
    start_time = timeit.default_timer()
    run()
    print('Runtime: {} seconds.'.format(round(timeit.default_timer() - start_time, 5)))
