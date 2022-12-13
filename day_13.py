# --- Day 13: Distress Signal ---
# You climb the hill and again try contacting the Elves. However, you instead receive a signal you weren't expecting: a distress signal.

# Your handheld device must still not be working properly; the packets from the distress signal got decoded out of order. 
# You'll need to re-order the list of received packets (your puzzle input) to decode the message.

# Your list consists of pairs of packets; pairs are separated by a blank line. 
# You need to identify how many pairs of packets are in the right order.

# For example:

# [1,1,3,1,1]
# [1,1,5,1,1]

# [[1],[2,3,4]]
# [[1],4]

# [9]
# [[8,7,6]]

# [[4,4],4,4]
# [[4,4],4,4,4]

# [7,7,7,7]
# [7,7,7]

# []
# [3]

# [[[]]]
# [[]]

# [1,[2,[3,[4,[5,6,7]]]],8,9]
# [1,[2,[3,[4,[5,6,0]]]],8,9]
# Packet data consists of lists and integers. Each list starts with [, ends with ], 
# and contains zero or more comma-separated values (either integers or other lists). Each packet is always a list and appears on its own line.

# When comparing two values, the first value is called left and the second value is called right. Then:

# If both values are integers, the lower integer should come first. If the left integer is lower than the right integer, 
# the inputs are in the right order. If the left integer is higher than the right integer, the inputs are not in the right order. 
# Otherwise, the inputs are the same integer; continue checking the next part of the input.
# If both values are lists, compare the first value of each list, then the second value, and so on. 
# If the left list runs out of items first, the inputs are in the right order. If the right list runs out of items first, the inputs are not in the right order. 
# If the lists are the same length and no comparison makes a decision about the order, continue checking the next part of the input.
# If exactly one value is an integer, convert the integer to a list which contains that integer as its only value, then retry the comparison. 
# For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2); the result is then found by instead comparing [0,0,0] and [2].
# Using these rules, you can determine which of the pairs in the example are in the right order:

# == Pair 1 ==
# - Compare [1,1,3,1,1] vs [1,1,5,1,1]
#   - Compare 1 vs 1
#   - Compare 1 vs 1
#   - Compare 3 vs 5
#     - Left side is smaller, so inputs are in the right order

# == Pair 2 ==
# - Compare [[1],[2,3,4]] vs [[1],4]
#   - Compare [1] vs [1]
#     - Compare 1 vs 1
#   - Compare [2,3,4] vs 4
#     - Mixed types; convert right to [4] and retry comparison
#     - Compare [2,3,4] vs [4]
#       - Compare 2 vs 4
#         - Left side is smaller, so inputs are in the right order

# == Pair 3 ==
# - Compare [9] vs [[8,7,6]]
#   - Compare 9 vs [8,7,6]
#     - Mixed types; convert left to [9] and retry comparison
#     - Compare [9] vs [8,7,6]
#       - Compare 9 vs 8
#         - Right side is smaller, so inputs are not in the right order

# == Pair 4 ==
# - Compare [[4,4],4,4] vs [[4,4],4,4,4]
#   - Compare [4,4] vs [4,4]
#     - Compare 4 vs 4
#     - Compare 4 vs 4
#   - Compare 4 vs 4
#   - Compare 4 vs 4
#   - Left side ran out of items, so inputs are in the right order

# == Pair 5 ==
# - Compare [7,7,7,7] vs [7,7,7]
#   - Compare 7 vs 7
#   - Compare 7 vs 7
#   - Compare 7 vs 7
#   - Right side ran out of items, so inputs are not in the right order

# == Pair 6 ==
# - Compare [] vs [3]
#   - Left side ran out of items, so inputs are in the right order

# == Pair 7 ==
# - Compare [[[]]] vs [[]]
#   - Compare [[]] vs []
#     - Right side ran out of items, so inputs are not in the right order

# == Pair 8 ==
# - Compare [1,[2,[3,[4,[5,6,7]]]],8,9] vs [1,[2,[3,[4,[5,6,0]]]],8,9]
#   - Compare 1 vs 1
#   - Compare [2,[3,[4,[5,6,7]]]] vs [2,[3,[4,[5,6,0]]]]
#     - Compare 2 vs 2
#     - Compare [3,[4,[5,6,7]]] vs [3,[4,[5,6,0]]]
#       - Compare 3 vs 3
#       - Compare [4,[5,6,7]] vs [4,[5,6,0]]
#         - Compare 4 vs 4
#         - Compare [5,6,7] vs [5,6,0]
#           - Compare 5 vs 5
#           - Compare 6 vs 6
#           - Compare 7 vs 0
#             - Right side is smaller, so inputs are not in the right order
# What are the indices of the pairs that are already in the right order? (The first pair has index 1, the second pair has index 2, and so on.) 
# In the above example, the pairs in the right order are 1, 2, 4, and 6; the sum of these indices is 13.

# Determine which pairs of packets are already in the right order. What is the sum of the indices of those pairs?

# --- Part Two ---
# Now, you just need to put all of the packets in the right order. Disregard the blank lines in your list of received packets.

# The distress signal protocol also requires that you include two additional divider packets:

# [[2]]
# [[6]]
# Using the same rules as before, organize all packets - the ones in your list of received packets as well as the two divider packets - into the correct order.

# For the example above, the result of putting the packets in the correct order is:

# []
# [[]]
# [[[]]]
# [1,1,3,1,1]
# [1,1,5,1,1]
# [[1],[2,3,4]]
# [1,[2,[3,[4,[5,6,0]]]],8,9]
# [1,[2,[3,[4,[5,6,7]]]],8,9]
# [[1],4]
# [[2]]
# [3]
# [[4,4],4,4]
# [[4,4],4,4,4]
# [[6]]
# [7,7,7]
# [7,7,7,7]
# [[8,7,6]]
# [9]
# Afterward, locate the divider packets. To find the decoder key for this distress signal, 
# you need to determine the indices of the two divider packets and multiply them together. 
# (The first packet is at index 1, the second packet is at index 2, and so on.) In this example, 
# the divider packets are 10th and 14th, and so the decoder key is 140.

# Organize all of the packets into the correct order. What is the decoder key for the distress signal?

import functools
import timeit

ORDER_UNKNOWN   = 0
ORDER_WRONG     = 1
ORDER_CORRECT   = -1

DIVIDER_PACKET_2 = [[2]]
DIVIDER_PACKET_6 = [[6]]


def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    pairs = list()
    pair = list()
    for line in lines:
        if not line:
            continue

        pair.append(eval(line))
        if len(pair) == 2:
            pairs.append(pair)
            pair = list()

    return pairs



def pair_items_compare(item_left = None, item_right = None):
    # Check Lists
    result = ORDER_UNKNOWN

    # LISTS
    if isinstance(item_left, list) and isinstance(item_right, list):
        # If the left runs out of items first: CORRECT ORDER
        # If the right list runs out of items first: WRONG ORDER
        # If they are the same length and order was determines, UNKNOWN ORDER

        max_len = max(len(item_left), len(item_right))
        item_left_copy = list(item_left)
        item_right_copy = list(item_right)

        for i in range(max_len):
            try:
                item_left_child = item_left_copy.pop(0)

            except IndexError:
                result = ORDER_CORRECT
                break

            try:
                item_right_child = item_right_copy.pop(0)

            except IndexError:
                result = ORDER_WRONG
                break

            result = pair_items_compare(item_left_child, item_right_child)
            if result in [ ORDER_WRONG, ORDER_CORRECT]:
                break

    # LIST / INT MISMATCH
    elif isinstance(item_left, int) and isinstance(item_right, list):
        result = pair_items_compare([item_left], item_right)
    
    elif isinstance(item_left, list) and isinstance(item_right, int):
        result = pair_items_compare(item_left, [item_right])

    # INTS
    elif isinstance(item_left, int) and isinstance(item_right, int):
        if item_left < item_right:
            result = ORDER_CORRECT
        
        elif item_left > item_right:
            result = ORDER_WRONG

    return result



def process_data(pairs):
    pair_number = 0
    pair_number_sum = 0

    for pair in pairs:
        pair_number += 1
        
        result = pair_items_compare(pair[0], pair[1])
        if result == ORDER_CORRECT:
            pair_number_sum += pair_number

    return pair_number_sum



def sort_pairs(pairs):
    pairs_sorted = list()
    for pair in pairs:
        pairs_sorted.append(pair[0])
        pairs_sorted.append(pair[1])
    
    pairs_sorted.append(DIVIDER_PACKET_2)
    pairs_sorted.append(DIVIDER_PACKET_6)

    pairs_sorted.sort(key=functools.cmp_to_key(pair_items_compare))

    return pairs_sorted



def get_answer_2(pairs):
    pairs_sorted = sort_pairs(pairs)
    decoder_key = (pairs_sorted.index(DIVIDER_PACKET_2) + 1) * (pairs_sorted.index(DIVIDER_PACKET_6) + 1)

    return decoder_key



def run():
    input_data_sample = read_input('./day_13_input_sample.txt')
    input_data = read_input('./day_13_input.txt')

    print('DAY 13')

    # Part 1 Answer
    answer_1_sample = process_data(input_data_sample)
    print(f'Answer 1 Sample: {answer_1_sample}') # 13
    answer_1 = process_data(input_data)
    print(f'Determine which pairs of packets are already in the right order. What is the sum of the indices of those pairs? : {answer_1}') # 5252

    # Part 2 Answer
    answer_2_sample = get_answer_2(input_data_sample)
    print(f'Answer 2 Sample: {answer_2_sample}') # 140
    answer_2 = get_answer_2(input_data)
    print(f'Organize all of the packets into the correct order. What is the decoder key for the distress signal? : {answer_2}') # 20592



if __name__ == '__main__':
    start_time = timeit.default_timer()
    run()
    print('Runtime: {} seconds.'.format(round(timeit.default_timer() - start_time, 5)))
