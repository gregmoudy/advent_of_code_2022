
import re
import time
import timeit


AIR = '.'
ROCK = '#'
SAND = 'o'
SAND_SOURCE = '+'

X_OFFSET = 0
X_WIDTH = 0
X_SAND_SOURCE = 0

CAVE_MAP = None


def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    return lines



def create_cave_map(lines, add_floor = False):
    global CAVE_MAP
    global X_SAND_SOURCE

    x_min = None
    x_max = None
    y_max = None

    rock_lines = list()
    for line in lines:
        rock_line_points = list()
        point_strs = re.findall(r'\d+,\d+', line)
        for point_str in point_strs:
            x_str, y_str = point_str.split(',')
            rock_line_point = (int(x_str), int(y_str))
            rock_line_points.append(rock_line_point)

            if x_min is None:
                x_min = rock_line_point[0]
                x_max = rock_line_point[0]
                y_max = rock_line_point[1]

            x_min = min(x_min, rock_line_point[0])
            x_max = max(x_max, rock_line_point[0])
            y_max = max(y_max, rock_line_point[1])
        
        rock_lines.append(rock_line_points)

    X_OFFSET = x_min
    X_WIDTH = x_max - x_min
    X_SAND_SOURCE = 500 - x_min

    CAVE_MAP = list()
    for y in range(0, y_max + 1):
        cave_map_row = [ AIR for _x in range(0, X_WIDTH + 1)]
        CAVE_MAP.append(cave_map_row)

    if add_floor:
        cave_map_row = [ AIR for _x in range(0, X_WIDTH + 1)]
        CAVE_MAP.append(cave_map_row)

        cave_map_row = [ ROCK for _x in range(0, X_WIDTH + 1)]
        CAVE_MAP.append(cave_map_row)

    CAVE_MAP[0][X_SAND_SOURCE] = SAND_SOURCE

    for rock_line_points in rock_lines:
        rock_line_point_prev = None
        for rock_line_point in rock_line_points:
            if rock_line_point_prev is None:
                rock_line_point_prev = rock_line_point
                CAVE_MAP[rock_line_point[1]][rock_line_point[0] - X_OFFSET] = ROCK
                continue

            x_range_start = min(rock_line_point_prev[0], rock_line_point[0])
            x_range_end = max(rock_line_point_prev[0], rock_line_point[0]) + 1

            y_range_start = min(rock_line_point_prev[1], rock_line_point[1])
            y_range_end = max(rock_line_point_prev[1], rock_line_point[1]) + 1

            for rock_line_y in range(y_range_start, y_range_end):
                for rock_line_x in range(x_range_start, x_range_end):
                    CAVE_MAP[rock_line_y][rock_line_x - X_OFFSET] = ROCK
            
            rock_line_point_prev = rock_line_point



def print_cave_map():
    print("CAVE MAP")
    for cave_row in CAVE_MAP:
        print(cave_row)
    
    #time.sleep(0.5)



def is_pos_blocked(pos):
    if CAVE_MAP[pos[1]][pos[0]] in [ROCK, SAND]:
        return True
    
    return False



def is_pos_abyss(pos):
    if pos[0] not in range(len(CAVE_MAP[0])) or pos[1] not in range(len(CAVE_MAP)):
        return True

    # The sand is not within a space in the row above the bottom of the map.
    #if pos[1] not in range(len(CAVE_MAP)):
        #return True

    return False



def simulate_sand(print_map = False):
    sand_settled = False
    sand_in_the_abyss = False
    sand_pos = None

    while not sand_in_the_abyss:
        sand_settled = False
        sand_pos = None
        while not sand_settled:
            if print_map:
                print_cave_map()

            # Emit new sand item.
            if sand_pos is None:
                sand_pos = (X_SAND_SOURCE, 0 + 1)
                CAVE_MAP[sand_pos[1]][sand_pos[0]] = SAND
                continue

            sand_pos_down = (sand_pos[0], sand_pos[1] + 1)

            if is_pos_abyss(sand_pos_down):
                sand_in_the_abyss = True
                CAVE_MAP[sand_pos[1]][sand_pos[0]] = AIR
                break

            if not is_pos_blocked(sand_pos_down):
                CAVE_MAP[sand_pos[1]][sand_pos[0]] = AIR
                sand_pos = sand_pos_down
                CAVE_MAP[sand_pos[1]][sand_pos[0]] = SAND
                continue

            sand_pos_left = (sand_pos[0] - 1, sand_pos[1] + 1)

            if is_pos_abyss(sand_pos_left):
                sand_in_the_abyss = True
                CAVE_MAP[sand_pos[1]][sand_pos[0]] = AIR
                break

            if not is_pos_blocked(sand_pos_left):
                CAVE_MAP[sand_pos[1]][sand_pos[0]] = AIR
                sand_pos = sand_pos_left
                CAVE_MAP[sand_pos[1]][sand_pos[0]] = SAND
                continue

            sand_pos_right = (sand_pos[0] + 1, sand_pos[1] + 1)

            if is_pos_abyss(sand_pos_right):
                sand_in_the_abyss = True
                CAVE_MAP[sand_pos[1]][sand_pos[0]] = AIR
                break

            if not is_pos_blocked(sand_pos_right):
                CAVE_MAP[sand_pos[1]][sand_pos[0]] = AIR
                sand_pos = sand_pos_right
                CAVE_MAP[sand_pos[1]][sand_pos[0]] = SAND
                continue

            sand_settled = True
        
    if print_map:
        print_cave_map()

    sand_count = 0
    for cave_row in CAVE_MAP:
        sand_count += cave_row.count(SAND)
    
    print(f'Sand Count: {sand_count}')
    return sand_count



def simulate_sand_2():
    with open("./day_14_input.txt") as fin:
        lines = fin.read().strip().split("\n")

    sand_source = 500, 0

    filled = set()
    for line in lines:
        coords = []

        for str_coord in line.split(" -> "):
            x, y = map(int, str_coord.split(","))
            coords.append((x, y))

        for i in range(1, len(coords)):
            cx, cy = coords[i]  # cur
            px, py = coords[i - 1]

            if cy != py:
                assert cx == px
                for y in range(min(cy, py), max(cy, py) + 1):
                    filled.add((cx, y))

            if cx != px:
                assert cy == py
                for x in range(min(cx, px), max(cx, px) + 1):
                    filled.add((x, cy))


    max_y = max([coord[1] for coord in filled])

    # Fill with sand


    def simulate_sand(filled):
        #global filled
        x, y = 500, 0

        if (x, y) in filled:
            return (x, y)

        while y <= max_y:
            if (x, y + 1) not in filled:
                y += 1
                continue

            if (x - 1, y + 1) not in filled:
                x -= 1
                y += 1
                continue

            if (x + 1, y + 1) not in filled:
                x += 1
                y += 1
                continue

            # Everything filled, come to rest
            break

        return (x, y)


    ans = 0

    while True:
        x, y = simulate_sand(filled)
        filled.add((x, y))
        ans += 1

        if (x, y) == (500, 0):
            break

    print(ans)


def run():
    input_data_sample = read_input('./day_14_input_sample.txt')
    create_cave_map(input_data_sample, add_floor = False)
    simulate_sand(print_map = True)

    simulate_sand_2()

    #input_data = read_input('./day_14_input.txt')
    #create_cave_map(input_data)
    #simulate_sand()

    print('DAY 14')

    # Part 1 Answer
    #answer_1_sample = process_data(input_data_sample)
    #print(f'Answer 1 Sample: {answer_1_sample}') # 13
    #answer_1 = process_data(input_data)
    #print(f'Determine which pairs of packets are already in the right order. What is the sum of the indices of those pairs? : {answer_1}') # 625

    # Part 2 Answer
    #answer_2_sample = get_answer_2(input_data_sample)
    #print(f'Answer 2 Sample: {answer_2_sample}') # 140
    #answer_2 = get_answer_2(input_data)
    #print(f'Organize all of the packets into the correct order. What is the decoder key for the distress signal? : {answer_2}') # 20592



if __name__ == '__main__':
    start_time = timeit.default_timer()
    run()
    print('Runtime: {} seconds.'.format(round(timeit.default_timer() - start_time, 5)))
