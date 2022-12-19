# --- Day 17: Pyroclastic Flow ---
# Your handheld device has located an alternative exit from the cave for you and the elephants. 
# The ground is rumbling almost continuously now, but the strange valves bought you some time. It's definitely getting warmer in here, though.

# The tunnels eventually open into a very tall, narrow chamber. Large, oddly-shaped rocks are falling into the chamber from above, presumably due to all the rumbling. 
# If you can't work out where the rocks will fall next, you might be crushed!

# The five types of rocks have the following peculiar shapes, where # is rock and . is empty space:

# ####

# .#.
# ###
# .#.

# ..#
# ..#
# ###

# #
# #
# #
# #

# ##
# ##
# The rocks fall in the order shown above: first the - shape, then the + shape, and so on. 
# Once the end of the list is reached, the same order repeats: the - shape falls first, sixth, 11th, 16th, etc.

# The rocks don't spin, but they do get pushed around by jets of hot gas coming out of the walls themselves. 
# A quick scan reveals the effect the jets of hot gas will have on the rocks as they fall (your puzzle input).

# For example, suppose this was the jet pattern in your cave:

# >>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
# In jet patterns, < means a push to the left, while > means a push to the right. 
# The pattern above means that the jets will push a falling rock right, then right, then right, then left, then left, then right, and so on. 
# If the end of the list is reached, it repeats.

# The tall, vertical chamber is exactly seven units wide. 
# Each rock appears so that its left edge is two units away from the left wall and its bottom edge is three units above the highest rock in the room (or the floor, if there isn't one).

# After a rock appears, it alternates between being pushed by a jet of hot gas one unit (in the direction indicated by the next symbol in the jet pattern) and then falling one unit down. 
# If any movement would cause any part of the rock to move into the walls, floor, or a stopped rock, the movement instead does not occur. 
# If a downward movement would have caused a falling rock to move into the floor or an already-fallen rock, 
# the falling rock stops where it is (having landed on something) and a new rock immediately begins falling.

# Drawing falling rocks with @ and stopped rocks with #, the jet pattern in the example above manifests as follows:

# The first rock begins falling:
# |..@@@@.|
# |.......|
# |.......|
# |.......|
# +-------+

# Jet of gas pushes rock right:
# |...@@@@|
# |.......|
# |.......|
# |.......|
# +-------+

# Rock falls 1 unit:
# |...@@@@|
# |.......|
# |.......|
# +-------+

# Jet of gas pushes rock right, but nothing happens:
# |...@@@@|
# |.......|
# |.......|
# +-------+

# Rock falls 1 unit:
# |...@@@@|
# |.......|
# +-------+

# Jet of gas pushes rock right, but nothing happens:
# |...@@@@|
# |.......|
# +-------+

# Rock falls 1 unit:
# |...@@@@|
# +-------+

# Jet of gas pushes rock left:
# |..@@@@.|
# +-------+

# Rock falls 1 unit, causing it to come to rest:
# |..####.|
# +-------+

# A new rock begins falling:
# |...@...|
# |..@@@..|
# |...@...|
# |.......|
# |.......|
# |.......|
# |..####.|
# +-------+

# Jet of gas pushes rock left:
# |..@....|
# |.@@@...|
# |..@....|
# |.......|
# |.......|
# |.......|
# |..####.|
# +-------+

# Rock falls 1 unit:
# |..@....|
# |.@@@...|
# |..@....|
# |.......|
# |.......|
# |..####.|
# +-------+

# Jet of gas pushes rock right:
# |...@...|
# |..@@@..|
# |...@...|
# |.......|
# |.......|
# |..####.|
# +-------+

# Rock falls 1 unit:
# |...@...|
# |..@@@..|
# |...@...|
# |.......|
# |..####.|
# +-------+

# Jet of gas pushes rock left:
# |..@....|
# |.@@@...|
# |..@....|
# |.......|
# |..####.|
# +-------+

# Rock falls 1 unit:
# |..@....|
# |.@@@...|
# |..@....|
# |..####.|
# +-------+

# Jet of gas pushes rock right:
# |...@...|
# |..@@@..|
# |...@...|
# |..####.|
# +-------+

# Rock falls 1 unit, causing it to come to rest:
# |...#...|
# |..###..|
# |...#...|
# |..####.|
# +-------+

# A new rock begins falling:
# |....@..|
# |....@..|
# |..@@@..|
# |.......|
# |.......|
# |.......|
# |...#...|
# |..###..|
# |...#...|
# |..####.|
# +-------+
# The moment each of the next few rocks begins falling, you would see this:

# |..@....|
# |..@....|
# |..@....|
# |..@....|
# |.......|
# |.......|
# |.......|
# |..#....|
# |..#....|
# |####...|
# |..###..|
# |...#...|
# |..####.|
# +-------+

# |..@@...|
# |..@@...|
# |.......|
# |.......|
# |.......|
# |....#..|
# |..#.#..|
# |..#.#..|
# |#####..|
# |..###..|
# |...#...|
# |..####.|
# +-------+

# |..@@@@.|
# |.......|
# |.......|
# |.......|
# |....##.|
# |....##.|
# |....#..|
# |..#.#..|
# |..#.#..|
# |#####..|
# |..###..|
# |...#...|
# |..####.|
# +-------+

# |...@...|
# |..@@@..|
# |...@...|
# |.......|
# |.......|
# |.......|
# |.####..|
# |....##.|
# |....##.|
# |....#..|
# |..#.#..|
# |..#.#..|
# |#####..|
# |..###..|
# |...#...|
# |..####.|
# +-------+

# |....@..|
# |....@..|
# |..@@@..|
# |.......|
# |.......|
# |.......|
# |..#....|
# |.###...|
# |..#....|
# |.####..|
# |....##.|
# |....##.|
# |....#..|
# |..#.#..|
# |..#.#..|
# |#####..|
# |..###..|
# |...#...|
# |..####.|
# +-------+

# |..@....|
# |..@....|
# |..@....|
# |..@....|
# |.......|
# |.......|
# |.......|
# |.....#.|
# |.....#.|
# |..####.|
# |.###...|
# |..#....|
# |.####..|
# |....##.|
# |....##.|
# |....#..|
# |..#.#..|
# |..#.#..|
# |#####..|
# |..###..|
# |...#...|
# |..####.|
# +-------+

# |..@@...|
# |..@@...|
# |.......|
# |.......|
# |.......|
# |....#..|
# |....#..|
# |....##.|
# |....##.|
# |..####.|
# |.###...|
# |..#....|
# |.####..|
# |....##.|
# |....##.|
# |....#..|
# |..#.#..|
# |..#.#..|
# |#####..|
# |..###..|
# |...#...|
# |..####.|
# +-------+

# |..@@@@.|
# |.......|
# |.......|
# |.......|
# |....#..|
# |....#..|
# |....##.|
# |##..##.|
# |######.|
# |.###...|
# |..#....|
# |.####..|
# |....##.|
# |....##.|
# |....#..|
# |..#.#..|
# |..#.#..|
# |#####..|
# |..###..|
# |...#...|
# |..####.|
# +-------+
# To prove to the elephants your simulation is accurate, they want to know how tall the tower will get after 2022 rocks have stopped (but before the 2023rd rock begins falling). 
# In this example, the tower of rocks will be 3068 units tall.

# How many units tall will the tower of rocks be after 2022 rocks have stopped falling?

# --- Part Two ---
# The elephants are not impressed by your simulation. 
# They demand to know how tall the tower will be after 1000000000000 rocks have stopped! 
# Only then will they feel confident enough to proceed through the cave.

# In the example above, the tower would be 1514285714288 units tall!

# How tall will the tower be after 1000000000000 rocks have stopped?



import timeit
import tqdm


PUSH_LEFT = '<'
PUSH_RIGHT = '>'

ROCK_WALL_LEFT_X = -1
ROCK_WALL_RIGHT_X = 7
ROCK_FLOOR_Y = -1



class Rock_Type_Base:
    """
    Legend:
    . Empty Space
    # Rock
    O Pivot Point Empty Space
    + Pivot Point Rock
    """

    def __init__(self, pos):
        self.pos = pos


    def get_rock_positions(self, pos):
        raise NotImplementedError



class Rock_Type_Horizontal_Line(Rock_Type_Base):
    """

    +###

    """

    def get_rock_positions(self, pos):
        rock_positions = (pos, (pos[0]+1, pos[1]), (pos[0]+2, pos[1]), (pos[0]+3, pos[1]))

        return rock_positions



class Rock_Type_Plus(Rock_Type_Base):
    """
    
    .#.
    ###
    O#.
    
    """

    def get_rock_positions(self, pos):
        rock_positions = (
                                (pos[0]+1, pos[1]+2),
            (pos[0], pos[1]+1), (pos[0]+1, pos[1]+1), (pos[0]+2, pos[1]+1),
                                (pos[0]+1, pos[1]),
        )

        return rock_positions



class Rock_Type_Backwards_L(Rock_Type_Base):
    """
    
    ..#
    ..#
    +##

    """

    def get_rock_positions(self, pos):
        rock_positions = (
                                    (pos[0]+2, pos[1]+2),
                                    (pos[0]+2, pos[1]+1),
            pos, (pos[0]+1, pos[1]), (pos[0]+2, pos[1]),
        )
        
        return rock_positions



class Rock_Type_Vertical_Line(Rock_Type_Base):
    """

    #
    # 
    #
    +

    """

    def get_rock_positions(self, pos):
        rock_positions = (
            (pos[0], pos[1]+3),
            (pos[0], pos[1]+2),
            (pos[0], pos[1]+1),
            pos,
        )
        
        return rock_positions


class Rock_Type_Square(Rock_Type_Base):
    """
    
    ##
    +#
    
    
    """

    def get_rock_positions(self, pos):
        rock_positions = (
            (pos[0], pos[1]+1), (pos[0]+1, pos[1]+1),
            pos, (pos[0]+1, pos[1]),
        )
        
        return rock_positions


ROCK_ORDER = (Rock_Type_Horizontal_Line, Rock_Type_Plus, Rock_Type_Backwards_L, Rock_Type_Vertical_Line, Rock_Type_Square)


def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    return lines[0]



def draw_playfield(playfield, highest_rock_y):
    print('PLAYFIELD START')

    for y in reversed(range(0, highest_rock_y + 1)):
        line = '|'
        for x in range(0, ROCK_WALL_RIGHT_X ):
            if (x,y) in playfield:
                line += '#'
            else:
                line += '.'

        line += '|'
        print(line)

    print('+-------+')
    print('PLAYFIELD END')



def process_data(jet_moves, settled_rock_count_max = 2022):
    playfield = set()
    highest_rock_y = ROCK_FLOOR_Y

    current_rock_instance = None

    settled_rock_count = 0

    jet_moves_length = len(jet_moves)
    jet_moves_used = 0

    pbar = tqdm.tqdm(total=settled_rock_count_max)

    while settled_rock_count < settled_rock_count_max:
        jet_move = jet_moves[jet_moves_used % jet_moves_length]
        jet_moves_used += 1

        # Create New Rock Instance
        if current_rock_instance is None:
            rock_type_class = ROCK_ORDER[settled_rock_count % 5]
            pos = (ROCK_WALL_LEFT_X + 1 + 2, highest_rock_y + 1 + 3)
            current_rock_instance = rock_type_class(pos)

        # JET MOVE
        # Right
        if jet_move == PUSH_RIGHT:
            new_pos = (current_rock_instance.pos[0] + 1, current_rock_instance.pos[1])

        # Left
        else:
            new_pos = (current_rock_instance.pos[0] - 1, current_rock_instance.pos[1])
        
        # JET MOVE VALIDATE
        new_rock_positions = current_rock_instance.get_rock_positions(new_pos)
        valid_move = True
        
        # Walls
        new_rock_positions_xs = [x[0] for x in new_rock_positions]
        if ROCK_WALL_LEFT_X in new_rock_positions_xs or ROCK_WALL_RIGHT_X in new_rock_positions_xs:
            valid_move = False

        # Other Settled Rocks
        if valid_move:
            collision_positions = set.intersection(playfield, set(new_rock_positions))
            if collision_positions:
                valid_move = False

        # Record move
        if valid_move:
            current_rock_instance.pos = new_pos

        # GRAVITY MOVE
        new_pos = (current_rock_instance.pos[0], current_rock_instance.pos[1] - 1)

        # GRAVITY MOVE VALIDATE
        new_rock_positions = current_rock_instance.get_rock_positions(new_pos)
        valid_move = True

        # Floor
        new_rock_positions_ys = [x[1] for x in new_rock_positions]
        if ROCK_FLOOR_Y in new_rock_positions_ys:
            valid_move = False

        # Other Settled Rocks
        if valid_move:
            collision_positions = set.intersection(playfield, set(new_rock_positions))
            if collision_positions:
                valid_move = False

        # Record Move
        if valid_move:
            current_rock_instance.pos = new_pos
        
        # Don't record move, rock is settled as this point        
        else:
            settled_rock_positions = current_rock_instance.get_rock_positions(current_rock_instance.pos)
            playfield.update(settled_rock_positions)
            current_rock_instance = None
            settled_rock_count += 1

            pbar.update(settled_rock_count)

            playfield_ys = [x[1] for x in playfield]
            highest_rock_y = max(playfield_ys)

            #draw_playfield(playfield, highest_rock_y)

    pbar.close()
    
    print('break')
    return highest_rock_y + 1




def run():
    input_data_sample = read_input('./day_17_input_sample.txt')
    input_data = read_input('./day_17_input.txt')

    print('DAY 17')

    # Part 1 Answer
    answer_1_sample = process_data(input_data_sample, settled_rock_count_max = 2022)
    print(f'Answer 1 Sample: {answer_1_sample}') # 3068
    answer_1 = process_data(input_data, settled_rock_count_max = 2022)
    print(f'How many units tall will the tower of rocks be after 2022 rocks have stopped falling? : {answer_1}') # 3163

    # Part 2 Answer
    #answer_2_sample = process_data(input_data_sample, settled_rock_count_max = 1000000000000)
    #print(f'Answer 2 Sample: {answer_2_sample}') # 1514285714288
    #answer_2 = process_data(input_data, settled_rock_count_max = 2022)
    #print(f'How tall will the tower be after 1000000000000 rocks have stopped? : {answer_2}') # 



if __name__ == '__main__':
    start_time = timeit.default_timer()
    run()
    print('Runtime: {} seconds.'.format(round(timeit.default_timer() - start_time, 5)))
