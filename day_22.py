# --- Day 22: Monkey Map ---
# The monkeys take you on a surprisingly easy trail through the jungle. 
# They're even going in roughly the right direction according to your handheld device's Grove Positioning System.

# As you walk, the monkeys explain that the grove is protected by a force field. 
# To pass through the force field, you have to enter a password; doing so involves tracing a specific path on a strangely-shaped board.

# At least, you're pretty sure that's what you have to do; the elephants aren't exactly fluent in monkey.

# The monkeys give you notes that they took when they last saw the password entered (your puzzle input).

# For example:

#         ...#
#         .#..
#         #...
#         ....
# ...#.......#
# ........#...
# ..#....#....
# ..........#.
#         ...#....
#         .....#..
#         .#......
#         ......#.

# 10R5L5R10L4R5L5
# The first half of the monkeys' notes is a map of the board. 
# It is comprised of a set of open tiles (on which you can move, drawn .) and solid walls (tiles which you cannot enter, drawn #).

# The second half is a description of the path you must follow. It consists of alternating numbers and letters:

# A number indicates the number of tiles to move in the direction you are facing. If you run into a wall, you stop moving forward and continue with the next instruction.
# A letter indicates whether to turn 90 degrees clockwise (R) or counterclockwise (L). Turning happens in-place; it does not change your current tile.
# So, a path like 10R5 means "go forward 10 tiles, then turn clockwise 90 degrees, then go forward 5 tiles".

# You begin the path in the leftmost open tile of the top row of tiles. Initially, you are facing to the right (from the perspective of how the map is drawn).

# If a movement instruction would take you off of the map, you wrap around to the other side of the board. 
# In other words, if your next tile is off of the board, 
# you should instead look in the direction opposite of your current facing as far as you can until you find the opposite edge of the board, 
# then reappear there.

# For example, if you are at A and facing to the right, the tile in front of you is marked B; 
# if you are at C and facing down, the tile in front of you is marked D:

#         ...#
#         .#..
#         #...
#         ....
# ...#.D.....#
# ........#...
# B.#....#...A
# .....C....#.
#         ...#....
#         .....#..
#         .#......
#         ......#.
# It is possible for the next tile (after wrapping around) to be a wall; this still counts as there being a wall in front of you, 
# and so movement stops before you actually wrap to the other side of the board.

# By drawing the last facing you had with an arrow on each tile you visit, the full path taken by the above example looks like this:

#         >>v#    
#         .#v.    
#         #.v.    
#         ..v.    
# ...#...v..v#    
# >>>v...>#.>>    
# ..#v...#....    
# ...>>>>v..#.    
#         ...#....
#         .....#..
#         .#......
#         ......#.
# To finish providing the password to this strange input device, you need to determine numbers for your final row, column, 
# and facing as your final position appears from the perspective of the original map. Rows start from 1 at the top and count downward; 
# columns start from 1 at the left and count rightward. (In the above example, row 1, column 1 refers to the empty space with no tile on it in the top-left corner.) 
# Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^). The final password is the sum of 1000 times the row, 4 times the column, and the facing.

# In the above example, the final row is 6, the final column is 8, and the final facing is 0. So, the final password is 1000 * 6 + 4 * 8 + 0: 6032.

# Follow the path given in the monkeys' notes. What is the final password?

# --- Part Two ---
# As you reach the force field, you think you hear some Elves in the distance. Perhaps they've already arrived?

# You approach the strange input device, but it isn't quite what the monkeys drew in their notes. 
# Instead, you are met with a large cube; each of its six faces is a square of 50x50 tiles.

# To be fair, the monkeys' map does have six 50x50 regions on it. If you were to carefully fold the map, 
# you should be able to shape it into a cube!

# In the example above, the six (smaller, 4x4) faces of the cube are:

#         1111
#         1111
#         1111
#         1111
# 222233334444
# 222233334444
# 222233334444
# 222233334444
#         55556666
#         55556666
#         55556666
#         55556666
# You still start in the same position and with the same facing as before, but the wrapping rules are different. 
# Now, if you would walk off the board, you instead proceed around the cube. From the perspective of the map, 
# this can look a little strange. In the above example, if you are at A and move to the right, you would arrive at B facing down; 
# if you are at C and move down, you would arrive at D facing up:

#         ...#
#         .#..
#         #...
#         ....
# ...#.......#
# ........#..A
# ..#....#....
# .D........#.
#         ...#..B.
#         .....#..
#         .#......
#         ..C...#.
# Walls still block your path, even if they are on a different face of the cube. 
# If you are at E facing up, your movement is blocked by the wall marked by the arrow:

#         ...#
#         .#..
#      -->#...
#         ....
# ...#..E....#
# ........#...
# ..#....#....
# ..........#.
#         ...#....
#         .....#..
#         .#......
#         ......#.
# Using the same method of drawing the last facing you had with an arrow on each tile you visit, 
# the full path taken by the above example now looks like this:

#         >>v#    
#         .#v.    
#         #.v.    
#         ..v.    
# ...#..^...v#    
# .>>>>>^.#.>>    
# .^#....#....    
# .^........#.    
#         ...#..v.
#         .....#v.
#         .#v<<<<.
#         ..v...#.
# The final password is still calculated from your final position and facing from the perspective of the map. 
# In this example, the final row is 5, the final column is 7, and the final facing is 3, so the final password is 1000 * 5 + 4 * 7 + 3 = 5031.

# Fold the map into a cube, then follow the path given in the monkeys' notes. What is the final password?


import re
import timeit
import tqdm


TILE_NULL = ' '
TILE_PATH = '.'
TILE_WALL = '#'

ROTATE_LEFT     = 'L'
ROTATE_RIGHT    = 'R'

FACING_RIGHT    = 0
FACING_DOWN     = 1
FACING_LEFT     = 2
FACING_UP       = 3

ROTATION_ORDER = (FACING_RIGHT, FACING_DOWN, FACING_LEFT, FACING_UP)

MOVE_OFFSET_RIGHT   = ( 1,  0)
MOVE_OFFSET_DOWN    = ( 0,  1)
MOVE_OFFSET_LEFT    = (-1,  0)
MOVE_OFFSET_UP      = ( 0, -1)

FACING_TO_MOVE_OFFSET = { 
    FACING_RIGHT    : MOVE_OFFSET_RIGHT, 
    FACING_DOWN     : MOVE_OFFSET_DOWN, 
    FACING_LEFT     : MOVE_OFFSET_LEFT, 
    FACING_UP       : MOVE_OFFSET_UP,
}

FACING_TO_CHAR = { 
    FACING_RIGHT    : '>', 
    FACING_DOWN     : 'V', 
    FACING_LEFT     : '<', 
    FACING_UP       : 'A',
}


def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    map_data = lines[:-2]
    dir_line = lines[-1]

    # Break apart elements of direction string into characters and numbers.
    matches = re.findall( r'\d+|\D', dir_line)
    directions = list()
    for match in matches:
        if match.isnumeric():
            directions.append(int(match))
        else:
            directions.append(match)

    return map_data, directions



def get_starting_position(map_data):
    starting_pos = (0, 0)

    for i, tile in enumerate(map_data[0]):
        if tile == TILE_PATH:
            starting_pos = (i, 0)
            break

    return starting_pos



def rotate(current_facing, rotation_direction):
    rotation_index = ROTATION_ORDER.index(current_facing)

    # Right
    if rotation_direction == ROTATE_RIGHT:
        new_facing_direction = ROTATION_ORDER[(rotation_index + 1) % len(ROTATION_ORDER)]

    # Left
    else:
        new_facing_direction = ROTATION_ORDER[rotation_index - 1]
    
    return new_facing_direction



def get_edge_mapping(map_data):
    # TODO: I don't know how to generate this data programatically so I'm hard coding it for now.
    edge_mapping = dict()

    # SAMPLE
    if len(map_data) == 12:
        # 14 edges, 4x4 sides. start and ends need to line up.
        positions_per_edge = 4

        # The facining direction is the way the player will face after crossing the edge defined.
        # SRC First Position, SRC Increment Offset, SRC Incoming Direction, SRC New Facing Direction, DEST First Position, DEST Increment Offset, DEST Incoming Direction, DEST New Facing Direction

        # Only need to define 7 as I will reverse them.
        edge_defines = (
            ((8, 0), (1, 0), FACING_UP, FACING_DOWN, (3, 4), (-1, 0), FACING_UP, FACING_DOWN),
            ((8, 0), (0, 1), FACING_LEFT, FACING_DOWN, (4, 4), (1, 0), FACING_UP, FACING_RIGHT),
            ((11, 0), (0, 1), FACING_RIGHT, FACING_LEFT, (15, 11), (0, -1), FACING_RIGHT, FACING_LEFT),
            ((0, 4), (0, 1), FACING_LEFT, FACING_UP, (15, 11), (-1, 0), FACING_DOWN, FACING_RIGHT),
            ((11, 4), (0, 1), FACING_RIGHT, FACING_DOWN, (15, 8), (-1, 0), FACING_UP, FACING_LEFT),
            ((0, 7), (1, 0), FACING_DOWN, FACING_UP, (11, 11), (-1, 0), FACING_DOWN, FACING_UP),
            ((4, 7), (1, 0), FACING_DOWN, FACING_RIGHT, (8, 11), (0, -1), FACING_LEFT, FACING_UP),
        )

    # FULL
    else:
        # 14 edges but define 7, 50x50 sides.
        positions_per_edge = 50
        edge_defines = (
            ((50, 0), (1, 0), FACING_UP, FACING_RIGHT, (0, 150), (0, 1), FACING_LEFT, FACING_DOWN),
            ((100, 0), (1, 0), FACING_UP, FACING_UP, (0, 199), (1, 0), FACING_DOWN, FACING_DOWN),
            ((50, 0), (0, 1), FACING_LEFT, FACING_RIGHT, (0, 149), (0, -1), FACING_LEFT, FACING_RIGHT),
            ((149, 0), (0, 1), FACING_RIGHT, FACING_LEFT, (99, 149), (0, -1), FACING_RIGHT, FACING_LEFT),
            ((50, 50), (0, 1), FACING_LEFT, FACING_DOWN, (0, 100), (1, 0), FACING_UP, FACING_RIGHT),
            ((100, 49), (1, 0), FACING_DOWN, FACING_LEFT, (99, 50), (0, 1), FACING_LEFT, FACING_UP),
            ((50, 149), (1, 0), FACING_DOWN, FACING_LEFT, (49, 150), (0, 1), FACING_RIGHT, FACING_UP),
        )


    if edge_defines:
        for src_first_pos, src_inc_offset, src_cur_dir, src_new_dir, dest_first_pos, dest_inc_offset, dest_cur_dir, dest_new_dir in edge_defines:
            src_first_pos_cur = src_first_pos
            dest_first_pos_cur = dest_first_pos

            edge_position_count = 0
            while edge_position_count < positions_per_edge:
                src_edge_pos_define_key = (src_first_pos_cur, src_cur_dir)
                src_edge_pos_define_val = (dest_first_pos_cur, src_new_dir)
                edge_mapping[src_edge_pos_define_key] = src_edge_pos_define_val

                dest_edge_pos_define_key = (dest_first_pos_cur, dest_cur_dir)
                dest_edge_pos_define_val = (src_first_pos_cur, dest_new_dir)
                edge_mapping[dest_edge_pos_define_key] = dest_edge_pos_define_val

                # Increment
                src_first_pos_cur = tuple(map(sum, zip(src_first_pos_cur, src_inc_offset)))
                dest_first_pos_cur = tuple(map(sum, zip(dest_first_pos_cur, dest_inc_offset)))

                edge_position_count += 1
    
    return edge_mapping



def make_move(map_data, current_pos, current_facing, steps, cube_wrap = False):
    new_pos = current_pos # This is the final new positions, and the position validate per step.
    new_facing = current_facing # This is the final new facing.

    # TODO: I should probably precaluate this once instead of every move.
    x_len = 0
    for row in map_data:
        x_len = max(x_len, len(row))

    # TODO: I should probably precaluate this once instead of every move.
    y_len = len(map_data)

    edge_mapping = dict()
    if cube_wrap:
        edge_mapping = get_edge_mapping(map_data)

    for _i in range(steps):
        possible_new_pos = new_pos # Potential new position.
        possible_new_facing = new_facing

        tile = None

        # Find a valid tile. This handles the wrap around from null tiles or index errors.
        while tile is None:
            possible_new_facing = new_facing
            move_offset = FACING_TO_MOVE_OFFSET[new_facing]

            if cube_wrap and (possible_new_pos, new_facing) in edge_mapping:
                edge_wrap_pos_dest, edge_wrap_facing_dest = edge_mapping.get((possible_new_pos, new_facing), (None, None))
                possible_new_pos = edge_wrap_pos_dest
                possible_new_facing = edge_wrap_facing_dest

            else:
                possible_new_pos = ((possible_new_pos[0] + move_offset[0]) % x_len, (possible_new_pos[1] + move_offset[1]) % y_len)

            try:
                tile = map_data[possible_new_pos[1]][possible_new_pos[0]]

            except:
                tile = None
            
            if tile == TILE_NULL:
                tile = None

        if tile == TILE_WALL:
            break
        
        elif tile == TILE_PATH:
            new_pos = possible_new_pos
            new_facing = possible_new_facing
            print_map_data(map_data, new_pos, new_facing)

    return new_pos, new_facing



def print_map_data(map_data, current_pos, current_facing):
    return

    print('==========MAP==========')
    for i, row in enumerate(map_data):
        if i == current_pos[1]:
            player_char = FACING_TO_CHAR[current_facing]
            row_with_character = row[:current_pos[0]] + player_char + row[current_pos[0] + 1:]
            print(row_with_character)

        else:
            print(row)

    print('=======================')



def get_answer_1(map_data, directions, cube_wrap = False):
    # Init Starting Values
    current_pos = get_starting_position(map_data)
    current_facing = FACING_RIGHT

    print_map_data(map_data, current_pos, current_facing)

    # Process Directions
    for direction in directions:
        # Movement
        if isinstance(direction, int):
            current_pos, current_facing = make_move(map_data, current_pos, current_facing, direction, cube_wrap = cube_wrap)

        # Rotation
        else:
            current_facing = rotate(current_facing, direction)
            print_map_data(map_data, current_pos, current_facing)

    # Calculate Answer - Position is offset by 1 because of 0 starting index.
    answer = sum([1000 * (current_pos[1] + 1), 4 * (current_pos[0] + 1), current_facing])

    return answer



def run():
    map_data_sample, directions_sample = read_input('./day_22_input_sample.txt')
    map_data, directions = read_input('./day_22_input.txt')
  
    print('DAY 22')

    # Part 1 Answer
    answer_1_sample = get_answer_1(map_data_sample, directions_sample)
    print(f'Answer 1 Sample: {answer_1_sample}') # 6032
    answer_1 = get_answer_1(map_data, directions)
    print(f'What is the final password? : {answer_1}') # 89224

    # Part 2 Answer
    answer_2_sample = get_answer_1(map_data_sample, directions_sample, cube_wrap = True)
    print(f'Answer 2 Sample: {answer_2_sample}') # 5031
    answer_2 = get_answer_1(map_data, directions, cube_wrap = True)
    print(f"What is the final password? : {answer_2}") # 136182



if __name__ == '__main__':
    start_time = timeit.default_timer()
    run()
    print('Runtime: {} seconds.'.format(round(timeit.default_timer() - start_time, 5)))
