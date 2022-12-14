# --- Day 14: Regolith Reservoir ---
# The distress signal leads you to a giant waterfall! Actually, hang on - the signal seems like it's coming from the waterfall itself, 
# and that doesn't make any sense. However, you do notice a little path that leads behind the waterfall.

# Correction: the distress signal leads you behind a giant waterfall! There seems to be a large cave system here, and the signal definitely leads further inside.

# As you begin to make your way deeper underground, you feel the ground rumble for a moment. 
# Sand begins pouring into the cave! If you don't quickly figure out where the sand is going, you could quickly become trapped!

# Fortunately, your familiarity with analyzing the path of falling material will come in handy here. 
# You scan a two-dimensional vertical slice of the cave above you (your puzzle input) and discover that it is mostly air with structures made of rock.

# Your scan traces the path of each solid rock structure and reports the x,y coordinates that form the shape of the path, 
# where x represents distance to the right and y represents distance down. Each path appears as a single line of text in your scan. 
# After the first point of each path, each point indicates the end of a straight horizontal or vertical line to be drawn from the previous point. For example:

# 498,4 -> 498,6 -> 496,6
# 503,4 -> 502,4 -> 502,9 -> 494,9
# This scan means that there are two paths of rock; the first path consists of two straight lines, 
# and the second path consists of three straight lines. (Specifically, the first path consists of a line of rock from 498,4 
# through 498,6 and another line of rock from 498,6 through 496,6.)

# The sand is pouring into the cave from point 500,0.

# Drawing rock as #, air as ., and the source of the sand as +, this becomes:


#   4     5  5
#   9     0  0
#   4     0  3
# 0 ......+...
# 1 ..........
# 2 ..........
# 3 ..........
# 4 ....#...##
# 5 ....#...#.
# 6 ..###...#.
# 7 ........#.
# 8 ........#.
# 9 #########.
# Sand is produced one unit at a time, and the next unit of sand is not produced until the previous unit of sand comes to rest. 
# A unit of sand is large enough to fill one tile of air in your scan.

# A unit of sand always falls down one step if possible. If the tile immediately below is blocked (by rock or sand), 
# the unit of sand attempts to instead move diagonally one step down and to the left. If that tile is blocked, 
# the unit of sand attempts to instead move diagonally one step down and to the right. Sand keeps moving as long as it is able to do so, 
# at each step trying to move down, then down-left, then down-right. If all three possible destinations are blocked, 
# the unit of sand comes to rest and no longer moves, at which point the next unit of sand is created back at the source.

# So, drawing sand that has come to rest as o, the first unit of sand simply falls straight down and then stops:

# ......+...
# ..........
# ..........
# ..........
# ....#...##
# ....#...#.
# ..###...#.
# ........#.
# ......o.#.
# #########.
# The second unit of sand then falls straight down, lands on the first one, and then comes to rest to its left:

# ......+...
# ..........
# ..........
# ..........
# ....#...##
# ....#...#.
# ..###...#.
# ........#.
# .....oo.#.
# #########.
# After a total of five units of sand have come to rest, they form this pattern:

# ......+...
# ..........
# ..........
# ..........
# ....#...##
# ....#...#.
# ..###...#.
# ......o.#.
# ....oooo#.
# #########.
# After a total of 22 units of sand:

# ......+...
# ..........
# ......o...
# .....ooo..
# ....#ooo##
# ....#ooo#.
# ..###ooo#.
# ....oooo#.
# ...ooooo#.
# #########.
# Finally, only two more units of sand can possibly come to rest:

# ......+...
# ..........
# ......o...
# .....ooo..
# ....#ooo##
# ...o#ooo#.
# ..###ooo#.
# ....oooo#.
# .o.ooooo#.
# #########.
# Once all 24 units of sand shown above have come to rest, all further sand flows out the bottom, 
# falling into the endless void. Just for fun, the path any new sand takes before falling forever is shown here with ~:

# .......+...
# .......~...
# ......~o...
# .....~ooo..
# ....~#ooo##
# ...~o#ooo#.
# ..~###ooo#.
# ..~..oooo#.
# .~o.ooooo#.
# ~#########.
# ~..........
# ~..........
# ~..........
# Using your scan, simulate the falling sand. How many units of sand come to rest before sand starts flowing into the abyss below?

# --- Part Two ---
# You realize you misread the scan. There isn't an endless void at the bottom of the scan - there's floor, and you're standing on it!

# You don't have time to scan the floor, so assume the floor is an infinite horizontal line with a y coordinate equal to two plus the highest y coordinate of any point in your scan.

# In the example above, the highest y coordinate of any point is 9, and so the floor is at y=11. 
# (This is as if your scan contained one extra rock path like -infinity,11 -> infinity,11.) With the added floor, the example above now looks like this:

#         ...........+........
#         ....................
#         ....................
#         ....................
#         .........#...##.....
#         .........#...#......
#         .......###...#......
#         .............#......
#         .............#......
#         .....#########......
#         ....................
# <-- etc #################### etc -->
# To find somewhere safe to stand, you'll need to simulate falling sand until a unit of sand comes to rest at 500,0, 
# blocking the source entirely and stopping the flow of sand into the cave. 
# In the example above, the situation finally looks like this after 93 units of sand come to rest:

# ............o............
# ...........ooo...........
# ..........ooooo..........
# .........ooooooo.........
# ........oo#ooo##o........
# .......ooo#ooo#ooo.......
# ......oo###ooo#oooo......
# .....oooo.oooo#ooooo.....
# ....oooooooooo#oooooo....
# ...ooo#########ooooooo...
# ..ooooo.......ooooooooo..
# #########################
# Using your scan, simulate the falling sand until the source of the sand becomes blocked. How many units of sand come to rest?


import re
import timeit

FILLED = set()
MAY_Y = 0
SOURCE_POS = (500, 0)



def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    return lines



def simulate_sand(infinite_floor=False):
    global FILLED
    global MAX_Y

    if infinite_floor:
        if SOURCE_POS in FILLED:
            return SOURCE_POS

    x, y = SOURCE_POS

    while y <= MAX_Y:
        if (x, y + 1) not in FILLED:
            y += 1
            continue

        if (x - 1, y + 1) not in FILLED:
            x -= 1
            y += 1
            continue

        if (x + 1, y + 1) not in FILLED:
            x += 1
            y += 1
            continue

        # Everything filled, come to rest
        if infinite_floor:
            break

        else:
            FILLED.add((x, y))
            return (x, y)
    
    if infinite_floor:
        return (x, y)

    else:
        return None



def process_data(lines, infinite_floor=False):
    global FILLED
    global MAX_Y

    FILLED = set()
    MAX_Y = 0

    # Parse Data
    rock_lines = list()
    for line in lines:
        rock_line_points = list()
        point_strs = re.findall(r'\d+,\d+', line)
        for point_str in point_strs:
            x_str, y_str = point_str.split(',')
            rock_line_point = (int(x_str), int(y_str))
            rock_line_points.append(rock_line_point)
       
        rock_lines.append(rock_line_points)
    
    # Fill out rocks froms parsed data.
    for rock_line in rock_lines:
        for i in range(1, len(rock_line)):
            cx, cy = rock_line[i]
            px, py = rock_line[i - 1]

            if cy != py:
                assert cx == px
                for y in range(min(cy, py), max(cy, py) + 1):
                    FILLED.add((cx, y))

            if cx != px:
                assert cy == py
                for x in range(min(cx, px), max(cx, px) + 1):
                    FILLED.add((x, cy))

    MAX_Y = max([pos[1] for pos in FILLED])


    # RUN SAND SIMULATION
    sand_count = 0
    while True:
        pos = simulate_sand(infinite_floor=infinite_floor)
        if pos is None:
            break

        sand_count += 1

        if infinite_floor:
            FILLED.add(pos)
            if pos == SOURCE_POS:
                break

    return sand_count



def run():
    input_data_sample = read_input('./day_14_input_sample.txt')
    input_data = read_input('./day_14_input.txt')

    print('DAY 14')

    # Part 1 Answer
    answer_1_sample = process_data(input_data_sample)
    print(f'Answer 1 Sample: {answer_1_sample}') # 24
    answer_1 = process_data(input_data)
    print(f'How many units of sand come to rest before sand starts flowing into the abyss below? : {answer_1}') # 625

    # Part 2 Answer
    answer_2_sample = process_data(input_data_sample, infinite_floor=True)
    print(f'Answer 2 Sample: {answer_2_sample}') # 93
    answer_2 = process_data(input_data, infinite_floor=True)
    print(f'How many units of sand come to rest? : {answer_2}') # 25193



if __name__ == '__main__':
    start_time = timeit.default_timer()
    run()
    print('Runtime: {} seconds.'.format(round(timeit.default_timer() - start_time, 5)))
