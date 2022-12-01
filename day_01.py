# --- Day 1: Calorie Counting ---
# The jungle must be too overgrown and difficult to navigate in vehicles or access from the air; the Elves' expedition traditionally goes on foot. 
# As your boats approach land, the Elves begin taking inventory of their supplies. One important consideration is food - in particular, the number of Calories each Elf is carrying (your puzzle input).

# The Elves take turns writing down the number of Calories contained by the various meals, snacks, rations, etc. that they've brought with them, one item per line. 
# Each Elf separates their own inventory from the previous Elf's inventory (if any) by a blank line.

# For example, suppose the Elves finish writing their items' Calories and end up with the following list:

# 1000
# 2000
# 3000

# 4000

# 5000
# 6000

# 7000
# 8000
# 9000

# 10000
# This list represents the Calories of the food carried by five Elves:

# The first Elf is carrying food with 1000, 2000, and 3000 Calories, a total of 6000 Calories.
# The second Elf is carrying one food item with 4000 Calories.
# The third Elf is carrying food with 5000 and 6000 Calories, a total of 11000 Calories.
# The fourth Elf is carrying food with 7000, 8000, and 9000 Calories, a total of 24000 Calories.
# The fifth Elf is carrying one food item with 10000 Calories.
# In case the Elves get hungry and need extra snacks, they need to know which Elf to ask: they'd like to know how many Calories are being carried by the Elf carrying the most Calories. 
# In the example above, this is 24000 (carried by the fourth Elf).

# Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?

# --- Part Two ---
# By the time you calculate the answer to the Elves' question, they've already realized that the Elf carrying the most Calories of food might eventually run out of snacks.

# To avoid this unacceptable situation, the Elves would instead like to know the total Calories carried by the top three Elves carrying the most Calories. 
# That way, even if one of those Elves runs out of snacks, they still have two backups.

# In the example above, the top three Elves are the fourth Elf (with 24000 Calories), then the third Elf (with 11000 Calories), then the fifth Elf (with 10000 Calories). 
# The sum of the Calories carried by these three elves is 45000.

# Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?

import timeit



def read_input():
    '''Read the input file and return the string data as tuple of int tuples.'''
    with open('./day_01_input.txt', 'r') as file:
        lines = file.read().splitlines()
    
    elves_calories_per_snack = list() # All the elves snack calories lists.
    elf_calories_per_snack = list()

    for line in lines:
        if not line:
            elves_calories_per_snack.append(tuple(elf_calories_per_snack))
            elf_calories_per_snack = list()
            continue

        elf_calories_per_snack.append(int(line))
 
    elves_calories_per_snack = tuple(elves_calories_per_snack)

    return elves_calories_per_snack



def get_top_total_calories(total_calories_per_elf, elf_count=None):
    '''Using the list given go through and create a tuple of however many max calories per elf were asked for.'''

    # Make a copy so we don't mangle the original as we will be removing items from the list as we find the current max item.
    total_calories_per_elf = list(total_calories_per_elf)

    # If no elf_count is proveded, use the entire list.
    elf_count = elf_count or len(total_calories_per_elf)
    
    # Don't allow elf_count to be higher than what is available in the list.
    elf_count = min(elf_count, len(total_calories_per_elf))
    
    # Go through the list however many times we were told and find the current max value and then remove it from the list keep track of those items along the way.
    top_total_calories = list()
    for _i in range(elf_count):
        top_total_calories_for_elf = max(total_calories_per_elf)
        top_total_calories.append(top_total_calories_for_elf)
        total_calories_per_elf.remove(top_total_calories_for_elf)
    
    top_total_calories = tuple(top_total_calories)

    # Here is a more streamlined approach:
    #top_total_calories = sorted(total_calories_per_elf, reverse=True)[0:elf_count]

    return top_total_calories



def run():
    elves_calories_per_snack = read_input()

    print('DAY 01')    

    # Part 1 Answer
    total_calories_per_elf = [sum(x) for x in elves_calories_per_snack]
    elf_max_total_calories = max(total_calories_per_elf)
    print(f'Find the Elf carrying the most Calories. How many total Calories is that Elf carrying? : {elf_max_total_calories}') # 69528

    #Part 2 Answer
    top_total_calories = get_top_total_calories(total_calories_per_elf, elf_count=3)
    top_total_calories_sum = sum(top_total_calories)
    print(f'Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total? : {top_total_calories_sum}') # 206152



if __name__ == '__main__':
    start_time = timeit.default_timer()
    run()
    print('Runtime: {} seconds.'.format(round(timeit.default_timer() - start_time, 5)))
