# --- Day 20: Grove Positioning System ---
# It's finally time to meet back up with the Elves. When you try to contact them, however, you get no reply. Perhaps you're out of range?

# You know they're headed to the grove where the star fruit grows, so if you can figure out where that is, you should be able to meet back up with them.

# Fortunately, your handheld device has a file (your puzzle input) that contains the grove's coordinates! Unfortunately, the file is encrypted - just in case the device were to fall into the wrong hands.

# Maybe you can decrypt it?

# When you were still back at the camp, you overheard some Elves talking about coordinate file encryption. The main operation involved in decrypting the file is called mixing.

# The encrypted file is a list of numbers. To mix the file, move each number forward or backward in the file a number of positions equal to the value of the number being moved. The list is circular, so moving a number off one end of the list wraps back around to the other end as if the ends were connected.

# For example, to move the 1 in a sequence like 4, 5, 6, 1, 7, 8, 9, the 1 moves one position forward: 4, 5, 6, 7, 1, 8, 9. To move the -2 in a sequence like 4, -2, 5, 6, 7, 8, 9, the -2 moves two positions backward, wrapping around: 4, 5, 6, 7, 8, -2, 9.

# The numbers should be moved in the order they originally appear in the encrypted file. Numbers moving around during the mixing process do not change the order in which the numbers are moved.

# Consider this encrypted file:

# 1
# 2
# -3
# 3
# -2
# 0
# 4
# Mixing this file proceeds as follows:

# Initial arrangement:
# 1, 2, -3, 3, -2, 0, 4

# 1 moves between 2 and -3:
# 2, 1, -3, 3, -2, 0, 4

# 2 moves between -3 and 3:
# 1, -3, 2, 3, -2, 0, 4

# -3 moves between -2 and 0:
# 1, 2, 3, -2, -3, 0, 4

# 3 moves between 0 and 4:
# 1, 2, -2, -3, 0, 3, 4

# -2 moves between 4 and 1:
# 1, 2, -3, 0, 3, 4, -2

# 0 does not move:
# 1, 2, -3, 0, 3, 4, -2

# 4 moves between -3 and 0:
# 1, 2, -3, 4, 0, 3, -2
# Then, the grove coordinates can be found by looking at the 1000th, 2000th, and 3000th numbers after the value 0, wrapping around the list as necessary. In the above example, the 1000th number after 0 is 4, the 2000th is -3, and the 3000th is 2; adding these together produces 3.

# Mix your encrypted file exactly once. What is the sum of the three numbers that form the grove coordinates?


import timeit
import tqdm
    


def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    numbers = [int(line) for line in lines]

    return numbers


class Number_Tracker:
    def __init__(self, num, start_index):
        self.num = num
        self.start_index = start_index
    
    def __repr__(self):
        return f'Start Index: {self.start_index} Number: {self.num}'


def process_data(numbers):
    item_0 = None
    original_order = list()
    for i, n in enumerate(numbers):
        number_tracker = Number_Tracker(n,i)
        original_order.append(number_tracker)

    mixed_list = list(original_order)
    for item in tqdm.tqdm(original_order):
        if item.num == 0:
            item_0 = item
            continue

        current_index = mixed_list.index(item)
        new_index = current_index + item.num
        new_index_flat = (new_index % len(mixed_list))

        # if item.num == 4:
        #     print('break')
        
        # if item.num < 0:
        #     if new_index_flat == 0:
        #         new_index_flat = len(mixed_list)
        #     else:
        #         new_index_flat -= 1

        # if item.num > 0:
        #     if new_index != new_index_flat:
        #         new_index_flat += 1

        #if new_index == 0:
            #new_index == len(mixed_list)

        # if new_index >= len(mixed_list):
        #     new_index = (new_index % len(mixed_list)) + 1
        
        # elif new_index < 0:
        #     new_index = (new_index % len(mixed_list)) - 1
        
        if new_index_flat == current_index:
            continue

        mixed_list.remove(item)
        mixed_list.insert(current_index, None)

        # if new_index == 0:
        #     mixed_list.append(item)
        
        # else:
        
        if item.num > 0:
            x = 1
        else:
            x = 0
            if new_index_flat == 0:
                new_index_flat = len(mixed_list)

        mixed_list.insert(new_index_flat + x, item)
        mixed_list.remove(None)

    item_0_index = mixed_list.index(item_0) # 4
    item_0_index_plus_1000 = (item_0_index + 1000) % len(mixed_list)
    item_0_index_plus_2000 = (item_0_index + 2000) % len(mixed_list)
    item_0_index_plus_3000 = (item_0_index + 3000) % len(mixed_list)

    coords = [mixed_list[item_0_index_plus_1000].num, mixed_list[item_0_index_plus_2000].num, mixed_list[item_0_index_plus_3000].num]
    coords_sum = sum(coords)

    return coords_sum



def run():
    input_data_sample = read_input('./day_20_input_sample.txt')
    input_data = read_input('./day_20_input.txt')

    print('DAY 20')

    # Part 1 Answer
    answer_1_sample = process_data(input_data_sample)
    print(f'Answer 1 Sample: {answer_1_sample}') # 3
    answer_1 = process_data(input_data)
    print(f'Mix your encrypted file exactly once. What is the sum of the three numbers that form the grove coordinates? : {answer_1}') # 8764 How????

    # Part 2 Answer
    #answer_2_sample = process_data(input_data_sample, settled_rock_count_max = 1000000000000)
    #print(f'Answer 2 Sample: {answer_2_sample}') # 1514285714288
    #answer_2 = process_data(input_data, settled_rock_count_max = 2022)
    #print(f'How tall will the tower be after 1000000000000 rocks have stopped? : {answer_2}') # 



if __name__ == '__main__':
    start_time = timeit.default_timer()
    run()
    print('Runtime: {} seconds.'.format(round(timeit.default_timer() - start_time, 5)))
