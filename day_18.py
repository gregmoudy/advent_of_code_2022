# --- Day 18: Boiling Boulders ---
# You and the elephants finally reach fresh air. You've emerged near the base of a large volcano that seems to be actively erupting! 
# Fortunately, the lava seems to be flowing away from you and toward the ocean.

# Bits of lava are still being ejected toward you, so you're sheltering in the cavern exit a little longer. 
# Outside the cave, you can see the lava landing in a pond and hear it loudly hissing as it solidifies.

# Depending on the specific compounds in the lava and speed at which it cools, 
# it might be forming obsidian! The cooling rate should be based on the surface area of the lava droplets, 
# so you take a quick scan of a droplet as it flies past you (your puzzle input).

# Because of how quickly the lava is moving, the scan isn't very good; its resolution is quite low and, as a result, 
# it approximates the shape of the lava droplet with 1x1x1 cubes on a 3D grid, each given as its x,y,z position.

# To approximate the surface area, count the number of sides of each cube that are not immediately connected to another cube. 
# So, if your scan were only two adjacent cubes like 1,1,1 and 2,1,1, each cube would have a single side covered and five sides exposed, a total surface area of 10 sides.

# Here's a larger example:

# 2,2,2
# 1,2,2
# 3,2,2
# 2,1,2
# 2,3,2
# 2,2,1
# 2,2,3
# 2,2,4
# 2,2,6
# 1,2,5
# 3,2,5
# 2,1,5
# 2,3,5
# In the above example, after counting up all the sides that aren't connected to another cube, the total surface area is 64.

# What is the surface area of your scanned lava droplet?

# --- Part Two ---
# Something seems off about your calculation. The cooling rate depends on exterior surface area, 
# but your calculation also included the surface area of air pockets trapped in the lava droplet.

# Instead, consider only cube sides that could be reached by the water and steam as the lava droplet tumbles into the pond. 
# The steam will expand to reach as much as possible, completely displacing any air on the outside of the lava droplet but never expanding diagonally.

# In the larger example above, exactly one cube of air is trapped within the lava droplet (at 2,2,5), so the exterior surface area of the lava droplet is 58.

# What is the exterior surface area of your scanned lava droplet?


import timeit
import tqdm # pip install tqdm



def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    cube_positions = [eval(x) for x in lines]

    return set(cube_positions)



def get_bounding_box(positions):
    xs = [x[0] for x in positions]
    ys = [x[1] for x in positions]
    zs = [x[2] for x in positions]

    pos_min = (min(xs) - 1, min(ys) - 1, min(zs) - 1)
    pos_max = (max(xs) + 1, max(ys) + 1, max(zs) + 1)

    return { 'pos_min' : pos_min, 'pos_max' : pos_max }



def position_outside_bounding_box(pos, bbox):
    if ( 
        bbox['pos_min'][0] <= pos[0] and pos[0] <= bbox['pos_max'][0] and 
        bbox['pos_min'][1] <= pos[1] and pos[1] <= bbox['pos_max'][1] and 
        bbox['pos_min'][2] <= pos[2] and pos[2] <= bbox['pos_max'][2] 
        ):

        return False
    
    return True



def get_outside_air_positions(cube_positions):
    
    def _fill_xyz_ranges( x_range, y_range, z_range, positions):
        for x in x_range:
            for y in y_range:
                for z in z_range:
                    positions.add((x, y, z))

    outside_air_positions = set()

    xs = [x[0] for x in cube_positions]
    ys = [x[1] for x in cube_positions]
    zs = [x[2] for x in cube_positions]

    pos_max = (max(xs) + 1, max(ys) + 1, max(zs) + 1)
    pos_min = (min(xs) - 1, min(ys) - 1, min(zs) - 1)

    # Front/Back
    _fill_xyz_ranges(
        range(pos_min[0], pos_max[0] + 1), 
        range(pos_min[1], pos_max[1] + 1), 
        [pos_max[2]],
        outside_air_positions,
    )

    _fill_xyz_ranges(
        range(pos_min[0], pos_max[0] + 1), 
        range(pos_min[1], pos_max[1] + 1), 
        [pos_min[2]],
        outside_air_positions,
    )

    # Left/Right
    _fill_xyz_ranges(
        [pos_min[0]], 
        range(pos_min[1], pos_max[1] + 1), 
        range(pos_min[2], pos_max[2] + 1), 
        outside_air_positions,
    )

    _fill_xyz_ranges(
        [pos_max[0]], 
        range(pos_min[1], pos_max[1] + 1), 
        range(pos_min[2], pos_max[2] + 1), 
        outside_air_positions,
    )

    # Top/Bottom
    _fill_xyz_ranges(
        range(pos_min[0], pos_max[0] + 1), 
        [pos_min[1]], 
        range(pos_min[2], pos_max[2] + 1), 
        outside_air_positions,
    )

    _fill_xyz_ranges(
        range(pos_min[0], pos_max[0] + 1), 
        [pos_max[1]], 
        range(pos_min[2], pos_max[2] + 1), 
        outside_air_positions,
    )

    return outside_air_positions



def get_neighbor_positions(pos):
    n_xp = (pos[0] + 1, pos[1], pos[2])
    n_xn = (pos[0] - 1, pos[1], pos[2])
    n_yp = (pos[0], pos[1] + 1, pos[2])
    n_yn = (pos[0], pos[1] - 1, pos[2])
    n_zp = (pos[0], pos[1], pos[2] + 1)
    n_zn = (pos[0], pos[1], pos[2] - 1)

    return (n_xp, n_xn, n_yp, n_yn, n_zp, n_zn)



def is_exposed_to_air(pos, cube_positions, outside_air_only = False, outside_air_positions = None):
    if not outside_air_only:
        if pos not in cube_positions:
            return True
        
        return False
    
    # OUTSIDE AIR ONLY
    cubes_to_check = [pos]
    positions_checked = set()

    while len(cubes_to_check) > 0:
        cube_pos = cubes_to_check.pop()
        if cube_pos in cube_positions:
            continue

        if cube_pos in positions_checked:
            continue

        if cube_pos in outside_air_positions:
            return True
        
        #if position_outside_bounding_box(cube_pos, outside_air_positions):
            #return True

        positions_checked.add(cube_pos)

        neighbor_positions = get_neighbor_positions(cube_pos)
        cubes_to_check.extend(neighbor_positions)

    return False
    


def process_data(cube_positions, outside_air_only = False):
    exposed_sides = 0

    outside_air_positions = None
    if outside_air_only:
        # TODO: Instead of generating all these cube positions, there is probably a quicker function to check if a cube of air falls out side the bounds of all the rock cubes.
        outside_air_positions = get_outside_air_positions(cube_positions) # This is actually 3 seconds faster then checking the bounding box.
        #outside_air_positions = get_bounding_box(cube_positions)


    for cube_pos in tqdm.tqdm(cube_positions):
        neighbor_positions = get_neighbor_positions(cube_pos)
        for n_pos in neighbor_positions:
            exposed = is_exposed_to_air(n_pos, cube_positions, outside_air_only = outside_air_only, outside_air_positions = outside_air_positions)
            if exposed:
                exposed_sides += 1

    return exposed_sides



def run():
    input_data_sample = read_input('./day_18_input_sample.txt')
    input_data = read_input('./day_18_input.txt')

    print('DAY 18')

    # Part 1 Answer
    answer_1_sample = process_data(input_data_sample)
    print(f'Answer 1 Sample: {answer_1_sample}') # 64
    answer_1 = process_data(input_data)
    print(f'What is the surface area of your scanned lava droplet? : {answer_1}') # 4370

    # Part 2 Answer
    answer_2_sample = process_data(input_data_sample, outside_air_only = True)
    print(f'Answer 2 Sample: {answer_2_sample}') # 58
    answer_2 = process_data(input_data, outside_air_only = True)
    print(f'What is the exterior surface area of your scanned lava droplet? : {answer_2}') # 2458



if __name__ == '__main__':
    start_time = timeit.default_timer()
    run()
    print('Runtime: {} seconds.'.format(round(timeit.default_timer() - start_time, 5)))
