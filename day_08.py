# --- Day 8: Treetop Tree House ---
# The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. 
# The Elves explain that a previous expedition planted these trees as a reforestation effort. 
# Now, they're curious if this would be a good location for a tree house.

# First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, 
# you need to count the number of trees that are visible from outside the grid when looking directly along a row or column.

# The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:

# 30373
# 25512
# 65332
# 33549
# 35390
# Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

# A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. 
# Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.

# All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to block the view. 
# In this example, that only leaves the interior nine trees to consider:

# The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
# The top-middle 5 is visible from the top and right.
# The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
# The left-middle 5 is visible, but only from the right.
# The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
# The right-middle 3 is visible from the right.
# In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
# With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.

# Consider your map; how many trees are visible from outside the grid?

# --- Part Two ---
# Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: they would like to be able to see a lot of trees.

# To measure the viewing distance from a given tree, look up, down, left, and right from that tree; 
# stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration. 
# (If a tree is right on the edge, at least one of its viewing distances will be zero.)

# The Elves don't care about distant trees taller than those found by the rules above; 
# the proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

# In the example above, consider the middle 5 in the second row:

# 30373
# 25512
# 65332
# 33549
# 35390
# Looking up, its view is not blocked; it can see 1 tree (of height 3).
# Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
# Looking right, its view is not blocked; it can see 2 trees.
# Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).
# A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. 
# For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

# However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

# 30373
# 25512
# 65332
# 33549
# 35390
# Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
# Looking left, its view is not blocked; it can see 2 trees.
# Looking down, its view is also not blocked; it can see 1 tree.
# Looking right, its view is blocked at 2 trees (by a massive tree of height 9).
# This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

# Consider each tree on your map. What is the highest scenic score possible for any tree?



import timeit


TREE_HEIGHT_GRID = None


def read_input():
    with open('./day_08_input.txt', 'r') as file:
        lines = file.read().splitlines()
  
    tree_rows = list()
    for line in lines:
        tree_row = tuple([ int(x) for x in line ])
        tree_rows.append(tree_row)
    
    tree_rows = tuple(tree_rows)

    return tree_rows



def get_visible_and_scenic_score_from_direction(x_range, y_range, current_tree_height):
    visible_from_range_direction = True
    scenic_score_for_range_direction = 0

    for y in y_range:
        for x in x_range:
            scenic_score_for_range_direction += 1
            adjacent_tree_height = TREE_HEIGHT_GRID[y][x]
            if adjacent_tree_height >= current_tree_height:
                visible_from_range_direction = False
                return visible_from_range_direction, scenic_score_for_range_direction
    
    return visible_from_range_direction, scenic_score_for_range_direction



def scan_trees():
    trees_visible = 0
    max_scenic_score = 0

    x_length = len(TREE_HEIGHT_GRID[0])
    x_range = range(0, x_length)

    y_length = len(TREE_HEIGHT_GRID)
    y_range = range(0, y_length)
    
    for y in y_range:
        for x in x_range:
            current_tree_height = TREE_HEIGHT_GRID[y][x]

            # Left/Right Ranges
            x_look_left_range = list(range(0,x))
            x_look_left_range.reverse()
          
            x_look_right_range = list(range(x+1, x_length))

            # Up/Down Ranges
            y_look_up_range = list(range(0, y))
            y_look_up_range.reverse()

            y_look_down_range = list(range(y + 1, y_length))

            visible_left, scenic_score_left = get_visible_and_scenic_score_from_direction(x_look_left_range, [y], current_tree_height)
            visible_right, scenic_score_right = get_visible_and_scenic_score_from_direction(x_look_right_range, [y], current_tree_height)
            visible_up, scenic_scorce_up = get_visible_and_scenic_score_from_direction([x], y_look_up_range, current_tree_height)
            visible_down, scenic_score_down = get_visible_and_scenic_score_from_direction([x], y_look_down_range, current_tree_height)

            tree_visible = any((visible_left, visible_right, visible_up, visible_down))
            if tree_visible:
                trees_visible += 1
            
            current_scenic_score = scenic_score_left * scenic_score_right * scenic_scorce_up * scenic_score_down
            max_scenic_score = max(max_scenic_score, current_scenic_score)

    return trees_visible, max_scenic_score



def run():
    tree_height_grid = read_input()

    global TREE_HEIGHT_GRID
    TREE_HEIGHT_GRID = tree_height_grid

    print('DAY 08')

    trees_visible, max_scenic_score = scan_trees()

    # Part 1 Answer
    print(f'Consider your map; how many trees are visible from outside the grid? : {trees_visible}') # 1798

    # Part 2 Answer
    print(f"Consider each tree on your map. What is the highest scenic score possible for any tree? : {max_scenic_score}") # 259308



if __name__ == '__main__':
    start_time = timeit.default_timer()
    run()
    print('Runtime: {} seconds.'.format(round(timeit.default_timer() - start_time, 5)))
